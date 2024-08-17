# pyright: reportUndefinedVariable=false

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
    for index, student_dir in enumerate(student_ids):
        # 同じ学生の複数提出がある場合は学籍番号を抽出する
        if multi_submission_pattern.match(student_dir):
            student_id = student_dir.split('_')[0]
        else:
            student_id = student_dir

        if student_id not in results_dict:
            results_dict[student_id] = []

        grade_result = grade_student(student_dir, assignment_name, grade_config, f'({index + 1} / {len(student_ids)})')
        results_dict[student_id].append(grade_result)

    # ベスト結果の選択
    results = []
    for student_id, result in results_dict.items():
        best = [max(s) for s in zip(*result)]
        results.append([student_id.split(' ')[0], student_id] + best)

    # 合計得点計算
    for r in results:
        total = round(sum(r[2:]), 2)
        r.append(total)

    # 結果書き込み
    with open(output_csv, 'w') as f:
        writer = csv.writer(f)
        headers = ['student_id', 'student_full'] + get_problems(grade_config) + ['total']
        writer.writerow(headers)
        writer.writerows(results)


def grade_student(student_id, assignment_name, grade_config, progress=''):
    """
    各学生のソースコードを採点する。
    それぞれの問題に対する得点をリストで返す。
    """
    logging.info('')
    logging.info('')
    logging.info('=' * 120)
    logging.info(f'Grading student "{student_id}" ... {progress}')
    logging.info('=' * 120)
    result = []

    # ソースコードのファイル名のみのリスト
    source_files = [os.path.basename(filename) for filename in glob.glob('data/{}/{}/*.c'.format(assignment_name, student_id))]

    # ファイル名から明らかに不要な文字たちを削除する
    # key: 修正後のファイル名, value: 元のファイル名 の辞書を作る
    source_files_with_corrected = {}
    for filename in source_files:
        # 日本語文字（ひらがな、カタカナ、漢字）を削除
        corrected_filename = re.sub(r'[ぁ-ん ァ-ン 一-龥]', '', filename)
        # 全角スペースを削除
        corrected_filename = corrected_filename.replace('　', '')
        # 「1W000000」のパターン文字列を削除
        corrected_filename = re.sub(r'1[a-zA-Z][0-9]{6}', '', corrected_filename)
        # 「(数字)」のパターン文字列を削除
        corrected_filename = re.sub(r'\([0-9]+\)', '', corrected_filename)
        source_files_with_corrected[corrected_filename] = filename

    for problem in get_problems(grade_config):
        logging.info('')
        logging.info('Expecting source code: `{}`'.format(problem))

        # 作成してほしかったファイル名と最もレーベンシュタイン距離が近いファイル名を採点対象とする
        target_file = get_closest(problem, list(source_files_with_corrected.keys()))
        if not target_file:
            logging.warning('{} is not found (> <) --> score = 0'.format(problem))
            result.append(0)
        else:
            original_filename = source_files_with_corrected[target_file]
            logging.info('Found! Evaluating `{}`'.format(original_filename))
            result.append(grade_source_code(
                    'data/{}/{}/{}'.format(assignment_name, student_id, original_filename),
                    problem, grade_config))

    return result


