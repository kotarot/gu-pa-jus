FROM ubuntu:20.04
LABEL maintainer="Kotaro Terada <kotarot@apache.org>"

USER root
WORKDIR /root

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y \
 && apt-get install -y \
      build-essential=12.8ubuntu1 \
      iputils-ping \
      net-tools \
 && apt-get clean \
 && apt-get autoclean \
 && rm -rf /var/cache/* \
 && rm -rf /tmp/* \
 && rm -rf /var/tmp/* \
 && rm -rf /var/lib/apt/lists/*
