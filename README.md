# :fist: :hand: :balance_scale: gu-pa-jus

:fist: (0点) か :hand: (5点) かをジャッジ :balance_scale: するオフラインジャッジシステム。

ユーザーが課題に対して作成したソースコードが正しいかどうかを、ソースコードの簡単な静的チェックやテストケースでの動作確認を通して判定する。

**現在対応している言語:**

- `C` (gcc (Ubuntu 9.3.0-10ubuntu2) 9.3.0)


## 動作確認環境

- Docker Desktop Community 2.3.0.3


## Docker Hub

https://hub.docker.com/r/kotarot/gu-pa-jus


## 実行方法

### Docker コマンド

[Docker_Commands.md](/Docker_Commands.md)

### ソースコードのセットアップ

TODO

### 採点基準のセットアップ

TODO

### 採点実行

TODO


## Future work

### 多言語対応

C++ や Java 等の言語にも対応する。

### セキュア化 (サンドボックス化)

今はどちらかというと実行環境を整備するためにDockerを使用している。Dockerはホストとカーネルを共有するのでゲスト環境でアプリケーションを完全には安全に実行できない問題がある。
Googleが開発したコンテナをサンドボックス化するランタイム [gVisor](https://github.com/google/gvisor) を使用すればこのセキュリティの問題が解決しそうだが、今のところLinuxのみサポートしている（Macで使えない）。
回避方法としては、VM (例えば VirtualBox + Vagrant) を利用する方法が考えられる。
