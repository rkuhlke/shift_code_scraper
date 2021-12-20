repo = "prod-borderlands-shift-code-scraper-ecr-repo"
version = "latest"

build:
	sudo docker build -f Dockerfile -t ${repo}:${version} .

run:
	sudo docker run ${repo}:${version}

del:
	docker system prune -a --volumes -f

deploy:
	make del
	make build
	./utilities/bin/publishecr.sh