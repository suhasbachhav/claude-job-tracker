#!/usr/bin/env python3
"""
CSV Data Loader and Analyzer
Loads CSV files and provides comprehensive data analysis including statistics,
data types, missing values, and correlations. Supports console output and report generation.
"""

import csv
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple
from statistics import mean, median, stdev
from collections import Counter
from datetime import datetime


class CSVAnalyzer:
    """Load and analyze CSV files."""

    def __init__(self, filepath: str):
        """Initialize analyzer with CSV file path."""
        self.filepath = Path(filepath)
        self.rows = []
        self.headers = []
        self.data_types = {}

        if not self.filepath.exists():
            raise FileNotFoundError(f"CSV file not found: {filepath}")

    def load(self) -> bool:
        """Load CSV file into memory."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.headers = reader.fieldnames or []
                self.rows = list(reader)
            return True
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            return False

    def detect_types(self) -> Dict[str, str]:
        """Detect data types for each column."""
        if not self.rows or not self.headers:
            return {}

        self.data_types = {}
        for header in self.headers:
            values = [row.get(header, '') for row in self.rows if row.get(header, '').strip()]

            if not values:
                self.data_types[header] = 'empty'
                continue

            # Try numeric
            numeric_count = 0
            for val in values:
                try:
                    float(val)
                    numeric_count += 1
                except (ValueError, TypeError):
                    pass

            if numeric_count == len(values):
                self.data_types[header] = 'numeric'
            else:
                self.data_types[header] = 'categorical'

        return self.data_types

    def get_summary(self) -> Dict[str, Any]:
        """Generate summary statistics for the dataset."""
        if not self.rows:
            return {}

        summary = {
            'total_rows': len(self.rows),
            'total_columns': len(self.headers),
            'columns': self.headers,
            'missing_values': self._count_missing(),
            'duplicates': self._count_duplicates(),
            'numeric_stats': self._numeric_stats(),
            'categorical_stats': self._categorical_stats(),
        }

        return summary

    def _count_missing(self) -> Dict[str, int]:
        """Count missing values per column."""
        missing = {}
        for header in self.headers:
            count = sum(1 for row in self.rows if not row.get(header, '').strip())
            if count > 0:
                missing[header] = count
        return missing

    def _count_duplicates(self) -> int:
        """Count duplicate rows."""
        if not self.rows:
            return 0

        seen = set()
        duplicates = 0
        for row in self.rows:
            row_tuple = tuple(sorted(row.items()))
            if row_tuple in seen:
                duplicates += 1
            seen.add(row_tuple)
        return duplicates

    def _numeric_stats(self) -> Dict[str, Dict[str, float]]:
        """Calculate statistics for numeric columns."""
        stats = {}

        for header, dtype in self.data_types.items():
            if dtype != 'numeric':
                continue

            values = []
            for row in self.rows:
                try:
                    val = float(row.get(header, 0))
                    values.append(val)
                except (ValueError, TypeError):
                    pass

            if not values:
                continue

            values.sort()
            stats[header] = {
                'count': len(values),
                'min': min(values),
                'max': max(values),
                'mean': mean(values),
                'median': median(values),
                'std_dev': stdev(values) if len(values) > 1 else 0,
            }

        return stats

    def _categorical_stats(self) -> Dict[str, List[Tuple[str, int]]]:
        """Get top categories for categorical columns."""
        stats = {}

        for header, dtype in self.data_types.items():
            if dtype != 'categorical':
                continue

            values = [row.get(header, '') for row in self.rows if row.get(header, '').strip()]

            if not values:
                continue

            counter = Counter(values)
            stats[header] = counter.most_common(10)  # Top 10 categories

        return stats

    def get_correlations(self) -> Dict[Tuple[str, str], float]:
        """Calculate correlations between numeric columns (simple Pearson)."""
        numeric_cols = [h for h, t in self.data_types.items() if t == 'numeric']

        if len(numeric_cols) < 2:
            return {}

        # Extract numeric data
        numeric_data = {}
        for col in numeric_cols:
            values = []
            for row in self.rows:
                try:
                    values.append(float(row.get(col, 0)))
                except (ValueError, TypeError):
                    values.append(0)
            numeric_data[col] = values

        # Simple correlation calculation
        correlations = {}
        for i, col1 in enumerate(numeric_cols):
            for col2 in numeric_cols[i+1:]:
                corr = self._pearson_correlation(numeric_data[col1], numeric_data[col2])
                if corr is not None:
                    correlations[(col1, col2)] = corr

        return correlations

    @staticmethod
    def _pearson_correlation(x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient."""
        if len(x) < 2 or len(y) < 2 or len(x) != len(y):
            return None

        mean_x = mean(x)
        mean_y = mean(y)

        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
        denom_x = sum((val - mean_x) ** 2 for val in x) ** 0.5
        denom_y = sum((val - mean_y) ** 2 for val in y) ** 0.5

        if denom_x == 0 or denom_y == 0:
            return 0

        return numerator / (denom_x * denom_y)

    def _get_recommendations(self, summary: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []

        if summary['missing_values']:
            recommendations.append("❗ Handle missing values through imputation or removal")

        if summary['duplicates'] > 0:
            recommendations.append("❗ Investigate and remove duplicate rows")

        numeric_cols = [col for col, dtype in self.data_types.items() if dtype == 'numeric']
        if len(numeric_cols) >= 2:
            recommendations.append(f"✓ Visualize relationships between {len(numeric_cols)} numeric columns")

        categorical_cols = [col for col, dtype in self.data_types.items() if dtype == 'categorical']
        if categorical_cols:
            recommendations.append(f"✓ Create bar charts for {len(categorical_cols)} categorical columns")

        return recommendations

    def print_report(self):
        """Print formatted analysis report to console."""
        if not self.load():
            return

        self.detect_types()
        summary = self.get_summary()

        print("\n" + "=" * 70)
        print("📊 CSV ANALYSIS REPORT")
        print("=" * 70)

        # Dataset Overview
        print(f"\n📋 DATASET OVERVIEW")
        print(f"  File: {self.filepath.name}")
        print(f"  Rows: {summary['total_rows']}")
        print(f"  Columns: {summary['total_columns']}")
        print(f"  Column Names: {', '.join(self.headers)}")

        # Data Types
        print(f"\n🔍 DATA TYPES")
        for header, dtype in self.data_types.items():
            print(f"  {header}: {dtype}")

        # Data Quality
        print(f"\n⚠️ DATA QUALITY")
        if summary['missing_values']:
            for col, count in summary['missing_values'].items():
                pct = (count / summary['total_rows']) * 100
                print(f"  Missing {col}: {count} ({pct:.1f}%)")
        else:
            print(f"  ✅ No missing values")

        if summary['duplicates'] > 0:
            pct = (summary['duplicates'] / summary['total_rows']) * 100
            print(f"  Duplicates: {summary['duplicates']} ({pct:.1f}%)")
        else:
            print(f"  ✅ No duplicate rows")

        # Numeric Statistics
        if summary['numeric_stats']:
            print(f"\n📈 NUMERIC STATISTICS")
            for col, stats in summary['numeric_stats'].items():
                print(f"\n  {col}:")
                print(f"    Min: {stats['min']:.2f}")
                print(f"    Max: {stats['max']:.2f}")
                print(f"    Mean: {stats['mean']:.2f}")
                print(f"    Median: {stats['median']:.2f}")
                print(f"    Std Dev: {stats['std_dev']:.2f}")

        # Categorical Statistics
        if summary['categorical_stats']:
            print(f"\n🏷️ CATEGORICAL DATA")
            for col, categories in summary['categorical_stats'].items():
                print(f"\n  {col}:")
                for cat, count in categories[:5]:
                    pct = (count / summary['total_rows']) * 100
                    print(f"    {cat}: {count} ({pct:.1f}%)")

        # Correlations
        correlations = self.get_correlations()
        if correlations:
            print(f"\n🔗 CORRELATIONS (numeric columns)")
            for (col1, col2), corr in sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True):
                print(f"  {col1} ↔ {col2}: {corr:.3f}")

        # Recommendations
        recommendations = self._get_recommendations(summary)
        if recommendations:
            print(f"\n💡 RECOMMENDATIONS")
            for rec in recommendations:
                print(f"  {rec}")

        print("\n" + "=" * 70)

    def generate_markdown_report(self, output_path: str) -> bool:
        """Generate a markdown formatted report file."""
        if not self.load():
            return False

        self.detect_types()
        summary = self.get_summary()
        correlations = self.get_correlations()
        recommendations = self._get_recommendations(summary)

        report = []
        report.append("# CSV Analysis Report\n")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"**File:** `{self.filepath.name}`\n")

        # Overview
        report.append("\n## Dataset Overview\n")
        report.append(f"- **Total Rows:** {summary['total_rows']}\n")
        report.append(f"- **Total Columns:** {summary['total_columns']}\n")
        report.append(f"- **Columns:** {', '.join(f'`{h}`' for h in self.headers)}\n")

        # Data Types
        report.append("\n## Data Types\n")
        report.append("| Column | Type |\n")
        report.append("|--------|------|\n")
        for header, dtype in self.data_types.items():
            report.append(f"| {header} | {dtype} |\n")

        # Data Quality
        report.append("\n## Data Quality\n")
        if summary['missing_values']:
            report.append("### Missing Values\n")
            for col, count in summary['missing_values'].items():
                pct = (count / summary['total_rows']) * 100
                report.append(f"- {col}: {count} ({pct:.1f}%)\n")
        else:
            report.append("✅ No missing values detected\n")

        if summary['duplicates'] > 0:
            pct = (summary['duplicates'] / summary['total_rows']) * 100
            report.append(f"\n⚠️ **Duplicates:** {summary['duplicates']} ({pct:.1f}%)\n")
        else:
            report.append("\n✅ No duplicate rows detected\n")

        # Numeric Statistics
        if summary['numeric_stats']:
            report.append("\n## Numeric Statistics\n")
            for col, stats in summary['numeric_stats'].items():
                report.append(f"\n### {col}\n")
                report.append(f"| Metric | Value |\n")
                report.append(f"|--------|-------|\n")
                report.append(f"| Count | {stats['count']} |\n")
                report.append(f"| Min | {stats['min']:.2f} |\n")
                report.append(f"| Max | {stats['max']:.2f} |\n")
                report.append(f"| Mean | {stats['mean']:.2f} |\n")
                report.append(f"| Median | {stats['median']:.2f} |\n")
                report.append(f"| Std Dev | {stats['std_dev']:.2f} |\n")

        # Categorical Data
        if summary['categorical_stats']:
            report.append("\n## Categorical Data\n")
            for col, categories in summary['categorical_stats'].items():
                report.append(f"\n### {col}\n")
                report.append("| Category | Count | Percentage |\n")
                report.append("|----------|-------|------------|\n")
                for cat, count in categories[:10]:
                    pct = (count / summary['total_rows']) * 100
                    report.append(f"| {cat} | {count} | {pct:.1f}% |\n")

        # Correlations
        if correlations:
            report.append("\n## Correlations (Numeric Columns)\n")
            report.append("| Column 1 | Column 2 | Correlation |\n")
            report.append("|----------|----------|-------------|\n")
            for (col1, col2), corr in sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True):
                strength = "Strong" if abs(corr) > 0.7 else "Moderate" if abs(corr) > 0.3 else "Weak"
                report.append(f"| {col1} | {col2} | {corr:.3f} ({strength}) |\n")

        # Recommendations
        if recommendations:
            report.append("\n## Recommendations\n")
            for rec in recommendations:
                report.append(f"- {rec}\n")

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.writelines(report)
            print(f"✅ Report saved to: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return False

    def export_json(self, output_path: str) -> bool:
        """Export analysis results as JSON."""
        if not self.load():
            return False

        self.detect_types()
        summary = self.get_summary()
        correlations = self.get_correlations()

        data = {
            'file': self.filepath.name,
            'generated': datetime.now().isoformat(),
            'summary': summary,
            'data_types': self.data_types,
            'correlations': {f"{k[0]} ↔ {k[1]}": v for k, v in correlations.items()},
        }

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"✅ JSON export saved to: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving JSON: {e}")
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='CSV Data Analyzer - Generate insights and reports from CSV files'
    )
    parser.add_argument('csv_file', help='Path to CSV file to analyze')
    parser.add_argument(
        '--report',
        type=str,
        help='Generate markdown report and save to specified file'
    )
    parser.add_argument(
        '--json',
        type=str,
        help='Export analysis results as JSON'
    )

    args = parser.parse_args()

    analyzer = CSVAnalyzer(args.csv_file)

    if args.report:
        analyzer.generate_markdown_report(args.report)
    elif args.json:
        analyzer.export_json(args.json)
    else:
        analyzer.print_report()


if __name__ == '__main__':
    main()
