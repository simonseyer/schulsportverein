dev:
	hugo server --watch --buildDrafts --config config.toml,development.toml

deploy:
	hugo
	scripts/gallery.py
	scripts/resize_images.sh
	scripts/optimize_images.sh
