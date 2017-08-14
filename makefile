SHELL := /bin/bash

all:

production:

watch-sass:
	sass --watch assets/scss/master.scss:assets/css/main.css 

render-jade:
	jade -P -o ./ --watch assets/jade/index.jade


render-jade:


