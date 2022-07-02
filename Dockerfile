FROM ubuntu:22.10
LABEL maintainer="Kotaro Terada <kotarot@apache.org>"

USER root
WORKDIR /root

ENV DEBIAN_FRONTEND noninteractive

RUN apt update -y \
 && apt install -y \
      build-essential=12.9ubuntu3 \
      iputils-ping \
      net-tools \
 && apt clean \
 && apt autoclean \
 && rm -rf /var/cache/* \
 && rm -rf /tmp/* \
 && rm -rf /var/tmp/* \
 && rm -rf /var/lib/apt/lists/*
