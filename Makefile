# Χρησιμοποιούμε bash
SHELL := /bin/bash

SCRIPT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

.PHONY: all clone move clean install

all: clone move clean install

clone:
	@echo "Cloning repositories..."
	git clone https://github.com/noamgat/lm-format-enforcer.git

move:
	@echo "Moving lmformatenforcer into thesisRepo/app..."
	cp -r lm-format-enforcer/lmformatenforcer ./app/

clean:
	@echo "Cleaning up..."
	rm -rf lm-format-enforcer

install:
	@echo "Installing Python dependencies..."
	pip install --no-deps -r requirements.txt
