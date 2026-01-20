# Server Deployment Guide - Yellow Pages Scraper

## 🚀 Running on a Powerful Server

### Why Use a Server?

**Your laptop (current):**
- 10 concurrent searches max
- Can't run 24/7
- Limited resources
- Need to keep laptop open

**Powerful server:**
- 50-100+ concurrent searches
- Runs 24/7
- Massive resources
- Access from anywhere
- Can scrape entire country in 1-2 hours

---

## 📊 Server Specs Recommendations

### Minimum Requirements (50 concurrent)
- **CPU:** 4 cores
- **RAM:** 8GB
- **Disk:** 20GB SSD
- **OS:** Ubuntu 20.04+ or similar Linux
- **Network:** 100Mbps+

### Recommended (100 concurrent)
- **CPU:** 8-16 cores
- **RAM:** 16-32GB
- **Disk:** 50GB SSD
- **OS:** Ubuntu 22.04 LTS
- **Network:** 1Gbps

### Optimal (200+ concurrent)
- **CPU:** 16-32 cores
- **RAM:** 64GB+
- **Disk:** 100GB SSD
- **OS:** Ubuntu 22.04 LTS
- **Network:** 1Gbps+

---

## 🔧 Installation on Server

### Step 1: Connect to Server

```bash
# SSH into the server
ssh username@server-ip-address

# Or if using key authentication
ssh -i ~/.ssh/your-key.pem username@server-ip-address
```

### Step 2: Install Dependencies

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Python 3.11+
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install Playwright dependencies
sudo apt install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2

# Install Git (if not already)
sudo apt install git -y
```

### Step 3: Upload Your Scraper

**Option A: Git Clone (if you have a repo)**
```bash
cd /home/username
git clone https://github.com/yourrepo/yellow-pages-scraper.git
cd yellow-pages-scraper
```

**Option B: SCP from your laptop**
```bash
# Run this on YOUR LAPTOP (not server)
cd "/Users/jonathangarces/Desktop/yellow page scraper"

# Copy entire directory to server
scp -r . username@server-ip:/home/username/yellow-pages-scraper/
```

**Option C: Create tar and upload**
```bash
# On your laptop
cd "/Users/jonathangarces/Desktop/yellow page scraper"
tar -czf scraper.tar.gz .

# Upload
scp scraper.tar.gz username@server-ip:/home/username/

# On server
cd /home/username
mkdir yellow-pages-scraper
cd yellow-pages-scraper
tar -xzf ../scraper.tar.gz
```

### Step 4: Setup Virtual Environment

```bash
cd /home/username/yellow-pages-scraper

# Create venv
python3.11 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
playwright install-deps chromium
```

### Step 5: Upload Proxies

```bash
# Option A: Edit directly on server
nano proxies.txt

# Paste your 50-100 proxies, one per line:
# 142.111.48.253:7030:iyggsdpl:i7mocimb1hxn
# ... (paste all proxies)
# Ctrl+X, Y, Enter to save

# Option B: SCP from laptop
# On your laptop:
scp proxies.txt username@server-ip:/home/username/yellow-pages-scraper/
```

---

## 🌐 Remote Access Setup

### Enable Remote Web UI Access

**Edit web_app.py to allow remote connections:**

```bash
nano web_app.py
```

**Find the last line:**
```python
app.run(debug=True, port=5001, threaded=True)
```

**Change to:**
```python
app.run(debug=False, host='0.0.0.0', port=5001, threaded=True)
```

**Save and exit:** Ctrl+X, Y, Enter

### Open Firewall Port

```bash
# Ubuntu/Debian with UFW
sudo ufw allow 5001/tcp
sudo ufw status

# Or if using firewalld
sudo firewall-cmd --permanent --add-port=5001/tcp
sudo firewall-cmd --reload
```

### Access Web UI from Anywhere

**From your laptop browser:**
```
http://SERVER-IP-ADDRESS:5001
```

**Example:**
```
http://192.168.1.100:5001
http://your-server.com:5001
```

---

## 🔒 Security Setup (IMPORTANT!)

### Option 1: SSH Tunnel (Recommended)

**Most secure - access UI through SSH tunnel:**

```bash
# On your laptop, create SSH tunnel
ssh -L 5001:localhost:5001 username@server-ip

# Then access in browser
http://localhost:5001
```

**Benefits:**
- Encrypted connection
- No exposed port
- No authentication needed

### Option 2: Add Password Protection

**Install Flask-HTTPAuth:**
```bash
source venv/bin/activate
pip install Flask-HTTPAuth
```

**Edit web_app.py:**
```python
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("your-strong-password-here")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    return render_template('scraper.html')
```

### Option 3: Use VPN

**If server on cloud (AWS, DigitalOcean, etc.):**
- Set up VPN to server
- Keep port 5001 blocked publicly
- Access only via VPN

---

## 🏃 Running the Scraper

### Method 1: Manual Start (Testing)

```bash
cd /home/username/yellow-pages-scraper
source venv/bin/activate
python web_app.py
```

**Access:** http://server-ip:5001

**Stop:** Ctrl+C

### Method 2: Background with nohup

```bash
cd /home/username/yellow-pages-scraper
source venv/bin/activate
nohup python web_app.py > scraper.log 2>&1 &

