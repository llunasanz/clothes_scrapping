build:
	docker build -t scrapper_img .

up:
	docker run -t -d \
	-p 127.0.0.1:34617:34617/tcp \
	--name scrapper_cont \
	scrapper_img

down:
	docker stop scrapper_cont

rm_cont:
	docker rm scrapper_cont

rm_img:
	docker image rm scrapper_img

rm_all:
	make rm_cont
	make rm_img

stop_rm_all:
	make down
	make rm_all

rebuild:
	make rm_all
	make build
