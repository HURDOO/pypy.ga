# 설치

* 주의: Azure VM을 사용할 때, `sudo reboot` 대신 Azure Portal의 '다시 시작' 기능을 사용하세요.

## Django 구동

1. 파이썬 및 pip 설치 (Python >= 3.9)
```
sudo apt install python3.9
sudo apt install pip
```

2. git clone
```shell
git clone https://github.com/HURDOO/pypy.ga
cd pypy.ga
```

3. 가상 환경 생성
```shell
sudo apt install python3.9-venv
python3.9 -m venv .venv
. .venv/bin/activate
```

4. 의존 모듈 설치
```shell
pip install -r requirements.txt
```
> 중간에 오류나는 건 신경 안써도 된다. 설치만 잘 끝나면 된다.
> 
> 만약 끝부분이 오류로 끝났다면, 아래 링크 및 코드 참조
> https://stackoverflow.com/questions/74981558/error-updating-python3-pip-attributeerror-module-lib-has-no-attribute-openss
> ```shell
> deactivate
> rm -r .venv
> python3.9 -m venv .venv
> . .venv/bin/activate
> pip install cryptography==38.0.4
> pip install -r requirements.txt
> ```

5. settings.py 작성
```shell
cp settings-example.yml settings.yml
nano settings.yml
```
내용 수정 후 'Ctrl+X → Y → Enter' 로 저장

6. DB 변경사항 적용 (migrate)
```shell
python3.9 manage.py migrate
```

7. 정적 파일 모으기 (static)
```shell
python3.9 manage.py collectstatic
```

8. 서버 실행
```shell
python3.9 manage.py runserver
```
서버 주소는 127.0.0.1:8000 (서버 연 컴퓨터에서만 접속 가능)

외부 접속 허용하려면 명령어 뒤에 `0.0.0.0:포트` 를 붙인다. Unix 계열에서는 1024 이하의 포트를 사용하려면 sudo 권한 필요.

서버 닫을 땐 Ctrl+C

## 채점 가상환경 설정 (docker)
1. docker 설치

[공식 사이트(Ubuntu)](https://docs.docker.com/engine/install/ubuntu/)에서 권장하는 방법이다.
```shell
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

sudo usermod -aG docker $USER
```


설치가 완료된 다음에는 한번 재시작해 주자. Azure의 경우에는 아래 명령어 대신 Azure Portal에서 재시작해주는 것이 좋다.
```shell
sudo reboot
```

설치 확인
```shell
docker run hello-world
```

2. docker 자동 실행 설정
```shell
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

3. 이미지 빌드
```shell
docker build -t pypyga ~/pypy.ga/runner/docker_dir
```

## 제출 페이지의 실시간 결과 설정 (redis)

1. redis 설치
```shell
sudo apt install redis-server
```

2. daphne 테스트
```shell
~/pypy.ga/.venv/bin/daphne -b 0.0.0.0 -p 8001 pypyga.asgi:application
```
실행 후 접속이 되는지 확인한다. (외부 접속 가능, 서버주소:8001 로 접속)

접속 테스트가 완료되면 Ctrl+C를 눌러 테스트를 종료한다. (간혹 종료가 되지 않는 경우, ssh 창을 닫았다 다시 열자.)

3. daphne 자동 실행 설정
```shell
sudo nano /etc/systemd/system/daphne.service
```
아래 내용을 작성한다.

```
[Unit]
Description=daphne daemon
After=network.target

[Service]
User=hurdoo
Group=hurdoo
WorkingDirectory=/home/hurdoo/pypy.ga
ExecStart=/home/hurdoo/pypy.ga/.venv/bin/daphne \
        -b 0.0.0.0 \
        -p 8001 \
        pypyga.asgi:application

[Install]
WantedBy=multi-user.target
```
6,7,8,9번째 줄의 `hurdoo` 부분을 우분투 계정 이름으로 변경한다.

작성이 끝나면 'Ctrl+X → Y → Enter' 로 저장.

아래 명령어로 daphne을 자동 실행하도록 실행한다.

```shell
sudo systemctl daemon-reload
sudo systemctl start daphne
sudo systemctl enable daphne
```

작동이 완료되었는지는 아래 명령어로 알아볼 수 있다.

```shell
systemctl status daphne
```
Ctrl+C를 한두번 누르면 로그에서 나올 수 있다.

## 웹서버 설정 (nginx)

1. nginx 설치

```shell
sudo apt install nginx
```

2. nginx에 daphne 등록하기

```shell
sudo nano /etc/nginx/sites-available/pypyga
```

아래 내용을 작성한다.

```
server {
    listen 80;
    server_name pypy.ga;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

`pypy.ga` 부분에 서버 주소를 적는다.

작성이 끝나면 'Ctrl+X → Y → Enter' 로 저장.

아래 명령어로 사이트를 등록한다.

```shell
sudo ln -s /etc/nginx/sites-available/pypyga /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

이제 서버 주소로 접속하면 된다.


## SSL(https) 설정
[공식 가이드(https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal)]에 따름
1. certbot 설치
```shell
sudo snap install core
sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

2. certbot 실행
```shell
sudo certbot --nginx
```
이후 절차에 따른다


## 그 이후
프로젝트 변경 사항 업데이트:
```shell
cd ~/pypy.ga
git pull
. .venv/bin/activate
python3.9 manage.py migrate
python3.9 manage.py collectstatic
deactivate
docker build -t pypyga ~/pypy.ga/runner/docker_dir
sudo systemctl restart nginx
sudo systemctl restart daphne
```

추후 사이트에 변경 사항이 생겨 재시작할 때에는 다음 명령어를 사용한다.
```shell
sudo systemctl restart nginx
sudo systemctl restart daphne
```
재시작에 약간 시간이 걸리는데, 기다리면 된다.
daphne의 경우 1분을 넘어가면 Ctrl+C를 눌러 취소하고 nginx부터 다시 재시작해주자.

서버 로그 보기
```shell
systemctl status gunicorn
```

refresh.sh
```shell
git pull
.venv/bin/python3.9 manage.py migrate
.venv/bin/python3.9 manage.py collectstatic --noinput
sudo systemctl restart daphne
```
