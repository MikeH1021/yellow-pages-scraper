# Git Push Guide - Upload to GitHub

## ✅ Git Repository Initialized!

Your scraper is now a Git repository with the initial commit complete.

---

## 🚀 How to Push to GitHub

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com/)
2. Click the **"+"** icon (top right) → **"New repository"**
3. **Repository name:** `yellow-pages-scraper`
4. **Description:** "Production-ready Yellow Pages scraper with web UI and parallel processing"
5. **Visibility:**
   - ⚠️ **Private** (RECOMMENDED - contains scraping code)
   - Or Public (if you want to share)
6. **Don't initialize** with README, .gitignore, or license (we already have them)
7. Click **"Create repository"**

### Step 2: Configure Git (First Time Only)

```bash
cd "/Users/jonathangarces/Desktop/yellow page scraper"

# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Add Remote & Push

**GitHub will show you these commands. Use them:**

```bash
cd "/Users/jonathangarces/Desktop/yellow page scraper"

# Add GitHub as remote
git remote add origin https://github.com/YOUR-USERNAME/yellow-pages-scraper.git

# Push to GitHub
git push -u origin main
```

**Replace `YOUR-USERNAME` with your actual GitHub username!**

### Step 4: Enter Credentials

**If using HTTPS:**
- Username: Your GitHub username
- Password: Your GitHub **Personal Access Token** (not your account password!)

**Don't have a token?**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Select scopes: `repo` (all)
4. Copy token and use as password

**Or use SSH (recommended):**
```bash
# Change remote to SSH
git remote set-url origin git@github.com:YOUR-USERNAME/yellow-pages-scraper.git

# Push
git push -u origin main
```

---

## 📦 What's Being Pushed

### Included (52 files, 12,624 lines)
✅ All Python scraper code
✅ Web UI (Flask + HTML)
✅ Proxy management system
✅ Configuration files
✅ City lists (455 cities)
✅ Complete documentation (20+ MD files)
✅ Shell scripts for easy running

### Excluded (.gitignore)
❌ `proxies.txt` (your proxy credentials - NEVER commit!)
❌ `*.csv` files (scraping results - too large)
❌ `*.log` files (logs - not needed in repo)
❌ `venv/` (virtual environment - recreate on each machine)
❌ `__pycache__/` (Python cache - auto-generated)

---

## 🔄 Making Changes & Pushing Updates

### After Making Changes:

```bash
cd "/Users/jonathangarces/Desktop/yellow page scraper"

# Check what changed
git status

# Add all changes
git add .

# Commit with message
git commit -m "Add new feature: XYZ"

# Push to GitHub
git push
```

### Good Commit Message Examples:

```bash
git commit -m "Add parallel processing support for 100+ concurrent searches"
git commit -m "Fix proxy rotation bug in web UI"
git commit -m "Update README with server deployment guide"
git commit -m "Improve block detection for 403/429 errors"
```

---

## 📋 Repository Structure on GitHub

```
yellow-pages-scraper/
│
├── 📄 README.md (⭐ Main documentation - shown on GitHub homepage)
├── 📄 .gitignore (What not to commit)
├── 📄 requirements.txt (Python dependencies)
│
├── 🐍 Core Python Files
│   ├── web_app.py (Flask web server)
│   ├── yellowpages_scraper.py (Scraping engine)
│   ├── proxy_manager.py (Proxy rotation)
│   └── config files
│
├── 📁 templates/ (Web UI HTML)
│   └── scraper.html
│
├── 📁 Documentation/ (20+ guides)
│   ├── WEB_UI_GUIDE.md
│   ├── SERVER_DEPLOYMENT.md
│   ├── PROXY_BLOCK_DETECTION.md
│   └── ... (many more)
│
├── 📁 City Lists (455 cities)
│   ├── cities_top_50.txt
│   ├── cities_top_100.txt
│   └── cities_all.txt
│
└── 🔧 Scripts (Run scripts)
    ├── start_web_ui.sh
    ├── run_small_test.py
    └── run_top_cities.py
```

---

## 🌟 Make Repository Look Professional

### Add Repository Topics (Tags)

On GitHub repository page:
1. Click **"⚙️ Settings"** (gear icon next to About)
2. Add topics:
   ```
   web-scraping
   lead-generation
   yellow-pages
   playwright
   flask
   python
   proxy-rotation
   parallel-processing
   ```

### Update Repository Description

```
Production-ready Yellow Pages scraper with web UI, real-time monitoring, proxy rotation, and parallel processing. Generate 100K+ B2B leads.
```

### Add Website Link

```
https://github.com/YOUR-USERNAME/yellow-pages-scraper
```

---

## 🔒 Security Checklist

### ✅ Before Pushing - VERIFY:

```bash
# Check what's being pushed
git status

# Make sure proxies.txt is NOT listed
# Should show: "nothing to commit, working tree clean"
# Or only files you actually changed

# Double-check .gitignore is working
cat .gitignore | grep proxies.txt
# Should output: proxies.txt
```

### ❌ NEVER Commit:

- `proxies.txt` (proxy credentials)
- Any file with passwords
- `.env` files with API keys
- Large CSV files (> 100MB)

### ✅ Safe to Commit:

- All `.py` code files
- `.md` documentation
- `.txt` city lists
- `.sh` shell scripts
- `templates/` HTML files

---

## 🎯 Quick Reference Commands

```bash
# Check status
git status

# See what changed
git diff

# Add all changes
git add .

# Commit
git commit -m "Your message here"

# Push
git push

# Pull latest from GitHub
git pull

# View commit history
git log --oneline

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main
```

---

## 🔗 Sharing Your Repository

### Public Repository:
```
https://github.com/YOUR-USERNAME/yellow-pages-scraper
```

### Clone Command (for others):
```bash
git clone https://github.com/YOUR-USERNAME/yellow-pages-scraper.git
cd yellow-pages-scraper
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
python web_app.py
```

---

## 📊 GitHub Features to Use

### Issues
Track bugs and feature requests

### Projects
Organize development tasks

### Wiki
Additional documentation

### Releases
Tag stable versions

### Actions (CI/CD)
Automated testing (optional)

---

## 🎉 You're Ready!

Your repository is initialized and ready to push to GitHub.

**Next steps:**
1. Create repository on GitHub
2. Add remote: `git remote add origin https://github.com/YOUR-USERNAME/yellow-pages-scraper.git`
3. Push: `git push -u origin main`
4. Share with your friend for server deployment!

---

## 🆘 Troubleshooting

### "Permission denied (publickey)"
- Use HTTPS instead of SSH
- Or set up SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### "Repository not found"
- Check repository name matches exactly
- Verify you're logged into correct GitHub account

### "Failed to push some refs"
- Pull first: `git pull origin main`
- Then push: `git push`

### "Large files detected"
- Check .gitignore is working
- Remove large files: `git rm --cached large-file.csv`
- Commit and push again

---

**Your scraper is now version-controlled and ready to share!** 🚀
