#!/bin/bash

hugo

# Resize images
sips --resampleHeight 800 docs/header/*
sips --resampleHeight 400 docs/img/logo.png
sips --resampleHeight 140 docs/img/partner/*

# Optimize images
/Applications/ImageOptim.app/Contents/MacOS/ImageOptim docs
