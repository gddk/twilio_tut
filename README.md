twilio-tut
==========

Practice files learning twilio.

# Setup

This was done on centos-7. Adapt for your OS.

## Get python3.5
```
wget -O ius.sh https://setup.ius.io/
/bin/bash ius.sh
sudo yum install -y python35u python35u-pip python35u-devel
```

## Install gcc
```
sudo yum install -y gcc
```

## Setup dir
Replace davek with your user:
```
cd /opt
sudo mkdir twillio
sudo chown davek: twillio
git clone git@github.com:gddk/twilio_tut.git twillio || \
    git clone https://github.com/gddk/twilio_tut.git twillio
```

## Setup virtual-environtment
```
cd /opt/twillio
pyvenv-3.5 .venv-twillio
source .venv-twillio/bin/activate
pip install -r app/requirements.txt
``` 

## Setup uwsgi
```
sudo -s
cat << 'EOF' > /etc/systemd/system/hello_monkey.service
[Unit]
Description=uWSGI instance to serve hello_monkey
After=network.target

[Service]
User=davek
Group=nginx
WorkingDirectory=/opt/twillio/app
Environment="PATH=/opt/twillio/.venv-twillio/bin"
ExecStart=/opt/twillio/.venv-twillio/bin/uwsgi --ini hello_monkey.ini

[Install]
WantedBy=multi-user.target
EOF
exit # sudo -s
sudo systemctl enable hello_monkey
sudo systemctl start hello_monkey
```

## Setup nginx
```
sudo yum install -y nginx
cd /etc/pki/tls/certs
sudo openssl req -newkey rsa:2048 -nodes -keyout server.key  -x509 -days 365 -out server.crt -subj '/CN=your.name.or.ip'
sudo -s
cat << 'EOF' > /etc/nginx/conf.d/hello_monkey.conf
server {
    listen 80;
    server_name 192.169.174.100;

    location /hello-monkey/ {
        include uwsgi_params;
        uwsgi_pass unix:/opt/twillio/app/hello_monkey.sock;
    }
}
server {
    listen 443 ssl spdy;
    server_name 192.169.174.100;
    ssl on;
    ssl_certificate /etc/pki/tls/certs/server.crt;
    ssl_certificate_key /etc/pki/tls/certs/server.key;
    ssl_prefer_server_ciphers On;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+3DES:!aNULL:!MD5:!DSS;

    location /hello-monkey/ {
        include uwsgi_params;
        uwsgi_pass unix:/opt/twillio/app/hello_monkey.sock;
    }
}
EOF
exit # sudo -s
sudo systemctl enable nginx
sudo systemctl start nginx
```

