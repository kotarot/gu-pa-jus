FROM ubuntu:24.04
LABEL maintainer="Kotaro Terada <kotarot@apache.org>"

USER root
WORKDIR /root

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y \
  && apt install -y \
    gcc-13 \
    iputils-ping \
    net-tools \
  && apt clean \
  && apt autoclean \
  && rm -rf /var/cache/* \
  && rm -rf /tmp/* \
  && rm -rf /var/tmp/* \
  && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/gcc-13 /usr/bin/gcc \
  && ln -s /usr/bin/gcc-13 /usr/bin/cc \
  && ln -s /usr/bin/gcc-13 /usr/bin/g++
