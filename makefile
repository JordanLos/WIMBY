SHELL := /bin/bash

all:


watch-sass:
	sass --watch assets/scss/master.scss:assets/css/main.css 

render-jade:
	jade -P -o ./ --watch assets/jade/index.jade

start-browser-sync:
	browser-sync start --server --files "assets/js/*.js, assets/css/*.css, index.html"

dev:
	make watch-sass render-jade start-browser-sync -j

production:
