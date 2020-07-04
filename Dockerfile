FROM ubuntu:20.04

RUN apt update && \
    apt upgrade && \
    apt install -y build-essential=12.8ubuntu1