# Check it's running
ps aux | grep web_app.py

# View logs
tail -f scraper.log

# Stop
pkill -f web_app.py
```

### Method 3: Systemd Service (Production) ⭐

**Create service file:**
```bash
sudo nano /etc/systemd/system/yellowpages-scraper.service
```

**Paste:**
```ini
[Unit]
Description=Yellow Pages Scraper Web UI
After=network.target

[Service]
Type=simple
User=username
WorkingDirectory=/home/username/yellow-pages-scraper
Environment="PATH=/home/username/yellow-pages-scraper/venv/bin"
ExecStart=/home/username/yellow-pages-scraper/venv/bin/python web_app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Replace `username` with your actual username!**

**Enable and start:**
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable (start on boot)
sudo systemctl enable yellowpages-scraper

# Start now
sudo systemctl start yellowpages-scraper

# Check status
sudo systemctl status yellowpages-scraper

# View logs
sudo journalctl -u yellowpages-scraper -f

# Stop
sudo systemctl stop yellowpages-scraper

# Restart
sudo systemctl restart yellowpages-scraper
```

**Benefits:**
- Auto-starts on server reboot
- Auto-restarts if crashes
- Easy to manage
- Proper logging

---

## ⚡ Parallel Processing on Server

### Build Parallel Mode First

I need to build the parallel processing feature. Once built, you can configure:

**For 50 concurrent searches:**
```python
CONCURRENT_SEARCHES = 50
```

**For 100 concurrent searches:**
```python
CONCURRENT_SEARCHES = 100
```

**Resource usage:**
- Each concurrent search ≈ 150-300MB RAM
- 50 concurrent ≈ 10-15GB RAM
- 100 concurrent ≈ 20-30GB RAM

### Optimal Concurrency Settings

**Based on server specs:**

| Server RAM | CPU Cores | Max Concurrent | Recommended |
|------------|-----------|----------------|-------------|
| 8GB | 4 | 30 | 20 |
| 16GB | 8 | 60 | 40 |
| 32GB | 16 | 120 | 80 |
| 64GB | 32 | 250 | 150 |

**Formula:**
```
Max Concurrent = (RAM_GB × 3) - 10
Recommended = Max Concurrent × 0.7
```

---

## 📊 Performance Expectations

### With 50 Proxies + 40 Concurrent

**Nationwide scrape:**
- 455 cities × 5 categories = 2,275 searches
- 2,275 ÷ 40 = ~57 batches
- 57 batches × 3 min = **~2.5 hours**

**Compare to laptop (sequential):**
- 2,275 × 3 min = **114 hours** (4.75 days)

**Speed improvement:** **45x faster!**

### With 100 Proxies + 80 Concurrent

**Nationwide scrape:**
- 2,275 ÷ 80 = ~28 batches
- 28 batches × 3 min = **~1.5 hours**

**Speed improvement:** **76x faster!**

---

## 📁 File Management on Server

### Where Files Save

```bash
/home/username/yellow-pages-scraper/scrape_results_*.csv
```

### Download from Server to Your Laptop

**Method 1: Web UI Download**
- Use the download button in web UI
- Downloads directly to your laptop

**Method 2: SCP**
```bash
# On your laptop
scp username@server-ip:/home/username/yellow-pages-scraper/scrape_results_*.csv ~/Downloads/
```

**Method 3: Setup Shared Folder**
```bash
# On server - install Samba
sudo apt install samba -y

# Configure shared folder
sudo nano /etc/samba/smb.conf

# Add:
[yellowpages]
    path = /home/username/yellow-pages-scraper
    browseable = yes
    read only = no
    guest ok = no

# Restart Samba
sudo systemctl restart smbd

# Access from laptop
# Mac: Finder → Go → Connect to Server
# smb://server-ip/yellowpages
```

---

## 🔄 Automated Scraping

### Option 1: Cron Job (Scheduled)

**Run every Monday at 2am:**
```bash
crontab -e
```

**Add:**
```bash
0 2 * * 1 /home/username/yellow-pages-scraper/scripts/auto_scrape.sh
```

**Create script:**
```bash
mkdir -p /home/username/yellow-pages-scraper/scripts
nano /home/username/yellow-pages-scraper/scripts/auto_scrape.sh
```

**Paste:**
```bash
#!/bin/bash
cd /home/username/yellow-pages-scraper
source venv/bin/activate

# Run scraper via API
curl -X POST http://localhost:5001/api/start-scrape \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "building supply, shutters, millwork, lumber, architects",
    "locations": "Miami FL, Chicago IL, New York NY",
    "max_pages": 10,
    "use_proxies": true
  }'
```

**Make executable:**
```bash
chmod +x /home/username/yellow-pages-scraper/scripts/auto_scrape.sh
```

### Option 2: API-Triggered

**Start scrape from anywhere via API:**
```bash
# From your laptop or another server
curl -X POST http://server-ip:5001/api/start-scrape \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "building supply, shutters",
    "locations": "Los Angeles CA, Houston TX",
    "max_pages": 10,
    "use_proxies": true
  }'
