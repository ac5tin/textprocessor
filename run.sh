#!/bin/sh
docker run --rm -it -p 8000:8000 -e PORT=8000 -e PARA=2 textprocessor
