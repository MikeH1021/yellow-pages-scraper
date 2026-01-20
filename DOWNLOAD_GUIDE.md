# Download Guide - Where Files Save & How to Download

## 📁 Where Files Save

### Current Behavior

CSV files save to:
```
/Users/jonathangarces/Desktop/yellow page scraper/scrape_results_TIMESTAMP.csv
```

**Example:**
```
scrape_results_20260120_142315.csv
scrape_results_20260120_150722.csv
scrape_results_20260120_163045.csv
```

---

## 📥 How to Download Files

### Method 1: Download Button (Easiest) ⭐

**After scraping completes:**

1. You'll see a **"📥 Download Results CSV"** button appear in the Progress Panel
2. Click the button
3. Chrome will prompt you to **choose where to save the file**
4. Select your preferred location (Downloads, Desktop, etc.)
5. File downloads directly to your chosen location

**Screenshot of what you'll see:**
```
┌─────────────────────────────────────────┐
│  Scraping Progress                      │
├─────────────────────────────────────────┤
│  [████████████████████████] 100%        │
│                                         │
│  SEARCHES COMPLETED: 10                 │
│  TOTAL SEARCHES: 10                     │
│  BUSINESSES FOUND: 387                  │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  📥 Download Results CSV          │ │
│  └───────────────────────────────────┘ │
│  File: scrape_results_20260120_142315  │
└─────────────────────────────────────────┘
```

### Method 2: Previous Results Panel

**Download any previous scrape:**

1. Scroll down to **"📁 Previous Results"** panel
2. See list of all CSV files with:
   - Filename
   - Date/time created
   - File size
3. Click **"📥 Download"** next to any file
4. Chrome prompts you to choose save location
5. Done!