```

---

## 📈 Scaling Recommendations

### Phase 1: Initial Setup (Week 1)
```
Server: 8GB RAM, 4 cores
Proxies: 25
Concurrent: 15
Target: 50 cities, test run
Time: ~1 hour
Cost: $30/month (server + proxies)
```

### Phase 2: Production Scale (Week 2)
```
Server: 16GB RAM, 8 cores
Proxies: 50
Concurrent: 30-40
Target: 100 cities
Time: ~1.5 hours
Cost: $60-80/month
```

### Phase 3: Maximum Scale (Month 2)
```
Server: 32GB RAM, 16 cores
Proxies: 100
Concurrent: 60-80
Target: All 455 cities nationwide
Time: ~1.5 hours
Cost: $120-150/month
Result: 200K+ leads
```

---

## 💰 Server Cost Options

### Option 1: DigitalOcean Droplet
**16GB RAM, 8 CPU:**
- $96/month
- Ubuntu 22.04
- 1Gbps network
- Easy to setup

### Option 2: AWS EC2
**t3.xlarge (16GB, 4 vCPU):**
- ~$120/month
- More expensive but scalable
- Pay-as-you-go

### Option 3: Hetzner (Cheapest)
**16GB RAM, 8 CPU:**
- €40/month (~$45)
- Great specs for price
- European servers

### Option 4: Friend's Server (Free!)
**If your friend has spare capacity:**
- Cost: $0
- Just pay for proxies
- Best option if available!

---

## 🛡️ Best Practices

### 1. Monitor Resources

```bash
# Check RAM usage
free -h

# Check CPU usage
htop

# Check disk space
df -h

# Check running processes
ps aux | grep python
```

### 2. Log Everything

```bash
# View scraper logs
tail -f scraper.log

# View systemd logs
sudo journalctl -u yellowpages-scraper -f

# Save logs for analysis
cp scraper.log scraper_$(date +%Y%m%d).log
```

### 3. Backup Results

```bash
# Auto-backup to cloud
# Install rclone
curl https://rclone.org/install.sh | sudo bash

# Configure (Google Drive, Dropbox, etc.)
rclone config

# Auto-sync results
rclone sync /home/username/yellow-pages-scraper/*.csv remote:yellowpages/
```

### 4. Monitor Proxy Health

- Check web UI regularly
- If > 50% blocked, pause and buy fresh proxies
- Rotate proxy lists monthly

---

## 🎯 Recommended Server Setup

**For your use case (Cobblestone Millwork):**

### Server Specs
- **Provider:** DigitalOcean or Hetzner
- **Plan:** 16GB RAM, 8 CPU cores
- **Cost:** $45-96/month
- **Storage:** 50GB SSD

### Proxies
- **Count:** 50-100 Webshare residential
- **Cost:** $60-100/month

### Configuration
- **Concurrent:** 40-60 searches
- **Delay:** 2-3 seconds
- **Max Pages:** 10

### Performance
- **Nationwide scrape:** 2-3 hours
- **Output:** 200,000+ leads
- **Frequency:** Monthly refresh
- **Cost per lead:** $0.0005-0.001

### Total Monthly Cost
```
Server: $60/month
Proxies (50): $60/month
Total: $120/month

Leads generated: 200,000/month
Cost per lead: $0.0006

vs. Buying leads: $20,000-$40,000
Savings: $19,880/month
ROI: 16,500%
```

---

## ✅ Deployment Checklist

### Before Deployment
- [ ] Server provisioned (16GB+ RAM recommended)
- [ ] SSH access working
- [ ] Domain name (optional)
- [ ] 50-100 proxies purchased

### Installation
- [ ] Dependencies installed
- [ ] Scraper code uploaded
- [ ] Virtual environment created
- [ ] Requirements installed
- [ ] Playwright browsers installed
- [ ] Proxies uploaded

### Configuration
- [ ] Web UI allows remote access (host='0.0.0.0')
- [ ] Firewall configured (port 5001 open or SSH tunnel)
- [ ] Authentication added (if public)
- [ ] Systemd service created
- [ ] Service enabled and started

### Testing
- [ ] Web UI accessible from laptop
- [ ] Small test scrape (2 cities)
- [ ] Proxy health showing in UI
- [ ] Download button works
- [ ] Logs streaming properly

### Production
- [ ] Parallel mode enabled (I need to build this)
- [ ] Concurrency set appropriately
- [ ] Full scrape tested
- [ ] Results downloading
- [ ] Backup system setup (optional)
- [ ] Monitoring in place

---

## 🚀 Next Steps

1. **Get server access** from your friend
2. **I'll build parallel mode** (takes ~15-20 min)
3. **Deploy to server** using this guide
4. **Buy 50 proxies** ($60/month)
5. **Run nationwide scrape** (2-3 hours)
6. **Generate 200K+ leads!**

---

**With a powerful server, you can turn what would take 5 days on your laptop into a 2-hour job!** 🎉
