# nginx의 1.27.0 버전을 사용
FROM nginx:1.27.0

# 기존 설정 제거
RUN rm /etc/nginx/conf.d/default.conf 
# 커스텀 설정 복사
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf

# 웹 콘텐츠 복사
COPY ./html /usr/share/nginx/html

# 포트 지정(80 -> html 443 -> htmls)
EXPOSE 80 443

# 컨테이너 시작 시 기본으로 실행할 명령 지정 * daemon off -> on이 기본 설정인데, 이 경우 실행 후 즉시 종료됨
# -g의 의미 global의 g, nginx의 전체 동작에 영향을 미치는 최상위 설정
CMD [ "nginx", "-g", "daemon off;" ]