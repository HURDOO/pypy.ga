# 설치

1. 파이썬 및 pip 설치
```
sudo apt install python3
sudo apt install pip
```

2. git clone
```shell
git clone https://github.com/HURDOO/python-trainer
cd python-trainer
```

3. 가상 환경 생성
```shell
sudo apt install python3-venv
python3 -m venv .venv
. .venv/bin/activate
```

4. 의존 모듈 설치
```shell
pip install -r requirements.txt
```
5. settings.py 작성
```shell
cp settings-example.yml settings.yml
nano settings.yml
```
내용 수정 후 'Ctrl+X → Y → Enter' 로 저장

6. DB 변경사항 적용 (migrate)
```shell
python3 manage.py migrate
```

7. 서버 실행
```shell
python3 manage.py runserver
```
서버 주소는 127.0.0.1:8000 (서버 연 컴퓨터에서만 접속 가능)

외부 접속 허용하려면 명령어 뒤에 `0.0.0.0:포트` 를 붙인다. Unix 계열에서는 1024 이하의 포트를 사용하려면 sudo 권한 필요.

서버 닫을 땐 Ctrl+C

## 채점 서버 설정
1. .tmp 폴더 생성
```shell
mkdir .tmp
```

2. docker 설치

[공식 사이트(Ubuntu)](https://docs.docker.com/engine/install/ubuntu/)에서 권장하는 방법이다.
```shell
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

sudo apt install uidmap
dockerd-rootless-setuptool.sh install
export PATH=/usr/bin:$PATH
export DOCKER_HOST=unix:///run/user/1000/docker.sock
sudo usermod -aG docker $USER
```

설치 확인
```shell
docker run hello-world
```

설치가 완료된 다음에는 한번 재시작해 주자. Azure의 경우에는 아래 명령어 대신 Azure Portal에서 재시작해주는 것이 좋다.
```shell
sudo reboot
```

3. docker 자동 실행 설정
```shell
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

4. 이미지 빌드
```shell
docker build -t test1234 ~/pyton-trainer/runner/docker_dir
```

## gunicorn + nginx

Unix 계열에선 기본 포트인 80, 443 포트로 서비스하려면 sudo 권한으로 실행해야 한다. 보안 상 안전하지 않기에, gunicorn + nginx를 추가로 사용한다.

1. gunicorn 작동 테스트
```shell
gunicorn --bind 0.0.0.0:8000 pypyga.wsgi:application
```
외부 접속이 허용된 상태로 8000번 포트에서 열린다.

서버 닫을 땐 Ctrl+C

작동이 잘 된다면 이제 가상 환경을 나와도 된다.
```shell
deactivate
```

2. gunicorn 자동 시작 설정
```shell
sudo nano /etc/systemd/system/gunicorn.socket
```
아래 내용을 작성한다
```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock
# Our service won't need permissions for the socket, since it
# inherits the file descriptor by socket activation
# only the nginx daemon will need access to the socket
SocketUser=YOUR_USERNAME
# Optionally restrict the socket permissions even more.
# SocketMode=600

[Install]
WantedBy=sockets.target
```
`YOUR_USERNAME` 부분을 유저 이름으로 변경한다.

작성이 끝나면 'Ctrl+X → Y → Enter' 로 저장.

```shell
sudo nano /etc/systemd/system/gunicorn.service
```

아래 내용을 작성한다

```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=YOUR_USERNAME
Group=YOUR_USERNAME
WorkingDirectory=/home/hurdoo/python-trainer
ExecStart=/home/hurdoo/python-trainer/.venv/bin/gunicorn \
        --workers 3 \
        --bind unix:/run/gunicorn.sock \
        pypyga.wsgi:application

[Install]
WantedBy=multi-user.target
```
`YOUR_USERNAME` 부분을 유저 이름으로 변경한다.

작성이 끝나면 'Ctrl+X → Y → Enter' 로 저장.

아래 명령어로 gunicorn을 실행한다.

```shell
sudo systemctl daemon-reload
sudo systemctl start gunicorn.socket
sudo systemctl start gunicorn.service
sudo systemctl enable gunicorn.socket
sudo systemctl enable gunicorn.service
```

작동이 완료되었는지는 아래 명령어로 알아볼 수 있다.

```shell
systemctl status gunicorn.socket
systemctl status gunicorn.socket
```
Ctrl+C를 한두번 누르면 로그에서 나올 수 있다.

3. nginx 설치

```shell
sudo apt install nginx
```

4. nginx에 gunicorn 등록하기

```shell
sudo nano /etc/nginx/sites-available/pypyga
```

아래 내용을 작성한다.

```
server {
    listen 80;
    server_name IP_ADDRESS;

    location / {
        include proxy_params;
        proxy_pass unix:/run/gunicorn.sock;

    }
}
```

`IP_ADDRESS` 부분에 서버 주소를 적는다.

작성이 끝나면 'Ctrl+X → Y → Enter' 로 저장.

아래 명령어로 사이트를 등록한다.

```shell
sudo ln -s /etc/nginx/sites-available/django_test /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

4. 그 이후
업데이트 할 때:
```shell
cd ~/python-trainer
git pull
```

추후 사이트에 변경 사항이 생겨 재시작할 때에는 다음 명령어를 사용한다.
```shell
sudo systemctl restart gunicorn
```

서버 로그 보기
```shell
systemctl status gunicorn
```
