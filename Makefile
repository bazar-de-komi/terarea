##
## EPITECH PROJECT, 2024
## terarea
## File description:
## Makefile
##

SUDO=

all:
	$(SUDO) docker compose up

sudo:
	SUDO=sudo

down:
	$(SUDO) docker compose down

build:
	$(SUDO) docker compose build

re: down build all

.PHONY: all sudo down build re
