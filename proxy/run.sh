#!/bin/sh

set -e

#? Environment Substitute
envsubst  < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

#? Run in the foreground
nginx -g 'daemon off;'