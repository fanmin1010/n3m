#!/usr/bin/env bash
echo $(pwd)
cp ./bin/hooks/post-merge .git/hooks/
chmod +x .git/hooks/post-merge
