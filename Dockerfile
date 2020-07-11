FROM ubuntu:20.04
LABEL maintainer="Kotaro Terada <kotarot@apache.org>"

USER root
WORKDIR /root

ENV DEBIAN_FRONTEND noninteractive

RUN apt update -y && \
    apt upgrade -y && \
    apt install -y \
        build-essential=12.8ubuntu1 \
        iputils-ping \
        net-tools
