#!/bin/bash

curl -X POST http://localhost:5000/api/timeline_post -d 'name=Mike&email=mike@gmail.com&content=Testing out my endpoints using postman and curl!'

curl http://localhost:5000/api/timeline_post