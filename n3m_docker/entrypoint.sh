#!/bin/bash

sudo service postgresql start &
cd /home/n3m/git
if [ ! -d "./n3m" ]; then
  source /home/n3m/.bashrc
  mkdir /home/n3m/.vimundo
  sudo npm cache clean -f
  sudo npm install -g n
  sudo n stable
  sudo npm install npm -g
  git clone https://github.com/team-n3m/n3m.git
  cd n3m
  virtualenv venv
  . venv/bin/activate 
  pip install -r requirements.txt
  sudo -H -u postgres bash -c "createuser -r -s -d --replication n3m"
  createdb n3mdb
  python manage.py create_db
  python manage.py db upgrade
  python manage.py db migrate 
  cd static
  npm install
  cd ../
  sh bin/install_phantomjs.sh
else
  cd n3m
  . venv/bin/activate 
fi

exec $@

