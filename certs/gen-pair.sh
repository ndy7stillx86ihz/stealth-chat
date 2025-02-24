#!/bin/sh
mkdir certs && \
openssl genpkey -algorithm RSA -out server.key -aes256 && \
openssl req -new -x509 -key server.key -out server.crt -days 365