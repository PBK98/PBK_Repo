FROM ubuntu:25.10

# 1. 패키지 업데이트 및 기본 도구 설치
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 2. 커스텀 사용자 생성 (보안)
RUN useradd -m -s /bin/bash appuser

# 3. 환경변수 설정
ENV APP_HOME=/app \
    PYTHONUNBUFFERED=1 \
    NODE_ENV=production

# 4. 작업 디렉토리 설정
WORKDIR $APP_HOME

# 5. 간단한 Python 앱 복사 (예시)
COPY app.py .
COPY requirements.txt .

# 6. Python 패키지 설치
RUN pip3 install --break-system-packages -r requirements.txt

# 7. 사용자 권한 변경
RUN chown -R appuser:appuser $APP_HOME
USER appuser

# 8. 헬스체크 추가
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 9. 포트 노출
EXPOSE 8000

# 10. 실행 명령
CMD ["python3", "app.py"]