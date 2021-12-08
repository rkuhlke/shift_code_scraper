repo = "prod-boderlands-shift_code_scraper-ecr-repo"
version = "latest"

build:
	docker build -f Dockerfile -t ${repo}:${version} .

del:
	docker system prine -a --volumes -f

deploy:
	make del
	make build
	./utilities/bin/publishecr.sh