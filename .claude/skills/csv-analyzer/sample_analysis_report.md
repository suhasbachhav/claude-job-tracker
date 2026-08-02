# CSV Analysis Report
**Generated:** 2026-08-02 18:53:24
**File:** `sample_data.csv`

## Dataset Overview
- **Total Rows:** 16
- **Total Columns:** 8
- **Columns:** `product`, `category`, `price`, `quantity`, `sales`, `region`, `quarter`, `customer_satisfaction`

## Data Types
| Column | Type |
|--------|------|
| product | categorical |
| category | categorical |
| price | numeric |
| quantity | numeric |
| sales | numeric |
| region | categorical |
| quarter | categorical |
| customer_satisfaction | numeric |

## Data Quality
✅ No missing values detected

✅ No duplicate rows detected

## Numeric Statistics

### price
| Metric | Value |
|--------|-------|
| Count | 16 |
| Min | 50.00 |
| Max | 1200.00 |
| Mean | 467.50 |
| Median | 350.00 |
| Std Dev | 356.79 |

### quantity
| Metric | Value |
|--------|-------|
| Count | 16 |
| Min | 45.00 |
| Max | 500.00 |
| Mean | 131.56 |
| Median | 105.00 |
| Std Dev | 110.18 |

### sales
| Metric | Value |
|--------|-------|
| Count | 16 |
| Min | 15000.00 |
| Max | 96000.00 |
| Mean | 41812.50 |
| Median | 35000.00 |
| Std Dev | 23591.58 |

### customer_satisfaction
| Metric | Value |
|--------|-------|
| Count | 16 |
| Min | 7.50 |
| Max | 8.60 |
| Mean | 8.12 |
| Median | 8.15 |
| Std Dev | 0.31 |

## Categorical Data

### product
| Category | Count | Percentage |
|----------|-------|------------|
| Laptop | 2 | 12.5% |
| Phone | 2 | 12.5% |
| Tablet | 2 | 12.5% |
| Monitor | 2 | 12.5% |
| Desk | 2 | 12.5% |
| Chair | 2 | 12.5% |
| Keyboard | 1 | 6.2% |
| Mouse | 1 | 6.2% |
| Lamp | 1 | 6.2% |
| Bookshelf | 1 | 6.2% |

### category
| Category | Count | Percentage |
|----------|-------|------------|
| Electronics | 10 | 62.5% |
| Furniture | 6 | 37.5% |

### region
| Category | Count | Percentage |
|----------|-------|------------|
| North | 4 | 25.0% |
| South | 4 | 25.0% |
| East | 4 | 25.0% |
| West | 4 | 25.0% |

### quarter
| Category | Count | Percentage |
|----------|-------|------------|
| Q1 | 4 | 25.0% |
| Q2 | 4 | 25.0% |
| Q3 | 4 | 25.0% |
| Q4 | 4 | 25.0% |

## Correlations (Numeric Columns)
| Column 1 | Column 2 | Correlation |
|----------|----------|-------------|
| price | sales | 0.695 (Moderate) |
| price | customer_satisfaction | 0.571 (Moderate) |
| price | quantity | -0.534 (Moderate) |
| sales | customer_satisfaction | 0.388 (Moderate) |
| quantity | sales | -0.199 (Weak) |
| quantity | customer_satisfaction | -0.173 (Weak) |

## Recommendations
- ✓ Visualize relationships between 4 numeric columns
- ✓ Create bar charts for 4 categorical columns
