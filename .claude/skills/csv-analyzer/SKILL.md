---
name: csv-analyzer
description: Analyze CSV files with Python and generate insights. Use this whenever a user wants to analyze a CSV file, explore data patterns, generate statistics, create visualizations, or understand data quality. Generates a reusable Python script using pandas and provides a summary report with key findings, missing data analysis, correlations, and recommended visualizations.
compatibility: Python 3.8+, pandas, matplotlib, seaborn
---

# CSV Analyzer Skill

When a user wants to analyze a CSV file, this skill generates a Python script and provides a comprehensive analysis report.

## What this skill does

1. **Reads the CSV file** — loads the file and inspects its structure
2. **Generates exploratory analysis** — data types, shape, missing values, basic statistics
3. **Creates a Python script** — a reusable pandas-based script the user can modify and re-run
4. **Produces visualizations** — appropriate charts based on the data (distributions, correlations, trends)
5. **Delivers a summary report** — key findings, data quality issues, and actionable insights

## How to use this skill

When you see a user ask to analyze a CSV file, they might phrase it as:
- "Analyze this CSV"
- "Give me insights on this data"
- "Explore this dataset"
- "What patterns are in this file?"
- "Generate stats for this CSV"
- "Check data quality on this file"

### Your workflow

1. **Ask for the file** — if the user hasn't provided it, ask them to share the CSV file path or upload it
2. **Run the analysis** — execute Python code to:
   - Load and inspect the CSV
   - Calculate descriptive statistics (mean, median, std dev, etc.)
   - Identify missing data and data quality issues
   - Detect numeric vs categorical columns
   - Compute correlations for numeric columns
   - Generate appropriate visualizations
3. **Present results** as both a written summary and a saved Python script
4. **Show the script** — provide the generated code so they can re-use, modify, or extend it

## Analysis components

### Summary Report
Include these sections:
- **Dataset Overview** — rows, columns, data types
- **Data Quality** — missing values, duplicates, outliers
- **Key Statistics** — descriptive stats for numeric columns
- **Correlations** — relationships between numeric columns (if applicable)
- **Distributions** — shape of numeric and categorical data
- **Recommended Visualizations** — what charts would reveal patterns

### Generated Python Script
The script should:
- Import pandas, numpy, matplotlib, seaborn
- Load the CSV
- Perform the same analyses shown in the report
- Save visualizations as PNG files
- Be executable as-is, but also easy to modify

## Using the bundled loader script

This skill includes a reusable Python script for CSV analysis:

**Location:** `scripts/load_csv.py`

**Usage:**
```bash
python3 scripts/load_csv.py <path_to_csv_file>
```

**Features:**
- Automatic data type detection (numeric vs categorical)
- Missing value and duplicate detection
- Descriptive statistics for numeric columns
- Category frequency analysis
- Pearson correlation coefficients
- Data quality summary

**Example:**
```bash
python3 scripts/load_csv.py data/sales.csv
```

## Tips

- **Adapt to the data** — don't force analyses that don't apply. If the data is all categorical, skip correlation analysis; if it's mostly numeric, focus on statistical distributions.
- **Handle edge cases** — very large files (>100MB), special characters in column names, missing delimiters
- **Suggest next steps** — after showing the analysis, mention if data cleaning, transformation, or deeper analysis would be useful
- **Make scripts self-contained** — include comments explaining what each section does
- **Reuse the script** — when analyzing CSVs, run the bundled `load_csv.py` script for consistent results

## Example trigger

User: "I have a sales dataset with quarterly numbers. Can you analyze it and tell me what I should be looking at?"

Your response: Run the `load_csv.py` script on the CSV, share the analysis output, and provide a Python script they can adapt for future datasets.
