sms_alert
==========

Following along the tutorial from
https://www.twilio.com/docs/tutorials/walkthrough/server-notifications/python/django

And combining it with the tuturial from
https://docs.djangoproject.com/en/1.9/intro/tutorial01/

Will integrate the two tutorials to send an SMS to the site admin when an exception in the application occurs.

# Setup

## Python virtual env 

```
pyvenv-3.5 .venv-sms_alert
source .venv-sms_alert/bin/activate
pip install -r requirements.txt
```

## /etc/systemd/system/sms_alert.service 
```
[Unit]
Description=uWSGI instance to serve sms_alert

[Service]
ExecStartPre=-/usr/bin/bash -c 'mkdir -p /run/sms_alert; chown davek:nginx /run/sms_alert'
ExecStart=/usr/bin/bash -c 'cd /opt/twillio/sms_alert; source .venv-sms_alert/bin/activate; uwsgi --ini uwsgi.ini'

[Install]
WantedBy=multi-user.target
```


## nginx conf.d/sms_alert.conf

```
server {
    listen 80;
    server_name 192.169.1.1;

    location /polls/ {
        include uwsgi_params;
        uwsgi_pass unix:/run/sms_alert/sms_alert.sock;
    }
}
server {
    listen 443 ssl spdy;
    server_name 192.169.1.1;
    ssl on;
    ssl_certificate /etc/pki/tls/certs/server.crt;
    ssl_certificate_key /etc/pki/tls/certs/server.key;
    ssl_prefer_server_ciphers On;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+3DES:!aNULL:!MD5:!DSS;

    location /polls/ {
        include uwsgi_params;
        uwsgi_pass unix:/run/sms_alert/sms_alert.sock;
    }
}
```
