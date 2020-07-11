# Docker Commands

## Docker Hub

https://hub.docker.com/r/kotarot/gu-pa-jus

## コマンド

Docker Hub から latest を取ってくる場合
```
docker pull kotarot/gu-pa-jus
```

Dockerfile からイメージビルド
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
docker cp data/sample.c my-gu-pa-jus:/root/sample.c
```

コマンド実行
```
docker exec -it my-gu-pa-jus hostname
docker exec -it my-gu-pa-jus cat /etc/lsb-release
docker exec -it my-gu-pa-jus gcc --version
docker exec -it my-gu-pa-jus ls -la /root
docker exec -it my-gu-pa-jus gcc /root/sample.c -o /root/a.out
docker exec -i my-gu-pa-jus /root/a.out < data/sample_input_1.txt
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
