"""
scripts/grade.py の純粋関数に対する最小限のユニットテスト。
Levenshtein / PyYAML など、Python 3.13対応でバージョンを上げたライブラリの
挙動に変化がないことを確認する。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import grade  # noqa: E402


def test_get_problems():
    grade_config = [
        {'name': 'area.c'},
        {'name': 'circle.c'},
    ]
    assert grade.get_problems(grade_config) == ['area.c', 'circle.c']


def test_get_closest_exact_match():
    assert grade.get_closest('area.c', ['area.c', 'circle.c']) == 'area.c'


def test_get_closest_within_accept_distance():
    # 1文字違い ("areb.c") は許容範囲 (デフォルト accept_distance=3) なのでマッチする
    assert grade.get_closest('area.c', ['areb.c', 'circle.c']) == 'areb.c'


def test_get_closest_no_match():
    # 距離が離れすぎている場合は None を返す
    assert grade.get_closest('area.c', ['completely_unrelated.c']) is None
