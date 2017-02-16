dev:
	hugo server --watch --buildDrafts

deploy:
	hugo
	./scripts/resize_images.sh
	bundle exec image_optim -r --cache-dir tmp/image_cache docs
