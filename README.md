# 📊 Product Analytics Dashboard — Olist Brazilian E-Commerce

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/sqllite-4169E1?style=flat&logo=sqllite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)

**Tools:** SQL (PostgreSQL) · Python · Pandas · Power BI  
**Dataset:** Olist Brazilian E-Commerce · 99,441 orders · [kaggle.com/olistbr](https://www.kaggle.com/olistbr/brazilian-ecommerce)

---

## 📌 Business Problem

An e-commerce company wants to understand:
- Which customer cohorts have the highest retention?
- Where is churn highest and why?
- What is the average customer lifetime value — and which segments drive it?
- Which Brazilian states generate the most orders?

---

## 📷 Dashboard Preview

<p align="center">
  <img src="output/Power BI dashboard.png" width="900" alt="Product Analytics Dashboard">
</p>

---

## 🔍 Key Findings

| Metric | Value | Insight |
|--------|-------|---------|
| **Total Orders** | 99,441 | Full dataset across Sep 2016 – Oct 2018 |
| **Total Revenue** | R$16.01M | 2-year cumulative across all product categories |
| **Active Customers** | ~100,000 | Unique buyers across the entire period |
| **Average CLV** | R$154.10 | Most customers are single-purchase (low repeat rate) |
| **Revenue Peak** | R$1.19M (Nov 2017) | Black Friday effect — single strongest month |
| **Customer Peak** | ~6,500 (Jan 2018) | Lagged growth following Nov 2017 acquisition spike |
| **Top State** | São Paulo (SP) | Dominant market; RJ, MG, RS, SC follow distantly |

### 📈 Revenue Trend
- Near-zero revenue in Sep–Dec 2016 (platform launch phase)
- Consistent month-on-month growth through 2017 — from R$0.14M (Jan 2017) to R$1.19M (Nov 2017)
- Revenue stabilised at ~R$1.0–1.16M through mid-2018, showing platform maturity
- **Growth rate 2017 vs 2016: ~8x**

### 👥 Customer Retention
- Average CLV of R$154.10 against 99K orders suggests most customers purchase only once
- Customer count peaked Jan 2018 then declined — indicating a **churn problem post-holiday season**, not an acquisition problem
- Retention focus should be on the Jan 2018 cohort (largest) — converting one-time buyers to repeat purchasers is the highest-leverage opportunity

### 🗺️ Geographic Concentration
- **SP (São Paulo)** dominates with the largest bubble on the map
- **RJ, MG, RS, SC** are secondary markets
- Northern and western states (AC, RO, AP) show very low order counts — untapped markets or logistics gaps

### ⚠️ Anomaly Flagged
- September–December 2016 shows R$0.00M revenue — data starts mid-platform launch; exclude from YoY comparisons to avoid skewed growth calculations

---

## 💼 Amazon Parallel

> At Amazon, I built cohort-style retention tracking for compliance KPIs serving 50+ stakeholders. The analytical pattern here is identical — identify the acquisition cohort, track their behaviour over time, and surface where drop-off occurs. The difference is the domain: compliance KPIs vs customer purchases. The SQL and thinking are the same.

---

## 🗂️ Project Structure

```
p1-product-analytics/
├── data/
│   ├── olist_orders_dataset.csv
│   ├── olist_customers_dataset.csv
│   ├── olist_order_items_dataset.csv
│   └── olist_order_payments_dataset.csv
├── sql/
│   ├── cohort_retention.sql        # PostgreSQL — cohort analysis
│   └── churn_rate.sql              # PostgreSQL — monthly churn rate
├── output/
│   └── Power BI dashboard.png      ← dashboard screenshot
├── retention_analysis.py
└── README.md
```

---

## ▶️ How to Run

```bash
# Install dependencies
pip install pandas matplotlib seaborn

# Run the analysis (generates output/product_analytics_dashboard.png)
python retention_analysis.py
```

**SQL queries** — run in DBeaver or any PostgreSQL client:
```bash
# Load CSVs into PostgreSQL first, then:
psql -d your_database -f sql/cohort_retention.sql
psql -d your_database -f sql/churn_rate.sql
```

---

## 👤 Author

**Parvathy Menon**  
Business Intelligence Engineer · 8+ years Amazon  
📧 a.menon.parvathy@gmail.com  
🔗 [linkedin.com/in/parvathymenon-1aa75a100](https://linkedin.com/in/parvathymenon-1aa75a100)  
🐙 [github.com/Parvathyamenon](https://github.com/Parvathyamenon)
