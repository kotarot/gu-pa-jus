#!/usr/bin/env python3

import csv
import datetime
import glob
import Levenshtein
import logging
import os
import re
import subprocess
import sys
import yaml

"""
ソースコードを採点するスクリプト。
"""

# 最低得点
MIN_SCORE = 1
# コンテナ名
CONTAINER_NAME = 'my-gu-pa-jus'

def main():
    """
    スクリプトのエントリポイント。
    """

    # 初期設定
    inputs = list(snakemake.input)
    student_ids = []
    assignment_name = None
    grade_yaml = None

    for i in sorted(inputs):
        s = i.split('/')

        # 課題名設定
        if not assignment_name:
            assignment_name = s[1]
        # 設定ファイル
        if i.endswith('.yaml'):
            grade_yaml = i
        # テキストファイル (外部リソース)
        elif i.endswith('.txt'):
            pass
        # 学籍番号
        else:
            student_ids.append(s[-1])

    output_csv = 'results/summary_{}.csv'.format(assignment_name)

    # logging
    file_handler = logging.FileHandler(filename='logs/grade_{}_{}.log'.format(assignment_name, datetime.datetime.now().strftime('%Y%m%d-%H%M%S')))
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [file_handler, stdout_handler]
    logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s | %(message)s',
            handlers=handlers)

    logging.info('Assignment : {}'.format(assignment_name))
    logging.info('#Students  : {}'.format(len(student_ids)))
    logging.info('YAML       : {}'.format(grade_yaml))
    logging.info('Output CSV : {}'.format(output_csv))

    # 設定ファイルの読み込み
    with open(grade_yaml, 'r') as yml:
        grade_config = yaml.load(yml, Loader=yaml.FullLoader)

    # ディレクトリごとに採点開始
    # 同じ学籍番号の結果は同じキーにまとめる
    results_dict = {}
    multi_submission_pattern_str = r'^1[A-Z][0-9A-Z]{6}_[0-9]+$'
    multi_submission_pattern = re.compile(multi_submission_pattern_str)
    for student_dir in student_ids:
        # 同じ学生の複数提出がある場合は学籍番号を抽出する
        if multi_submission_pattern.match(student_dir):
            student_id = student_dir.split('_')[0]
        else:
            student_id = student_dir

        if student_id not in results_dict:
            results_dict[student_id] = []
        results_dict[student_id].append(grade_student(student_dir, assignment_name, grade_config))

    # ベスト結果の選択
    results = []
    for student_id, result in results_dict.items():
        best = [max(s) for s in zip(*result)]
        results.append([student_id] + best)

    # 結果書き込み
    with open(output_csv, 'w') as f:
        writer = csv.writer(f)
        headers = ['student_id'] + get_problems(grade_config)
        writer.writerow(headers)
        writer.writerows(results)


def grade_student(student_id, assignment_name, grade_config):
    """
    各学生のソースコードを採点する。
    それぞれの問題に対する得点をリストで返す。
    """
    logging.info('')
    logging.info('================================================================')
    logging.info('Grading student "{}" ...'.format(student_id))
    logging.info('================================================================')
    result = []

    code_files = [os.path.basename(filename) for filename in glob.glob('data/{}/{}/*.c'.format(assignment_name, student_id))]
    for problem in get_problems(grade_config):
        logging.info('* Desired source code: {}'.format(problem))

        # 作成してほしかったファイル名と最もレーベンシュタイン距離が近いファイル名を採点対象とする
        target_file = get_closest(problem, code_files)
        if not target_file:
            logging.info('  {} is not found (> <) --> score = 0'.format(problem))
            result.append(0)
        else:
            result.append(grade_source_code(
                    'data/{}/{}/{}'.format(assignment_name, student_id, target_file),
                    problem, grade_config))

    return result


