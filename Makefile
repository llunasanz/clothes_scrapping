# Setup
build:
	docker build -t scrapper_img .

up:
	docker run -t -d \
	-p 127.0.0.1:34617:34617/tcp \
	--name scrapper_cont \
	scrapper_img

build_up:
	make build
	make up

build_up_no_cache:
	docker build --no-cache -t scrapper_img .
	make up


# Run
run:
	docker exec -it scrapper_cont python3 scrapper/scrap.py $(url)

run_example_manual:
	@read -p "Enter URL: " url; \
	docker exec -it scrapper_cont python3 scrapper/scrap.py $$url

run_example_auto:
	# Call the category page and use the first item (if exists) as input for make run
	url=$$(docker exec -it scrapper_cont python3 src/test/get_link_first_product.py | tr -d '\r'); \
	if [ "$$url" != "No products found" ]; then \
		make run url="$$url"; \
	else \
		echo "No products found"; \
	fi

run_example:
	# Juat to make this example more generic, it will be suitable to call to a category page and run the example with the first item (if exists)
	docker exec -it scrapper_cont python3 scrapper/scrap.py "https://en.gb.scalperscompany.com/products/bbcstudio24-44361-fill-ruffle-skirt-ss24-lilac"

run_tests:
	docker exec -it scrapper_cont python3 -m unittest discover -s tests

run_tests_no_docker:
	python3 -m unittest discover -s tests



# Down and remove
stop:
	docker stop scrapper_cont

rm_cont:
	docker rm scrapper_cont

rm_img:
	docker image rm scrapper_img

rm_all:
	make rm_cont
	make rm_img

stop_rm_all:
	make stop
	make rm_all

rebuild:
	make rm_all
	make build
