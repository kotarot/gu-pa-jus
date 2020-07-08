# :fist: :hand: :balance_scale: gu-pa-jus

Dockerはホストとカーネルを共有するのでゲスト環境でアプリケーションを完全には安全に実行できない問題がある。
Googleが開発したコンテナをサンドボックス化するランタイム [gVisor](https://github.com/google/gvisor) を使用すればこのセキュリティの問題が解決しそうだが、今のところLinuxのみサポートしている（Macで使えない）。

今はひとまず、VM (おそらく VirtualBox + Vagrant) を利用する。


## Docker Hub

https://hub.docker.com/r/kotarot/gu-pa-jus


## コマンド

イメージビルド
```
docker build -t gu-pa-jus .
```

起動
```
docker run -d -it --name my-gu-pa-jus gu-pa-jus
```

シェルに入る
```
docker exec -it my-gu-pa-jus /bin/bash
```

ファイルコピー
```
docker cp sample/sample.c my-gu-pa-jus:/root/sample.c
```

コマンド実行
```
docker exec -it my-gu-pa-jus hostname
docker exec -it my-gu-pa-jus cat /etc/lsb-release
docker exec -it my-gu-pa-jus gcc --version
docker exec -it my-gu-pa-jus ls -la /root
docker exec -it my-gu-pa-jus gcc /root/sample.c -o /root/a.out
docker exec -i my-gu-pa-jus /root/a.out < sample/sample_input_1.txt
```

一覧
```
docker ps
docker ps -a
```

停止
```
docker stop <コンテナID>
docker stop my-gu-pa-jus
```

コンテナ削除
```
docker rm <コンテナID>
docker rm my-gu-pa-jus
```
