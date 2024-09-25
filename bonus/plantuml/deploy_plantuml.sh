#!/bin/bash
DOCKER_IMAGE=plantuml/plantuml-server
DOCKER_NAME=plantuml
sudo docker stop $DOCKER_NAME
sudo docker rm $DOCKER_NAME
sudo docker pull $DOCKER_IMAGE
sudo docker run -it -d -p 8082:8080 -v $(pwd):/usr/src/app/plantuml --name $DOCKER_NAME $DOCKER_IMAGE
