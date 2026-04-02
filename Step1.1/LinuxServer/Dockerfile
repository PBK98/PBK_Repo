FROM ubuntu:22.04

# 패키지 업데이트
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 컨테이너 실행시 기본 명령어
CMD [ "/bin/bash" ]