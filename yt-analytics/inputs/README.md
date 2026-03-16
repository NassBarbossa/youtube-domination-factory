# 📊 YouTube Analytics Input — How to Use

## Quick Start

### Step 1: Download from YouTube Studio
1. Go to **YouTube Studio** → **Analytics**
2. Select your video date range
3. Click **Download** (gear icon)
4. Choose **CSV** format
5. You get a `.zip` file with 2 CSV files inside

### Step 2: Extract the ZIP
Unzip the downloaded file. You'll get:
```
Informations relatives aux tableaux.csv
Totaux.csv
```

### Step 3: Parse with Python
```bash
cd youtube-domination-factory
python yt-analytics/parse_youtube_csv.py "path/to/Informations relatives aux tableaux.csv"
```

This generates a JSON file with structured metrics.

### Step 4: Give to Claude
Either:
- **Option A:** Share the JSON file path
- **Option B:** Share the extracted CSV path

And say:
```
/yt-analytics analyze "video-slug"
```

Or just paste the CSV content and Claude will parse it!

---

## File Formats

### Input: YouTube CSV
Expected columns:
- Vues (Views)
- Impressions
- Taux de clics par impression (%) (CTR)
- Durée moyenne d'une vue (Avg View Duration)
- Pourcentage moyen de vidéo regardé (%) (Avg % watched)
- Durée de visionnage (heures) (Watch time hours)
- Spectateurs uniques (Unique viewers)
- Nouveaux abonnés (New subscribers)
- Partages (Shares)
- Etc.

### Output: JSON (from parser)
```json
{
  "metadata": {...},
  "video_metrics": {
    "views": 167,
    "impressions": 777,
    "ctr": 8.24,
    "avg_percent_watched": 21.42,
    ...
  },
  "audience": {
    "unique_viewers": 102,
    "new_subscribers": 1,
    ...
  }
}
```

---

## Available Commands

### Parse CSV to JSON
```bash
python yt-analytics/parse_youtube_csv.py "path/to/CSV"
```

### Generate Analytics Report
```
/yt-analytics "video-slug"
```

Reads the JSON and generates `analytics-[video-slug].html` with:
- Key metrics
- Retention visualization
- What worked / What didn't
- Prioritized recommendations

---

## Naming Convention

Save your extracted CSV as:
```
yt-analytics/inputs/[video-slug].csv
```

Example:
```
yt-analytics/inputs/vibecoding.csv
yt-analytics/inputs/claude-code-4.csv
```

Then Claude can reference it directly without file paths!

---

## Need Help?

All metrics are extracted automatically from YouTube CSV. Just provide the file and Claude handles the rest.
