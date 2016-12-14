#!/bin/bash

mogrify -verbose -resize x800 docs/header/*
mogrify -verbose -resize x400 docs/img/logo.png
mogrify -verbose -resize x140 docs/img/partner/*
