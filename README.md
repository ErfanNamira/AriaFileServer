# AriaFileServer 🪄
🌟 Simple Python+Flask HTTP/HTTPS File Server with Authentication

## How to run ❓
🧩 Modify the username and password fields within the users dictionary in AriaFileServerHTTP/S.py.
### ⭐ HTTP Version
✨ http://IP:Port
```
cd /path/to/files
wget https://raw.githubusercontent.com/ErfanNamira/AriaFileServer/main/AriaFileServerHTTP.py
sudo apt install python3-pip
pip3 install flask
python3 AriaFileServerHTTP.py
```
### ⭐ HTTPS Version
✨ https://sub.domain.com:Port
⚠️ Please note that the port specified in https://sub.domain.com:Port is set in AriaFileServerHTTPS.py and not in the NGINX configuration.
```
cd /path/to/files
wget https://raw.githubusercontent.com/ErfanNamira/AriaFileServer/main/AriaFileServerHTTPS.py
sudo apt install certbot python3-pip python3-certbot-nginx
pip3 install flask
sudo certbot --nginx -d sub.domain.com
sudo ufw allow 443/tcp
sudo python3 AriaFileServerHTTPS.py
```
### NGINX conf 🧬
```
sudo nano /etc/nginx/sites-available/default
sudo systemctl reload nginx
```
Sample NGINX Configuration 🎡
```
server {
    listen 80;
    server_name sub.example.com www.sub.example.com;

    # Redirect HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name sub.example.com www.sub.example.com;

    ssl_certificate /path/to/your/certificate/fullchain.pem;
    ssl_certificate_key /path/to/your/certificate/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;
    ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';

    # Enable HSTS for added security (optional but recommended)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Security Headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options SAMEORIGIN;
    add_header X-XSS-Protection "1; mode=block";

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /path/to/your/certificate/chain.pem;
    resolver 8.8.8.8;

    location / {
        # Your application settings
        # ...
    }
}
```
## Buy Me a Coffee ☕❤️
```
Tron USDT (TRC20): TMrJHiTnE6wMqHarp2SxVEmJfKXBoTSnZ4
LiteCoin (LTC): ltc1qwhd8jpwumg5uywgv028h3lnsck8mjxhxnp4rja
BTC: bc1q2tjjyg60hhsuyauha6uptgrwm32sarhmjlwvae
```
