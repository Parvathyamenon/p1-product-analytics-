# FILE: retention_analysis.py
# PURPOSE: Load Olist data, calculate retention + churn, produce charts
# HOW TO RUN: pip install pandas matplotlib seaborn  then  python retention_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ── STEP 1: Load data ────────────────────────────────────────────
print('Loading data...')
orders   = pd.read_csv('data/olist_orders_dataset.csv')
customers= pd.read_csv('data/olist_customers_dataset.csv')
payments = pd.read_csv('data/olist_order_payments_dataset.csv')
items    = pd.read_csv('data/olist_order_items_dataset.csv')

# ── STEP 2: Clean and prepare ────────────────────────────────────
# Convert date string to datetime so we can do date math
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_month'] = orders['order_purchase_timestamp'].dt.to_period('M')

# Keep only delivered orders (same logic as your SQL)
orders = orders[orders['order_status'] == 'delivered']

# Merge orders with customer info
df = orders.merge(customers, on='customer_id', how='left')
df = df.merge(payments.groupby('order_id')['payment_value'].sum().reset_index(),
              on='order_id', how='left')

print(f'Loaded {len(df):,} delivered orders from {df.customer_id.nunique():,} customers')

# ── STEP 3: Cohort analysis ──────────────────────────────────────
# Find each customer's first purchase month
first_purchase = df.groupby('customer_id')['order_month'].min().reset_index()
first_purchase.columns = ['customer_id', 'cohort_month']

# Merge cohort month back onto all orders
df = df.merge(first_purchase, on='customer_id')
df['months_since_cohort'] = (df['order_month'] - df['cohort_month']).apply(lambda x: x.n)

# Build cohort retention matrix
cohort_data = df.groupby(['cohort_month', 'months_since_cohort'])['customer_id'].nunique().reset_index()
cohort_pivot = cohort_data.pivot_table(
    index='cohort_month', columns='months_since_cohort', values='customer_id')

# Calculate retention RATE (divide each row by month-0 count)
cohort_size = cohort_pivot.iloc[:, 0]
retention_matrix = cohort_pivot.divide(cohort_size, axis=0).round(3) * 100

# ── STEP 4: Create charts ────────────────────────────────────────
os.makedirs('output', exist_ok=True)
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Product Analytics Dashboard — Parvathy Menon', fontsize=16, fontweight='bold')

# Chart 1: Cohort retention heatmap
ax1 = axes[0, 0]
# Use only first 12 cohorts and first 6 months for clean display
retention_display = retention_matrix.iloc[:12, :6]
sns.heatmap(retention_display, annot=True, fmt='.0f', cmap='YlOrRd_r',
            ax=ax1, cbar_kws={'label': 'Retention %'})
ax1.set_title('Cohort Retention Heatmap (Month 0–5)', fontweight='bold')
ax1.set_xlabel('Months After First Purchase')
ax1.set_ylabel('Cohort Month')

# Chart 2: Monthly Revenue Trend
ax2 = axes[0, 1]
monthly_rev = df.groupby('order_month')['payment_value'].sum()
monthly_rev.index = monthly_rev.index.astype(str)
ax2.bar(monthly_rev.index[-12:], monthly_rev.values[-12:], color='#0E7490')
ax2.set_title('Monthly Revenue (Last 12 Months)', fontweight='bold')
ax2.set_xlabel('Month')
ax2.set_ylabel('Revenue (BRL)')
ax2.tick_params(axis='x', rotation=45)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'R${x/1000:.0f}K'))

# Chart 3: Monthly Active Customers
ax3 = axes[1, 0]
monthly_cust = df.groupby('order_month')['customer_id'].nunique()
monthly_cust.index = monthly_cust.index.astype(str)
ax3.plot(monthly_cust.index[-12:], monthly_cust.values[-12:],
         marker='o', color='#166534', linewidth=2.5, markersize=6)
ax3.fill_between(range(len(monthly_cust.index[-12:])),
                 monthly_cust.values[-12:], alpha=0.1, color='#166534')
ax3.set_title('Monthly Active Customers', fontweight='bold')
ax3.tick_params(axis='x', rotation=45)
ax3.set_xticks(range(len(monthly_cust.index[-12:])))
ax3.set_xticklabels(monthly_cust.index[-12:])

# Chart 4: Customer Lifetime Value Distribution
ax4 = axes[1, 1]
clv = df.groupby('customer_id')['payment_value'].sum()
ax4.hist(clv[clv < clv.quantile(0.95)], bins=40, color='#4C1D95', edgecolor='white')
ax4.axvline(clv.median(), color='red', linestyle='--', label=f'Median CLV: R${clv.median():.0f}')
ax4.set_title('Customer Lifetime Value Distribution', fontweight='bold')
ax4.set_xlabel('Total Customer Spend (BRL)')
ax4.legend()

plt.tight_layout()
plt.savefig('output/product_analytics_dashboard.png', dpi=150, bbox_inches='tight')
print('Saved: output/product_analytics_dashboard.png')

# ── STEP 5: Print executive summary ─────────────────────────────
print('\n=== EXECUTIVE SUMMARY ===')
print(f'Total Customers Analysed: {df.customer_id.nunique():,}')
print(f'Average CLV: R${clv.mean():.2f}')
print(f'Median CLV: R${clv.median():.2f}')
print(f'Month-0 Retention Rate: 100%')
month1 = retention_matrix[1].mean() if 1 in retention_matrix.columns else 0
month3 = retention_matrix[3].mean() if 3 in retention_matrix.columns else 0

print(f'Month-1 Retention Rate: {month1:.1f}%')
print(f'Month-3 Retention Rate: {month3:.1f}%')
