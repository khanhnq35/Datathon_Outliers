import nbformat as nbf
import os

def create_retention_notebook():
    nb = nbf.v4.new_notebook()
    
    # Notebook Metadata
    nb['metadata'] = {
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'name': 'python',
            'version': '3.10'
        }
    }

    cells = []

    # Title
    cells.append(nbf.v4.new_markdown_cell("# Module ❷: Khách hàng & Retention Analysis\\n\\n**Mục tiêu**: Phân tích hành vi mua hàng lặp lại, mức độ trung thành và phân khúc khách hàng theo giá trị.\\n\\n---"))

    # Setup
    cells.append(nbf.v4.new_markdown_cell("## 1. Setup & Load Data"))
    cells.append(nbf.v4.new_code_cell(
        "import polars as pl\\n"
        "import pandas as pd\\n"
        "import matplotlib.pyplot as plt\\n"
        "import seaborn as sns\\n"
        "import sys\\n"
        "from pathlib import Path\\n\\n"
        "# Thêm src vào path để load DataLoader\\n"
        "sys.path.append(str(Path('..').resolve()))\\n"
        "from src.data_loader import DataLoader\\n\\n"
        "sns.set_theme(style='whitegrid')\\n"
        "plt.rcParams['figure.figsize'] = (12, 6)\\n\\n"
        "loader = DataLoader()\\n"
        "orders = loader.load('orders')\\n"
        "customers = loader.load('customers')\\n"
        "payments = loader.load('payments')\\n\\n"
        "print(f\\\"Orders: {len(orders):,}\\\")\\n"
        "print(f\\\"Customers: {len(customers):,}\\\")\\n"
        "print(f\\\"Payments: {len(payments):,}\\\")"
    ))

    # Repeat Purchase Rate
    cells.append(nbf.v4.new_markdown_cell("## 2. Repeat Purchase Rate (Tỷ lệ mua hàng lặp lại)"))
    cells.append(nbf.v4.new_code_cell(
        "# Đếm số đơn hàng của mỗi khách hàng\\n"
        "purchase_counts = orders.group_by('customer_id').agg([\\n"
        "    pl.count('order_id').alias('order_count')\\n"
        "])\\n\\n"
        "# Tính số lượng khách hàng mua lặp lại (>1 đơn)\\n"
        "total_customers = purchase_counts.height\\n"
        "repeat_customers = purchase_counts.filter(pl.col('order_count') > 1).height\\n"
        "repeat_rate = (repeat_customers / total_customers) * 100\\n\\n"
        "print(f\\\"Tổng số khách hàng: {total_customers:,}\\\")\\n"
        "print(f\\\"Số khách hàng mua lặp lại: {repeat_customers:,}\\\")\\n"
        "print(f\\\"Tỷ lệ mua lặp lại: {repeat_rate:.2f}%\\\")\\n\\n"
        "# Trực quan hóa phân phối số đơn hàng\\n"
        "sns.countplot(data=purchase_counts.to_pandas(), x='order_count')\\n"
        "plt.title('Phân phối số lượng đơn hàng trên mỗi khách hàng')\\n"
        "plt.xlabel('Số đơn hàng')\\n"
        "plt.ylabel('Số lượng khách hàng')\\n"
        "plt.show()"
    ))

    # Cohort Analysis
    cells.append(nbf.v4.new_markdown_cell("## 3. Cohort Retention Analysis\\n\\nPhân tích tỷ lệ duy trì khách hàng dựa trên tháng mua hàng đầu tiên."))
    cells.append(nbf.v4.new_code_cell(
        "# 1. Xác định tháng mua hàng đầu tiên của mỗi khách hàng (Cohort Month)\\n"
        "cohort_data = orders.group_by('customer_id').agg([\\n"
        "    pl.col('order_date').min().alias('first_order_date')\\n"
        "])\\n\\n"
        "# 2. Join lại với bảng orders\\n"
        "orders_cohort = orders.join(cohort_data, on='customer_id')\\n\\n"
        "# 3. Tính Cohort Month và Order Month (dưới dạng yyyy-mm)\\n"
        "orders_cohort = orders_cohort.with_columns([\\n"
        "    pl.col('first_order_date').dt.truncate('1mo').alias('cohort_month'),\\n"
        "    pl.col('order_date').dt.truncate('1mo').alias('order_month')\\n"
        "])\\n\\n"
        "# 4. Tính khoảng cách (index) theo tháng giữa đơn hàng và cohort\\n"
        "def diff_months(col_end, col_start):\\n"
        "    return (col_end.dt.year() - col_start.dt.year()) * 12 + (col_end.dt.month() - col_start.dt.month())\\n\\n"
        "orders_cohort = orders_cohort.with_columns([\\n"
        "    diff_months(pl.col('order_month'), pl.col('cohort_month')).alias('cohort_index')\\n"
        "])\\n\\n"
        "# 5. Nhóm dữ liệu để tính số lượng khách hàng active trong mỗi cohort index\\n"
        "cohort_counts = orders_cohort.group_by(['cohort_month', 'cohort_index']).agg([\\n"
        "    pl.col('customer_id').n_unique().alias('active_customers')\\n"
        "]).sort(['cohort_month', 'cohort_index'])\\n\\n"
        "# 6. Pivot table để tạo ma trận retention\\n"
        "retention_matrix = cohort_counts.to_pandas().pivot(index='cohort_month', columns='cohort_index', values='active_customers')\\n\\n"
        "# 7. Chuyển sang tỷ lệ %\\n"
        "cohort_sizes = retention_matrix.iloc[:, 0]\\n"
        "retention_percentage = retention_matrix.divide(cohort_sizes, axis=0) * 100\\n\\n"
        "# 8. Vẽ Heatmap (Lọc bớt các cohort quá cũ nếu cần)\\n"
        "plt.figure(figsize=(16, 10))\\n"
        "sns.heatmap(retention_percentage, annot=True, fmt='.1f', cmap='YlGnBu')\\n"
        "plt.title('Cohort Retention Matrix (%)')\\n"
        "plt.ylabel('Cohort Month')\\n"
        "plt.xlabel('Months Since First Purchase')\\n"
        "plt.show()"
    ))

    # RFM Segmentation
    cells.append(nbf.v4.new_markdown_cell("## 4. RFM Segmentation\\n\\nPhân khúc khách hàng dựa trên Recency, Frequency, và Monetary."))
    cells.append(nbf.v4.new_code_cell(
        "# 1. Chuẩn bị dữ liệu RFM\\n"
        "# Cần join orders với payments để có giá trị đơn hàng\\n"
        "order_payments = orders.join(payments, on='order_id')\\n\\n"
        "current_date = orders['order_date'].max() + pl.duration(days=1)\\n\\n"
        "rfm = order_payments.group_by('customer_id').agg([\\n"
        "    ((current_date - pl.col('order_date').max()).dt.total_days()).alias('recency'),\\n"
        "    pl.col('order_id').n_unique().alias('frequency'),\\n"
        "    pl.col('payment_value').sum().alias('monetary')\\n"
        "])\\n\\n"
        "# 2. Tính điểm R, F, M (Quantiles)\\n"
        "# Chuyển sang pandas để dùng qcut dễ hơn cho bài toán này\\n"
        "rfm_pd = rfm.to_pandas()\\n"
        "rfm_pd['r_score'] = pd.qcut(rfm_pd['recency'], 5, labels=[5, 4, 3, 2, 1])\\n"
        "rfm_pd['f_score'] = pd.qcut(rfm_pd['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])\\n"
        "rfm_pd['m_score'] = pd.qcut(rfm_pd['monetary'], 5, labels=[1, 2, 3, 4, 5])\\n\\n"
        "# 3. Tính RFM Score\\n"
        "rfm_pd['rfm_score'] = rfm_pd['r_score'].astype(str) + rfm_pd['f_score'].astype(str) + rfm_pd['m_score'].astype(str)\\n\\n"
        "# 4. Phân khúc (Ví dụ đơn giản)\\n"
        "def segment_customer(df):\\n"
        "    r = int(df['r_score'])\\n"
        "    f = int(df['f_score'])\\n"
        "    if r >= 4 and f >= 4:\\n"
        "        return 'Champions'\\n"
        "    if r >= 3 and f >= 3:\\n"
        "        return 'Loyal Customers'\\n"
        "    if r >= 4 and f <= 2:\\n"
        "        return 'New Customers'\\n"
        "    if r <= 2 and f >= 4:\\n"
        "        return 'At Risk'\\n"
        "    if r <= 2 and f <= 2:\\n"
        "        return 'Lost'\\n"
        "    return 'Potential Loyalist'\\n\\n"
        "rfm_pd['segment'] = rfm_pd.apply(segment_customer, axis=1)\\n\\n"
        "# 5. Trực quan hóa phân khúc\\n"
        "segment_counts = rfm_pd['segment'].value_counts()\\n"
        "plt.figure(figsize=(10, 6))\\n"
        "segment_counts.plot(kind='bar', color='skyblue')\\n"
        "plt.title('Phân khúc khách hàng RFM')\\n"
        "plt.xlabel('Phân khúc')\\n"
        "plt.ylabel('Số lượng khách hàng')\\n"
        "plt.xticks(rotation=45)\\n"
        "plt.show()"
    ))

    # Summary
    cells.append(nbf.v4.new_markdown_cell("## 5. Kết luận sơ bộ (Key Insights)\\n\\n- **Repeat Rate**: ...\\n- **Retention**: Nhóm cohort tháng ... có tỷ lệ duy trì tốt nhất.\\n- **RFM**: Tỷ lệ khách hàng 'At Risk' là ... cần có chiến dịch Win-back."))

    nb['cells'] = cells

    with open('notebooks/02_M2_customer_retention.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

if __name__ == '__main__':
    create_retention_notebook()
