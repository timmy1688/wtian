#!/bin/sh
# Installed to /etc/letsencrypt/renewal-hooks/deploy/ by `./wtian.sh deploy-api`.
# nginx keeps the certificate it loaded at startup, so it must reload after every renewal.
docker exec wtian-nginx nginx -s reload
