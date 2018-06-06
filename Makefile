dev:
	hugo server --watch --buildDrafts

deploy:
	hugo
	scripts/gallery.py
	scripts/resize_images.sh
	scripts/optimize_images.sh
