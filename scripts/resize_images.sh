#!/bin/bash

mogrify -monitor -resize x800 public/header/*
mogrify -monitor -resize x400 public/img/logo.png
mogrify -monitor -resize x140 public/img/partner/*