**Screenshot:**
```
┌─────────────────────────────────────────────────────────┐
│  📁 Previous Results                                    │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────┐  │
│  │ 📄 scrape_results_20260120_163045.csv            │  │
│  │ 2026-01-20 16:30:45 • 125.3 KB                   │  │
│  │                              [📥 Download]        │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 📄 scrape_results_20260120_150722.csv            │  │
│  │ 2026-01-20 15:07:22 • 89.7 KB                    │  │
│  │                              [📥 Download]        │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 📄 scrape_results_20260120_142315.csv            │  │
│  │ 2026-01-20 14:23:15 • 203.4 KB                   │  │
│  │                              [📥 Download]        │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Method 3: Manual File Access

**If you prefer to browse files directly:**

1. Open Finder
2. Navigate to: `/Users/jonathangarces/Desktop/yellow page scraper/`
3. Look for files starting with `scrape_results_`
4. Double-click to open in Excel/Numbers
5. Or drag to your preferred location

---

## 🎯 Chrome Download Behavior

### What Happens When You Click Download

**Step 1: Click "📥 Download Results CSV"**

**Step 2: Chrome prompts you:**
```
┌────────────────────────────────────────┐
│  Save As                               │
├────────────────────────────────────────┤
│  Save as: scrape_results_20260120.csv  │
│                                        │
│  Where: [Downloads         ▼]         │
│                                        │
│  Tags: [None               ▼]         │
│                                        │
│         [Cancel]  [Save]               │
└────────────────────────────────────────┘
```

**Step 3: Choose your location:**
- Downloads folder (default)
- Desktop
- Documents
- Custom folder

**Step 4: Click "Save"**
- File downloads to your chosen location
- Chrome shows download in bottom left
- Click downloaded file to open

---

## 📊 File Format

### CSV Structure

**Columns included:**
```
business_name
phone
street
city
state
zip
website
categories
rating
years_in_business
search_category
search_location
```

**Example row:**
```
"ABC Building Supply","305-555-1234","123 Main St","Miami","FL","33101","www.abcbuildingsupply.com","Building Materials, Lumber","4.5","15","building supply","Miami FL"
```

### Opening the File

**In Excel:**
1. Download the CSV
2. Open Excel
3. File → Open → Select the CSV
4. Data imports with proper columns

**In Google Sheets:**
1. Download the CSV
2. Go to sheets.google.com
3. File → Import → Upload
4. Select the downloaded CSV

**In Numbers (Mac):**
1. Double-click the CSV file
2. Numbers opens automatically
3. Data formatted in table

---

## 🔄 Auto-Refresh

### Previous Results Panel

The **"📁 Previous Results"** panel:
- Updates every 10 seconds automatically
- Shows newest files at the top
- No page refresh needed
- Appears only when CSV files exist

### When Files Appear

**Download button appears:**
- ✅ Immediately after scraping completes
- ✅ When you reload the page (if files exist)
- ✅ Automatically refreshes list

**Files are sorted by:**
- Newest first (top)
- Oldest last (bottom)

---

## 💡 Tips

### 1. Organize Your Downloads

**Create a folder structure:**
```
Downloads/
├── YellowPages/
│   ├── 2026-01-20/
│   │   ├── scrape_results_142315.csv
│   │   ├── scrape_results_150722.csv
│   │   └── scrape_results_163045.csv
│   ├── 2026-01-21/
│   └── 2026-01-22/
```

**When downloading:**
- Choose custom location
- Navigate to YellowPages folder
- Create date folder
- Save there

### 2. Rename Files for Clarity

**Default name:**
```
scrape_results_20260120_142315.csv
```

**Rename to:**
```
miami_chicago_building_supply_500_leads.csv
top_100_cities_all_categories_25000_leads.csv
```

**In Chrome download prompt:**
- Change filename before saving
- Add descriptive name
- Keep .csv extension

### 3. Import Directly to CRM

**For Instantly.ai:**
1. Download CSV
2. Go to Instantly.ai
3. Leads → Import
4. Upload the downloaded CSV
5. Map columns (phone, email, name, etc.)

**For Salesforce:**
1. Download CSV
2. Go to Salesforce
3. Data Import Wizard
4. Upload CSV
5. Map to Salesforce fields

### 4. Combine Multiple Scrapes

**If you have multiple CSVs:**

**In Excel:**
1. Open first CSV
2. Open second CSV
3. Copy all rows from second
4. Paste into first below existing data
5. Remove duplicates:
   - Data → Remove Duplicates
   - Select "phone" or "business_name" column

**In Google Sheets:**
1. Import first CSV
2. Import second CSV to new tab
3. Use QUERY to combine:
   ```
   =QUERY({Sheet1!A2:L; Sheet2!A2:L}, "SELECT * WHERE Col1 is not null")
   ```

---

## 🚨 Troubleshooting

### Download Button Not Appearing

**Problem:** Scraping finished but no download button

**Solution:**
1. Wait 2-3 seconds (button appears after file is saved)
2. Check "📁 Previous Results" panel below
3. Refresh page (F5)
4. File should appear in list

### Chrome Asking Where to Save Every Time

**Problem:** Want downloads to go to same folder automatically

**Solution:**
1. Chrome Settings → Downloads
2. Uncheck "Ask where to save each file before downloading"
3. Set default download location
4. Files auto-save to that folder

**Note:** I recommend keeping "Ask where to save" ON so you can organize by scrape type

### File Opens in Browser Instead of Downloading

**Problem:** CSV opens in browser tab

**Solution:**
1. Right-click the download button
2. Select "Save Link As..."
3. Choose location
4. Save

**Or in Chrome settings:**
1. Settings → Downloads
2. Check "Ask where to save each file"

### Can't Find Downloaded File

**Problem:** Downloaded but can't locate file

**Solution:**
1. Check Chrome downloads (Ctrl+J or Cmd+J)
2. Click "Show in folder"
3. Or check default Downloads folder
4. Or check web UI "Previous Results" - it's still on the server

---

## 📖 Summary

### Where Files Save on Server:
```
/Users/jonathangarces/Desktop/yellow page scraper/scrape_results_*.csv
```

### How to Download:

**Option 1 (Easiest):**
- Click "📥 Download Results CSV" button after scraping
- Choose save location in Chrome
- Done!

**Option 2:**
- Scroll to "📁 Previous Results" panel
- Click "📥 Download" next to any file
- Choose save location
- Done!

**Option 3:**
- Browse to scraper folder in Finder
- Copy files manually

### What You Get:
- CSV file ready for Excel/Sheets/CRM
- All business data: name, phone, address, website
- Tagged with search category and location
- Ready to import anywhere

---

**The download button appears automatically when scraping finishes. Just click and choose where to save!** 🎉