def grade_source_code(filename, problem, grade_config):
    """
    ソースコードを採点して、点数を返す。
    ここまできてたら多少のスペルミスはあっても何かしらのソースコードを作成しているので、1点以上はつける。
    """

    # 対応する問題をconfigから抜き出しておく
    for p in grade_config:
        if p['name'] == problem:
            problem_config = p

    # コンパイル前にdeny listの語句がソースコード内に使用されていないか確かめる
    if 'deny_list' not in problem_config:
        problem_config['deny_list'] = []
    try:
        with open(filename, 'r') as f:
            s = f.read()
            for d in problem_config['deny_list']:
                if d in s:
                    logging.warning('The source code contains the word `{}`, which is defined in the deny list. --> score = {}'.format(d, MIN_SCORE))
                    return MIN_SCORE
    except UnicodeDecodeError:
        # ちょっと強引だけど仕方ない... ごめんなさい
        logging.warning('Cannot decode the source code. --> score = {}'.format(MIN_SCORE))
        return MIN_SCORE

    # コンテナの不要ファイルを削除する
    proc = subprocess.run(f'docker exec -i {CONTAINER_NAME} bash -c "rm -f /root/*.c /root/a.out /root/*.txt"', shell=True)

    # ソースコードファイルと外部入力ファイルをコピー・コンパイルする
    basename = os.path.basename(filename)
    # `filename` にスペースが含まれている可能性があるため `;` で区切る
    proc = subprocess.run("docker;cp;{};{}:/root/{}".format(filename, CONTAINER_NAME, basename).split(';'))
    proc = subprocess.run('docker exec {} gcc /root/{} -lm -o /root/a.out'.format(CONTAINER_NAME, basename).split(' '))
    if proc.returncode != 0:
        logging.warning('Could not compile the source code. --> score = {}'.format(MIN_SCORE))
        return MIN_SCORE

    # テストケースで実行する
    # 失敗するごとに5点から1点ずつ減らしていく (ただし設定ファイルに得点が指定されていればその点を引く)
    passed, failed, penalty = 0, 0, 0
    for i, test_case in enumerate(problem_config['test_cases']):
        logging.info('--- Trying test case {} / {} ...'.format(i + 1, len(problem_config['test_cases'])))

        # 外部ファイルが指定されていればコピーする
        if 'external_files' in test_case:
            student_dir = os.path.dirname(filename)
            for external_file in test_case['external_files']:
                external_filename = '{}/../{}'.format(student_dir, external_file['source'])
                # `external_filename` にスペースが含まれている可能性があるため `;` で区切る
                proc = subprocess.run('docker;cp;{};{}:/root/{}'.format(external_filename, CONTAINER_NAME, external_file['destination']).split(';'))

        succeeded = True
        try:
            proc = subprocess.run('docker exec -i {} /root/a.out'.format(CONTAINER_NAME).split(' '),
                    encoding='UTF-8',
                    input=test_case['input'],
                    stdout=subprocess.PIPE,
                    timeout=problem_config['timeout'])
        except subprocess.TimeoutExpired as e:
            proc = subprocess.run('docker exec {} pkill -f a.out'.format(CONTAINER_NAME).split(' '))
            logging.warning(e)
            logging.warning('Execution timed out...')
            succeeded = False
        except UnicodeDecodeError as e:
            # ちょっと強引だけど仕方ない...
            # 文字コードを操作するプログラムで不正な文字変換をしてしまうとUnicode解釈できない出力が表示されることがある
            logging.warning(e)
            logging.warning('UnicodeDecodeError...')
            succeeded = False

        # a.outの実行が成功している場合のbash_test
        if succeeded and 'bash_test' in test_case:
            proc = subprocess.run('docker exec -i {} bash -c "{}"'.format(CONTAINER_NAME, test_case['bash_test']['command']),
                    encoding='UTF-8',
                    stdout=subprocess.PIPE,
                    shell=True)
            bash_output = proc.stdout
            if test_case['bash_test']['expected'] in bash_output:
                logging.info('bash_test Passed!')
                passed += 1
                continue
            logging.info('bash_test failed')

        # a.outの実行が成功した (bash_testが無い場合)
        elif succeeded:
            output = proc.stdout
            # 標準出力の1000文字までをログに出力する
            output_disp = output[:1000]
            logging.info(f'STDOUT ==>\n{"-" * 60}\n{output_disp.rstrip()}\n{"-" * 60}')
            # 実行結果が正しいケース
            match_obj = re.search(test_case['output'], output)
            if match_obj:
                logging.info('Passed!')
                passed += 1
                continue

        # 実行結果が間違っている、または実行が失敗（タイムアウト・出力文字列のデコードエラー）のケース
        logging.info('Failed (> <)')
        failed += 1
        if 'penalty' in test_case:
            penalty += test_case['penalty']
        else:
            penalty += 1

    score = 5 - penalty
    if score < MIN_SCORE:
        score = MIN_SCORE
    # スコアは小数点以下2桁までで丸める
    score = round(score, 2)
    logging.info('{} (out of {}) test cases passed. --> score = {}'.format(passed, len(problem_config['test_cases']), score))

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
        logging.warning('No files found that match the target `{}`, but `{}` is found.'.format(target, closest))
        return closest
    else:
        logging.warning('No files found that match the target `{}`.'.format(target))
        return None


if __name__ == '__main__':
    main()