def grade_source_code(filename, problem, grade_config):
    """
    ソースコードを採点して、点数を返す。
    ここまできてたら多少のスペルミスはあっても何かしらのソースコードを作成しているので、1点以上はつける。
    """
    logging.info('  Found! Evaluating {}'.format(filename))

    # 対応する問題をconfigから抜き出しておく
    for p in grade_config:
        if p['name'] == problem:
            problem_config = p

    # コンパイル前にdeny listの語句が使用されていないか確かめる
    try:
        with open(filename, 'r') as f:
            s = f.read()
            for d in problem_config['deny_list']:
                if d in s:
                    logging.warning('    The source code contains the word `{}`, which is defined in the deny list. --> score = {}'.format(d, MIN_SCORE))
                    return MIN_SCORE
    except UnicodeDecodeError:
        # ちょっと強引だけど仕方ない
        logging.info('    Cannot decode the source code. --> score = {}'.format(MIN_SCORE))
        return MIN_SCORE

    # ファイルコピー・コンパイルする
    basename = os.path.basename(filename)
    proc = subprocess.run("docker;cp;{};{}:/root/{}".format(filename, CONTAINER_NAME, basename).split(';'))
    proc = subprocess.run('docker exec {} gcc /root/{} -lm -o /root/a.out'.format(CONTAINER_NAME, basename).split(' '))
    if proc.returncode != 0:
        logging.info('    Could not compile the source code. --> score = {}'.format(MIN_SCORE))
        return MIN_SCORE

    # テストケースで実行する
    # 失敗するごとに5点から1点ずつ減らしていく (ただし設定ファイルに得点が指定されていればその点を引く)
    passed, failed, penalty = 0, 0, 0
    for i, test_case in enumerate(problem_config['test_cases']):
        logging.info('    Trying test case {} / {} ... '.format(i + 1, len(problem_config['test_cases'])))

        # 外部ファイルが指定されていればコピーする
        if 'external_file' in test_case:
            student_dir = os.path.dirname(filename)
            external_filename = '{}/../{}'.format(student_dir, test_case['external_file']['source'])
            proc = subprocess.run('docker cp {} {}:/root/{}'.format(external_filename, CONTAINER_NAME, test_case['external_file']['destination']).split(' '))

        try:
            proc = subprocess.run('docker exec -i {} /root/a.out'.format(CONTAINER_NAME).split(' '),
                    input=test_case['input'], encoding='UTF-8',
                    stdout=subprocess.PIPE,
                    timeout=problem_config['timeout'])
        except subprocess.TimeoutExpired as e:
            proc = subprocess.run('docker exec {} pkill -f a.out'.format(CONTAINER_NAME).split(' '))
            logging.info(e)
            logging.info('      Execution timed out. --> score = {}'.format(MIN_SCORE))
            return MIN_SCORE

        output = proc.stdout
        logging.info('      STDOUT ==>\n{}'.format(output))
        match_obj = re.search(test_case['output'], output)
        if match_obj:
            logging.info('      Passed!')
            passed += 1
        else:
            logging.info('      Failed (> <)')
            failed += 1
            if 'penalty' in test_case:
                penalty += test_case['penalty']
            else:
                penalty += 1

    score = 5 - penalty
    if score < MIN_SCORE:
        score = MIN_SCORE
    logging.info('    {} (out of {}) test cases passed. --> score = {}'.format(passed, len(problem_config['test_cases']), score))

    return score


def get_problems(grade_config):
    """
    課題設定ファイルから、問題一覧を抜き出してリストで返す。
    """
    problems = []
    for problem in grade_config:
        problems.append(problem['name'])
    return problems


def get_closest(target, xs):
    """
    xs の中からもっとも target に文字列のレーベンシュタイン距離が近いものを返す。
    ただし、距離が3より離れていたら、対象のファイルはなかったことにする。
    """
    closest = None
    max_distance = sys.maxsize
    for x in xs:
        d = Levenshtein.distance(target, x)
        if d < max_distance:
            closest = x
            max_distance = d
    if max_distance == 0:
        return closest
    elif max_distance <= 3:
        logging.warning('  No files found that match the target `{}`, but `{}` is found.'.format(target, closest))
        return closest
    else:
        return None


if __name__ == '__main__':
    main()
