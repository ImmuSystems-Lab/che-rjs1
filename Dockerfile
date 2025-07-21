FROM ubuntu:24.04
LABEL org.opencontainers.image.ref.name=ubuntu-server
LABEL org.opencontainers.image.version=24.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y ubuntu-server
