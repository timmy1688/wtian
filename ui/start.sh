#!/bin/bash
[ ! -d "node_modules" ] && npm install --registry=https://registry.npmmirror.com
npm run serve

