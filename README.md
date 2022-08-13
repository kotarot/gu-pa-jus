# :fist: :hand: :balance_scale: gu-pa-jus

[![CI](https://github.com/kotarot/gu-pa-jus/workflows/ci/badge.svg)](https://github.com/kotarot/gu-pa-jus/actions?query=workflow%3Aci)
[![Docker Build](https://img.shields.io/docker/cloud/build/kotarot/gu-pa-jus.svg)](https://hub.docker.com/r/kotarot/gu-pa-jus/)
[![Docker Autobuild](https://img.shields.io/docker/cloud/automated/kotarot/gu-pa-jus.svg)](https://hub.docker.com/r/kotarot/gu-pa-jus/)
[![Docker Pulls](https://img.shields.io/docker/pulls/kotarot/gu-pa-jus.svg)](https://hub.docker.com/r/kotarot/gu-pa-jus/)

:fist: (0点) か :hand: (5点・満点) かをジャッジ :balance_scale: するオフラインジャッジシステム。

課題に対してユーザーが作成したソースコードが正しいかどうかを、ソースコードの簡単な静的チェック、コンパイル、テストケースでの動作確認を通して判定（採点）する。


## 動作確認済み環境

- Docker Desktop 4.11.1
- Python 3.10.4


## Docker Hub

[![dockeri.co](https://dockeri.co/image/kotarot/gu-pa-jus)](https://hub.docker.com/r/kotarot/gu-pa-jus)

https://hub.docker.com/r/kotarot/gu-pa-jus

### 現在の対応済み言語

- `C` (gcc (Ubuntu 11.3.0-5ubuntu1) 11.3.0)


## 実行方法

### 採点実行環境: 環境セットアップ Docker コマンド

See: [README-Docker.md](/README-Docker.md)

コンテナを起動しておく。

### ローカル環境: Snakemake セットアップ

pyenv, virtualenv をセットアップし、Python をインストールしておく。

仮想環境と [Snakemake](https://github.com/snakemake/snakemake) のセットアップ:
```
$ pyenv virtualenv 3.10.4 gu-pa-jus
$ pyenv local gu-pa-jus

# pygraphvizのインストールに必要
$ brew install graphviz

$ pip install --upgrade pip
$ pip install -r requirements.txt
```

確認:
```
$ snakemake --version
7.8.5
```

### ソースコードのセットアップ

`data/<課題ID>` のディレクトリに、学籍番号ごとにディレクトリを切ってソースコードを配置する。

サンプルとして `data/sample/<学籍番号>` にサンプルデータを用意している。

プログラムのテーマ:
- `area.c`: 三角形の面積を計算するプログラム
- `circle.c`: 円の面積を計算するプログラム (`math.h` を使用)
- `calc_sum.c`: 外部ファイル `numbers.txt` の各行に書かれている数字の和を計算するプログラム

架空の受講者ごとのディレクトリ:
- `1Z000001`:
  - `area.c` 正解のソースコード。
  - `circle.c` 正解のソースコード。
  - `calc_sum.c` 正解のソースコード。
- `1Z000002`:
  - `area.c` はコンパイルできるが、答えが一部のテストケースで違う。
  - `circle.c` の答えも違う。
  - `calc_sum.c` の答えも違う。
- `1Z000003`:
  - `area.c` はコンパイルできるが、答えがすべて違う。
  - `circle.c` は答えが微妙に違うけど許容範囲。
  - `calc_sun.c` (ファイル名が1文字違い) は存在しないファイルを開こうとしている。
- `1Z000004`:
  - `area.c` はシンタックスエラーでコンパイルできない。
  - `circle.c` は答えを直接書いているためだめ。※意図しない検出（誤検出）の可能性もあるので後で手動で確認する。
  - `calc_sum.c` はコンパイルは通るけど実行でセグフォる。
- `1Z000005_1` (`1Z000005` の1回目の提出を想定):
  - `area.c` のファイル名を1文字間違えている (`areb.c`)。※単なる提出者のミスの可能性があるので後で手動で確認する。
- `1Z000005_2` (`1Z000005` の2回目の提出を想定):
  - `circle.c` は正しい。
- `1Z000006`:
  - `area.c` で使用禁止語句 (課題ごとにカスタマイズ定義できるがここでは `system` という語句を指定しているとする) を使用している。※意図しない検出（誤検出）の可能性もあるので後で手動で確認する。
- `1Z000007`:
  - `area.c` の実行時間が長い (課題ごとにタイムアウト値をカスタマイズ定義できるが、ここでは10秒をタイムアウト値として設定しているとして15秒間実行する)。

※ `1Z000006` 以降は `circle.c` が存在しない。解けなかったという状況を想定している。

### 採点基準のセットアップ

`data/<課題ID>/grade.yaml` にyamlファイル (設定ファイル) を定義する。

基本採点基準:
- 提出してあれば 1点
- コンパイル通らなくても 1点
- テストケース全部通っていれば 5点
- テストケースの失敗に応じて減点 (ただし最低1点は保証する)

### 採点実行

課題を追加したときは `Snakefile` を編集して課題のジョブを追加する。
タスクランナーとして [Snakemake](https://github.com/snakemake/snakemake) を利用している。

dry-run:
```
snakemake kadai --config kadainame="sample" -n
```

サンプルをシングルコアで実行 (`-F` をつけることで出力ファイルが存在しても強制的に実行する):
```
snakemake kadai --config kadainame="sample" --cores 1 -F
```

結果のCSVファイルが `results` ディレクトリ内に生成される。

課題 (例: kadai-2022h1-03-class1) の採点をシングルコアで実行 (`-F` をつけることで出力ファイルが存在しても強制的に実行する):
```
snakemake kadai --config kadainame="kadai-2022h1-03-class1" --cores 1 -F
```

(今はあまり意味ない) HTMLレポート出力:
```
snakemake kadai --config kadainame="sample" --report results/report.html
```


## Future work

### セキュア化 (サンドボックス化)

今はどちらかというと実行環境を整備するためにDockerを使用している。Dockerはホストとカーネルを共有するのでゲスト環境でアプリケーションを完全には安全に実行できない問題がある。
Googleが開発したコンテナをサンドボックス化するランタイム [gVisor](https://github.com/google/gvisor) を使用すればこのセキュリティの問題が解決しそうだが、今のところLinuxのみサポートしている（Macで使えない）。
回避方法としては、VM (例えば VirtualBox + Vagrant) を利用する方法が考えられる。

### 多言語対応

C++ や Java 等の他の言語にも対応する。
