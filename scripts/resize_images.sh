#!/bin/bash

mogrify -verbose -resize x800 public/header/*
mogrify -verbose -resize x400 public/img/logo.png
mogrify -verbose -resize x140 public/img/partner/*
