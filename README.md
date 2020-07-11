# :fist: :hand: :balance_scale: gu-pa-jus

:fist: (0点) か :hand: (5点) かをジャッジ :balance_scale: するオフラインジャッジシステム。

ユーザーが課題に対して作成したソースコードが正しいかどうかを、ソースコードの簡単な静的チェックやテストケースでの動作確認を通して判定する。

**現在対応している言語:**

- `C` (gcc (Ubuntu 9.3.0-10ubuntu2) 9.3.0)


## 動作確認環境

- Docker Desktop Community 2.3.0.3
- Python 3.8.3


## Docker Hub

https://hub.docker.com/r/kotarot/gu-pa-jus


## 実行方法

### ソースコード実行環境: 環境セットアップ Docker コマンド

See: [Docker_Commands.md](/Docker_Commands.md)

コンテナを起動しておく。

### ローカル環境: Snakemake セットアップ

pyenv, virtualenv をセットアップし、Python をインストールしておく。

仮想環境と [Snakemake](https://github.com/snakemake/snakemake) のセットアップ:
```
$ pyenv virtualenv 3.8.3 gu-pa-jus
$ pyenv local 3.8.3/envs/gu-pa-jus
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

pygraphvizだけインストール方法が特殊......
```
brew install graphviz
pip install --install-option="--include-path=/usr/local/include/" --install-option="--library-path=/usr/local/lib/" pygraphviz==1.5
```

確認:
```
$ snakemake --version
5.20.1
```

### ソースコードのセットアップ

`data/<課題ID>` のディレクトリに、学籍番号ごとにディレクトリを切ってソースコードを配置する。

サンプルとして `data/sample/<学籍番号>` にサンプルデータを用意している。
テーマは三角形の面積を計算するプログラム `area.c` と、円の面積を計算するプログラム `circle.c` (`math.h` を使用)。

- `1Z000001`: `area.c` と `circle.c` はともに正解のソースコード。
- `1Z000002`: `area.c` はコンパイルできるが、答えが違う。
- `1Z000003`: `area.c` はシンタックスエラーでコンパイルできない。
- `1Z000004`: `area.c` のファイル名を間違えている (`areb.c`)。※単なるミスの可能性があるので後で手動で確認する。
- `1Z000005`: `area.c` で使用禁止語句 (課題ごとにカスタマイズ定義できるがここでは `system` という語句を指定しているとする) を使用している。※意図しない検出の可能性もあるので後で手動で確認する。
- `1Z000006`: `area.c` の実行時間が長い (課題ごとにタイムアウト値をカスタマイズ定義できるが、ここでは30秒をタイムアウト値として設定しているとして35秒間実行する)。

※ `1Z000002` 以降は `circle.c` が存在しない。解けなかったという状況を仮定。

### 採点基準のセットアップ

TODO

### 採点実行

シングルコアで実行:
```
snakemake --cores 1
```

HTMLレポート出力:
```
snakemake --report report.html
```


## Future work

### ファイル名のミスに対応

今はファイル名が指定の名前と一字一句合っていないと採点対象にならないが、レーベンシュタイン距離を用いて最も近いファイル名で採点したい。

### 多言語対応

C++ や Java 等の言語にも対応する。

### セキュア化 (サンドボックス化)

今はどちらかというと実行環境を整備するためにDockerを使用している。Dockerはホストとカーネルを共有するのでゲスト環境でアプリケーションを完全には安全に実行できない問題がある。
Googleが開発したコンテナをサンドボックス化するランタイム [gVisor](https://github.com/google/gvisor) を使用すればこのセキュリティの問題が解決しそうだが、今のところLinuxのみサポートしている（Macで使えない）。
回避方法としては、VM (例えば VirtualBox + Vagrant) を利用する方法が考えられる。
