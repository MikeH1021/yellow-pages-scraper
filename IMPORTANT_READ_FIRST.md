# ⚠️ IMPORTANT: Always Activate Virtual Environment

## The Problem You Just Had

When you ran:
```bash
python3 test_scraper.py
```

You got:
```
ModuleNotFoundError: No module named 'playwright'
```

**Why?** You didn't activate the virtual environment!

## ✅ The Solution

### Option 1: Use Helper Scripts (Easiest)

Just run these - they handle everything:

```bash
./test.sh       # Run tests
./run.sh        # Run scraper
./run_with_logs.sh  # Run with logs saved
```

### Option 2: Activate Manually

**Every time you open a new terminal**, run:

```bash
cd "/Users/jonathangarces/Desktop/yellow page scraper"
source venv/bin/activate
```

Your prompt will change to show `(venv)`:
```bash
(venv) jonathangarces@Jonathans-MacBook-Pro yellow page scraper %
  ↑
This means it's activated!
```

Now you can run:
```bash
python test_scraper.py
python run_scraper.py
python quick_test.py
```

## 🎯 Quick Reference

### ❌ Wrong (Will Fail)
```bash
# DON'T do this:
python3 test_scraper.py          # ❌ No venv
python quick_test.py              # ❌ No venv
cd .. && python quick_test.py     # ❌ Wrong directory
```

### ✅ Correct

**Method 1: Helper scripts**
```bash
cd "/Users/jonathangarces/Desktop/yellow page scraper"
./test.sh                         # ✅ Auto-activates venv
```

**Method 2: Manual activation**
```bash
cd "/Users/jonathangarces/Desktop/yellow page scraper"
source venv/bin/activate          # Activate venv
python test_scraper.py            # ✅ Now it works
```

## 📋 Step-by-Step Checklist

Every time you want to run the scraper:

1. **Open terminal**
2. **Navigate to project:**
   ```bash
   cd "/Users/jonathangarces/Desktop/yellow page scraper"
   ```
3. **Choose one:**

   **Option A - Use helper script:**
   ```bash
   ./test.sh
   ```

   **Option B - Activate manually:**
   ```bash
   source venv/bin/activate
   python test_scraper.py
   ```

## 🔍 How to Tell if Venv is Activated

Look at your terminal prompt:

**Not activated:**
```bash
jonathangarces@Jonathans-MacBook-Pro yellow page scraper %
```

**Activated:**
```bash
(venv) jonathangarces@Jonathans-MacBook-Pro yellow page scraper %
  ↑
Shows (venv) prefix
```

## 🚀 All Available Commands

Once venv is activated, you can run:

```bash
# Quick test (1 page, no proxies)
python quick_test.py

# Interactive test menu
python test_scraper.py

# Get free proxies
python get_free_proxies.py

# Full production scrape
python run_scraper.py

# Or use helper scripts (auto-activate venv):
./test.sh
./run.sh
./run_with_logs.sh
```

## 💡 Pro Tip: Auto-Activate

Add to your `~/.zshrc` or `~/.bash_profile`:

```bash
# Auto-activate when entering project directory
alias scraper='cd "/Users/jonathangarces/Desktop/yellow page scraper" && source venv/bin/activate'
```

Then just type:
```bash
scraper
python test_scraper.py
```

## 🆘 Still Having Issues?

### Error: "No module named playwright"
→ Venv not activated. Run: `source venv/bin/activate`

### Error: "Can't open file"
→ Wrong directory. Run: `cd "/Users/jonathangarces/Desktop/yellow page scraper"`

### Error: "Permission denied"
→ Script not executable. Run: `chmod +x test.sh run.sh`

## 📖 Summary

**Remember these two things:**

1. **Always be in the right directory**
2. **Always activate the venv first**

**Easiest way:** Use the helper scripts!
```bash
./test.sh
```

They handle everything automatically.
