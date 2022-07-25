#!/usr/bin/env bash
git submodule update --init
git submodule add -f -b master ./ public
./hugow
echo "! go to public directory and push the changes to deploy"