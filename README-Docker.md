# Docker Commands

Dockerfileからイメージをビルド
```bash
docker build -t gu-pa-jus .
# (or キャッシュ使用しないでビルドするなら)
docker build -t gu-pa-jus . --no-cache=true
```

コンテナ起動
```bash
docker run -d -it --name my-gu-pa-jus gu-pa-jus
```

シェルに入る
```bash
docker exec -it my-gu-pa-jus /bin/bash
```

ファイルコピー
```bash
docker cp data/sample.c my-gu-pa-jus:/root/sample.c
```

コマンド実行
```bash
docker exec -it my-gu-pa-jus hostname
docker exec -it my-gu-pa-jus cat /etc/lsb-release
docker exec -it my-gu-pa-jus gcc --version
docker exec -it my-gu-pa-jus ls -la /root
docker exec -it my-gu-pa-jus gcc /root/sample.c -o /root/a.out
docker exec -i my-gu-pa-jus /root/a.out < data/sample_input_1.txt
```

一覧
```bash
docker ps
docker ps -a
```

コンテナ停止
```bash
docker stop <コンテナID>
docker stop my-gu-pa-jus
```

コンテナ削除
```bash
docker rm <コンテナID>
docker rm my-gu-pa-jus
```

## Docker Hub を用いる場合 (pull/push)

Docker Hubからlatestを取ってくる場合
```bash
docker pull kotarot/gu-pa-jus
```

Docker Hubにイメージを手動push
```bash
docker login
docker image ls
docker tag <image id> kotarot/gu-pa-jus:latest
docker push kotarot/gu-pa-jus:latest
```

コンテナ起動
```bash
docker run -d -it --name my-gu-pa-jus kotarot/gu-pa-jus
```
