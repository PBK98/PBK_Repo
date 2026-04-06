# PBK_Repo
PBK's Repository

<!--
1. 프로젝트 개요(미션 목표 요약)
    절대 경로와 상대 경로의 차이를 예시를 들어 설명할 수 있다.

    파일 권한의 의미(r/w/x)와 755, 644 같은 표기가 어떤 규칙으로 해석되는지 설명할 수 있다.

    기존 Dockerfile을 기반으로 “커스텀 이미지”를 만들 수 있다.

    포트 매핑이 필요한 이유를 설명할 수 있다.

    Docker 볼륨(영속 데이터)을 설명할 수 있다.

    Git과 GitHub의 역할 차이(로컬 버전관리 vs 원격 협업 플랫폼)를 설명할 수 있다.

2. 실행 환경
    docker : MAC
    git : MAC
    linux 명령어 : Ubuntu

3. 수행 항목 체크리스트(터미널/권한/Docker/Dockerfile/포트/볼륨/Git//GitHub)
    1. 터미널 o 
    2. 권한 o
    3. Docker o
    4. Dockerfile o
    5. 포트 o
    6. 볼륨 o
    7. Git o
    8. GitHub o

4. 검증 방법
    1. 터미널 : ./TerminalLog.txt 참조
    2. 권한 : ./TerminalLog.txt 참조
    3. Docker : ./DockerLog.txt 참조
    4. Dockerfile : /Users/bumkyu84259392/PBK_Repo/Step1.1/LinuxServer
                    /Users/bumkyu84259392/PBK_Repo/Step1.1/WebServer 참조
    5. 포트 : ./DockerLog.txt 참조
    6. 볼륨 : ./DockerLog.txt 참조
    7. Git : ./GitLog.txt 참조
    8. GitHub : ./GitLog.txt 참조

5. 트러블슈팅 2건 이상(문제 -> 원인 가설 -> 확인 -> 해결/대안)

    1. WebServer(nginx.server) 실행 시 동작이 유지 되지않고 즉시 종료되는 문제 발생
        - daemon off 미적용 혹은 포트 문제로 예상
        - 확인 결과 포트는 이상 없으나 daemon off가 Dockerfile과 nginx.conf에 중복으로 선언되어 충돌이 발생, 결과는 미적용
        - nginx.conf에 있는 daemon off 선언 부분을 수정
        - 수정 후 컨테이너 재생성하니 정상 작동
        - 대안 : Dockerfile 과 nginx.conf 에 중복선언만 피하면 되기 때문에 상황에 따라 Dockerfile을 수정하고 nginx.conf에 선언 가능. (Dockerfile은 기반 컨테이너에 모두 적용해야할 시, nginx.conf는 같은 Dockerfile기반이지만 daemon off는 특정 컨테이너만 사용해야 할 시에 사용)

    2. WebServer에서 Https 적용 했으나 접속이 불가한 문제 발생
        - Dockerfile에 443 포트 적용 했으나 Https 접속 불가한 문제 발생
        - 포트 충돌으로 예상했으나 학습 후 Https는 보안 프로토콜이기 때문에 인증서 발급이 필요한 것을 확인
        - Https는 필수 수행항목이 아니며, 해당 과제에서는 보안이 필요한 정보가 포함되지 않기 때문에 (DB, admin 등) 우선 제외하고 실행함
        - Https 제외 후 정상 작동
        - 추후 인증서 발급 후 재적용
         
* 기술 문서만 읽어도 전체 수행 내용을 파악할 수 있어야 한다.
-->

<!-- Container 별 베이스 이미지
    
    Web Server -> nginx:1.27.0

    Linux Server -> Ubuntu:22.04

-->