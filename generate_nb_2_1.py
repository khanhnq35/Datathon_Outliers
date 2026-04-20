import json
import os

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Module \u2776: T\u0103ng tr\u01b0\u1edfng & T\u00e0i ch\u00ednh - Descriptive Analysis\n",
                "**Task 2.1: Revenue YoY Trend & Seasonality**\n",
                "*Owner: L\u00ea B\u1ea3o Kh\u00e1nh*\n",
                "\n",
                "M\u1ee5c ti\u00eau:\n",
                "- Ph\u00e2n t\u00edch xu h\u01b0\u1edbng doanh thu qua c\u00e1c n\u0103m (2012-2022).\n",
                "- T\u00ednh to\u00e1n t\u1ed1c \u0111\u1ed9 t\u0103ng tr\u01b0\u1edfng (YoY Growth Rate) v\u00e0 CAGR.\n",
                "- Ph\u00e1t hi\u1ec7n t\u00ednh m\u00f9a v\u1ee5 (Seasonality) theo th\u00e1ng/qu\u00fd."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import polars as pl\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "import numpy as np\n",
                "import sys\n",
                "import os\n",
                "\n",
                "# Add src to path if needed\n",
                "sys.path.append(os.path.abspath(os.path.join('..', 'src')))\n",
                "from data_loader import DataLoader\n",
                "\n",
                "# Set random state and plot style\n",
                "np.random.seed(42)\n",
                "plt.style.use('seaborn-v0_8-whitegrid')\n",
                "sns.set_palette(\"husl\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 1. Load data: sales, order_items, products\n",
                "loader = DataLoader(data_dir=\"../Data\")\n",
                "\n",
                "# Load necessary tables\n",
                "sales = loader.load(\"sales\")\n",
                "order_items = loader.load(\"order_items\")\n",
                "products = loader.load(\"products\")\n",
                "\n",
                "print(\"Sales data shape:\", sales.shape)\n",
                "print(\"Date range:\", sales['Date'].min(), \"to\", sales['Date'].max())\n",
                "print(sales.head(3))"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Xu h\u01b0\u1edbng Doanh thu (Revenue YoY Trend)\n",
                "Ph\u00e2n t\u00edch t\u1ed5ng doanh thu theo n\u0103m v\u00e0 t\u1ed1c \u0111\u1ed9 t\u0103ng tr\u01b0\u1edfng (Growth Rate)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Th\u00eam c\u1ed9t Year v\u00e0 Month\n",
                "sales = sales.with_columns([\n",
                "    pl.col(\"Date\").dt.year().alias(\"Year\"),\n",
                "    pl.col(\"Date\").dt.month().alias(\"Month\"),\n",
                "    pl.col(\"Date\").dt.quarter().alias(\"Quarter\")\n",
                "])\n",
                "\n",
                "# Group by Year\n",
                "yearly_sales = sales.group_by(\"Year\").agg(\n",
                "    pl.col(\"Revenue\").sum().alias(\"Total_Revenue\")\n",
                ").sort(\"Year\")\n",
                "\n",
                "# T\u00ednh Growth Rate\n",
                "yearly_sales = yearly_sales.with_columns([\n",
                "    (pl.col(\"Total_Revenue\").diff() / pl.col(\"Total_Revenue\").shift(1) * 100).alias(\"YoY_Growth_Rate_%\")\n",
                "])\n",
                "\n",
                "print(yearly_sales)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# V\u1ebd Line Chart YoY\n",
                "fig, ax1 = plt.subplots(figsize=(12, 6))\n",
                "\n",
                "years = yearly_sales[\"Year\"].to_list()\n",
                "revenue = yearly_sales[\"Total_Revenue\"].to_list()\n",
                "growth = yearly_sales[\"YoY_Growth_Rate_%\"].to_list()\n",
                "\n",
                "color = 'tab:blue'\n",
                "ax1.set_xlabel('Year', fontweight='bold')\n",
                "ax1.set_ylabel('Total Revenue ($)', color=color, fontweight='bold')\n",
                "line1 = ax1.plot(years, revenue, marker='o', linewidth=2.5, color=color, label='Revenue')\n",
                "ax1.tick_params(axis='y', labelcolor=color)\n",
                "ax1.set_xticks(years)\n",
                "\n",
                "# Format y-axis to millions\n",
                "formatter = plt.FuncFormatter(lambda x, pos: f'${x*1e-6:.1f}M')\n",
                "ax1.yaxis.set_major_formatter(formatter)\n",
                "\n",
                "# Dual axis for Growth Rate\n",
                "ax2 = ax1.twinx()  \n",
                "color2 = 'tab:red'\n",
                "ax2.set_ylabel('YoY Growth Rate (%)', color=color2, fontweight='bold')\n",
                "line2 = ax2.plot(years, growth, marker='s', linestyle='--', color=color2, label='Growth Rate (%)')\n",
                "ax2.tick_params(axis='y', labelcolor=color2)\n",
                "\n",
                "# Annotate anomalies/key points\n",
                "for i, txt in enumerate(growth):\n",
                "    if txt is not None and not np.isnan(txt):\n",
                "        ax2.annotate(f\"{txt:.1f}%\", (years[i], growth[i]), textcoords=\"offset points\", xytext=(0,10), ha='center', color=color2)\n",
                "\n",
                "plt.title('Revenue YoY Trend & Growth Rate (2012 - 2022)', fontsize=16, fontweight='bold')\n",
                "fig.tight_layout()\n",
                "\n",
                "# Legend\n",
                "lines = line1 + line2\n",
                "labels = [l.get_label() for l in lines]\n",
                "ax1.legend(lines, labels, loc='upper left')\n",
                "\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# T\u00ednh CAGR (Compound Annual Growth Rate) to\u00e0n giai \u0111o\u1ea1n\n",
                "# CAGR = (Ending Value / Beginning Value) ^ (1 / Number of Years) - 1\n",
                "\n",
                "start_year = yearly_sales[\"Year\"][0]\n",
                "end_year = yearly_sales[\"Year\"][-1]\n",
                "num_years = end_year - start_year\n",
                "\n",
                "start_revenue = yearly_sales.filter(pl.col(\"Year\") == start_year)[\"Total_Revenue\"][0]\n",
                "end_revenue = yearly_sales.filter(pl.col(\"Year\") == end_year)[\"Total_Revenue\"][0]\n",
                "\n",
                "cagr = ((end_revenue / start_revenue) ** (1 / num_years)) - 1\n",
                "print(f\"B\u1eaft \u0111\u1ea7u ({start_year}): ${start_revenue:,.2f}\")\n",
                "print(f\"K\u1ebft th\u00fac ({end_year}): ${end_revenue:,.2f}\")\n",
                "print(f\"CAGR ({start_year}-{end_year}): {cagr * 100:.2f}%\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. T\u00ednh M\u00f9a V\u1ee5 (Seasonality)\n",
                "Ph\u00e2n t\u00edch theo th\u00e1ng \u0111\u1ec3 ph\u00e1t hi\u1ec7n c\u00e1c m\u1eabu (patterns) l\u1eb7p l\u1ea1i h\u00e0ng n\u0103m."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Group by Year and Month\n",
                "monthly_sales = sales.group_by([\"Year\", \"Month\"]).agg(\n",
                "    pl.col(\"Revenue\").sum().alias(\"Monthly_Revenue\")\n",
                ").sort([\"Year\", \"Month\"])\n",
                "\n",
                "# Pivot data for heatmap\n",
                "pivot_df = monthly_sales.pivot(values=\"Monthly_Revenue\", index=\"Year\", on=\"Month\")\n",
                "# Fill nulls with 0 or drop incomplete years\n",
                "pivot_df = pivot_df.fill_null(0)\n",
                "\n",
                "# Convert to pandas for easier seaborn heatmap plotting\n",
                "pd_pivot = pivot_df.to_pandas().set_index(\"Year\")\n",
                "# Sort columns (months) in case they are out of order\n",
                "pd_pivot = pd_pivot[sorted([c for c in pd_pivot.columns if str(c).isdigit()])]\n",
                "\n",
                "plt.figure(figsize=(14, 6))\n",
                "sns.heatmap(pd_pivot / 1e6, cmap=\"YlGnBu\", annot=True, fmt=\".1f\", cbar_kws={'label': 'Revenue ($ Millions)'})\n",
                "plt.title('Monthly Revenue Heatmap (in $ Millions)', fontsize=16, fontweight='bold')\n",
                "plt.xlabel('Month', fontweight='bold')\n",
                "plt.ylabel('Year', fontweight='bold')\n",
                "plt.show()\n",
                "\n",
                "# Trung b\u00ecnh doanh thu theo th\u00e1ng (box plot)\n",
                "plt.figure(figsize=(12, 6))\n",
                "sns.boxplot(data=monthly_sales.to_pandas(), x=\"Month\", y=\"Monthly_Revenue\", palette=\"viridis\")\n",
                "plt.title('Revenue Distribution by Month (Seasonality Check)', fontsize=16, fontweight='bold')\n",
                "plt.xlabel('Month', fontweight='bold')\n",
                "plt.ylabel('Revenue ($)', fontweight='bold')\n",
                "\n",
                "formatter = plt.FuncFormatter(lambda x, pos: f'${x*1e-6:.1f}M')\n",
                "plt.gca().yaxis.set_major_formatter(formatter)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## \ud83d\udcdd Narrative - Business Insights\n",
                "D\u1ef1a v\u00e0o ph\u00e2n t\u00edch tr\u00ean:\n",
                "1. **Xu h\u01b0\u1edbng t\u0103ng tr\u01b0\u1edfng (YoY Trend)**:\n",
                "   - Doanh nghi\u1ec7p c\u00f3 ch\u1ec9 s\u1ed1 t\u0103ng tr\u01b0\u1edfng (Growth Rate) \u1ed5n \u0111\u1ecbnh hay bi\u1ebfn \u0111\u1ed9ng?\n",
                "   - T\u00ednh to\u00e1n CAGR cho th\u1ea5y b\u1ee9c tranh d\u00e0i h\u1ea1n (CAGR ~ X%). \n",
                "   - \u0110i\u1ec3m \u0111\u00e1ng ch\u00fa \u00fd: N\u0103m n\u00e0o c\u00f3 s\u1ef1 s\u1ee5t gi\u1ea3m ho\u1eb7c t\u0103ng \u0111\u1ed9t bi\u1ebfn? (C\u1ea7n investigate th\u00eam trong ph\u1ea7n Diagnostic).\n",
                "   \n",
                "2. **T\u00ednh m\u00f9a v\u1ee5 (Seasonality)**:\n",
                "   - Doanh thu cao nh\u1ea5t th\u01b0\u1eddng r\u01a1i v\u00e0o nh\u1eefng th\u00e1ng n\u00e0o? (V\u00ed d\u1ee5: Th\u00e1ng 11-12 do m\u00f9a l\u1ec5 h\u1ed9i/khuy\u1ebfn m\u00e3i).\n",
                "   - C\u00f3 th\u00e1ng n\u00e0o lu\u00f4n \u1edf m\u1ee9c th\u1ea5p kh\u00f4ng? \n",
                "   - Th\u00f4ng tin n\u00e0y h\u1eefu \u00edch \u0111\u1ec3 chu\u1ea9n b\u1ecb inventory (Module 4) v\u00e0 d\u1ed3n ng\u00e2n s\u00e1ch marketing (Module 5)."
            ]
        }
    ],
    "metadata": {
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

os.makedirs('notebooks', exist_ok=True)
with open('notebooks/02_M1_revenue_health.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print("Notebook generated successfully at notebooks/02_M1_revenue_health.ipynb")
