# Django 주의사항



### Secret Key 문제

프로젝트 폴더 안에 있는 settings.py 파일 안을 자세히 살펴보면 secret key가 있는 것을 알 수 있다.

secret key는 누가 봐도 중요한 것이며 외부에 공개가 되선 안된다.

그러므로 github에 secret key를 노출시키면 안된다.

(실수로 나도 그냥 푸시했다가 경고메일 날라와서 쓰는거야ㅋㅋ)



secret key를 분리하는 방법은 다음 사이트를 참고하자.

[django secret key 분리, secrets.json 생성 (tistory.com)](https://integer-ji.tistory.com/180)

