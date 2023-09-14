# AriaFileServer 🪄
🌟 Simple Python+Flask HTTP/HTTPS File Server with Authentication

## How to run ❓
### ⭐ HTTP Version
```
cd /path/to/files
wget https://raw.githubusercontent.com/ErfanNamira/AriaFileServer/main/AriaFileServerHTTP.py
sudo apt install python3-pip
pip3 install flask
python3 AriaFileServerHTTP.py
```
### ⭐ HTTPS Version
```
cd /path/to/files
wget https://raw.githubusercontent.com/ErfanNamira/AriaFileServer/main/AriaFileServerHTTPS.py
sudo apt install certbot python3-pip python3-certbot-nginx
pip3 install flask
sudo certbot --nginx -d sub.domain.com
sudo ufw allow 443/tcp
sudo python3 AriaFileServerHTTPS.py
```
