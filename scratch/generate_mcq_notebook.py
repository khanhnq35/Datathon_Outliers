import json
import os

notebook = {
    'cells': [
        {
            'cell_type': 'markdown',
            'id': '51fd1aea',
            'metadata': {},
            'source': ['# 🧠 Giải MCQ Answers (Optimized with Polars)']
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': '2baad924',
            'metadata': {},
            'outputs': [],
            'source': [
                'import polars as pl\n',
                'import sys\n',
                'import os\n',
                '# Thêm thư mục gốc vào path để import DataLoader\n',
                'sys.path.append(os.path.abspath(".."))\n',
                'from src.data_loader import DataLoader'
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': 'b0c096ec',
            'metadata': {},
            'outputs': [],
            'source': [
                '# Khởi tạo loader và tải dữ liệu\n',
                'loader = DataLoader(data_dir="Data")\n',
                'dfs = loader.load_all()'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': '16414421',
            'metadata': {},
            'source': ['### Q1: Trung vị số ngày giữa hai lần mua liên tiếp']
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': 'eb7ad919',
            'metadata': {},
            'outputs': [],
            'source': [
                '# Sắp xếp theo khách hàng và ngày\n',
                'orders_sorted = dfs["orders"].sort(["customer_id", "order_date"])\n',
                '\n',
                '# Tính chênh lệch ngày giữa các đơn liên tiếp của cùng một khách hàng\n',
                'df_diff = orders_sorted.with_columns(\n',
                '    diff_days = pl.col("order_date").diff().over("customer_id").dt.total_days()\n',
                ')\n',
                '\n',
                '# Tính trung vị\n',
                'median_gap = df_diff.select(pl.col("diff_days").median()).to_series()[0]\n',
                'print(f"Q1 Answer: {median_gap} ngày")'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': 'd9fed56c',
            'metadata': {},
            'source': ['### Q2: Tỷ suất lợi nhuận gộp trung bình theo segment']
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': '9b81da3b',
            'metadata': {},
            'outputs': [],
            'source': [
                'products = dfs["products"]\n',
                'margin_by_segment = (\n',
                '    products.with_columns(\n',
                '        margin = (pl.col("price") - pl.col("cogs")) / pl.col("price")\n',
                '    )\n',
                '    .group_by("segment")\n',
                '    .agg(pl.col("margin").mean())\n',
                '    .sort("margin", descending=True)\n',
                ')\n',
                'print("Q2 Answer:")\n',
                'print(margin_by_segment)'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': 'c8ca814c',
            'metadata': {},
            'source': ['### Q3: Lý do trả hàng nhiều nhất cho danh mục Streetwear']
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': 'cb1f1138',
            'metadata': {},
            'outputs': [],
            'source': [
                'returns = dfs["returns"]\n',
                'products = dfs["products"]\n',
                '\n',
                'streetwear_returns = (\n',
                '    returns.join(products, on="product_id")\n',
                '    .filter(pl.col("category") == "Streetwear")\n',
                '    .group_by("return_reason")\n',
                '    .agg(pl.count().alias("count"))\n',
                '    .sort("count", descending=True)\n',
                ')\n',
                'print("Q3 Answer:")\n',
                'print(streetwear_returns)'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': '99a2a82a',
            'metadata': {},
            'source': ['### Q4: Nguồn traffic có tỷ lệ thoát trung bình thấp nhất']
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': '30446346',
            'metadata': {},
            'outputs': [],
            'source': [
                'web_traffic = dfs["web_traffic"]\n',
                'bounce_by_source = (\n',
                '    web_traffic.group_by("traffic_source")\n',
                '    .agg(pl.col("bounce_rate").mean())\n',
                '    .sort("bounce_rate")\n',
                ')\n',
                'print("Q4 Answer:")\n',
                'print(bounce_by_source)'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': '01ea2a6e',
            'metadata': {},
            'source': ['### Q5: Tỷ lệ order_items có khuyến mãi']
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': '414929bb',
            'metadata': {},
            'outputs': [],
            'source': [
                'order_items = dfs["order_items"]\n',
                'total_items = order_items.height\n',
                'promo_items = order_items.filter(pl.col("promo_id").is_not_null()).height\n',
                'promo_ratio = (promo_items / total_items) * 100\n',
                'print(f"Q5 Answer: {promo_ratio:.2f}%")'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': 'd36f7e8d',
            'metadata': {},
            'source': ['### Q6: Nhóm tuổi có số đơn hàng trung bình cao nhất']
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': '33cf2362',
            'metadata': {},
            'outputs': [],
            'source': [
                'orders = dfs["orders"]\n',
                'customers = dfs["customers"]\n',
                '\n',
                'order_counts = orders.group_by("customer_id").agg(pl.count().alias("order_count"))\n',
                '\n',
                'age_group_orders = (\n',
                '    customers.join(order_counts, on="customer_id", how="left")\n',
                '    .fill_null(0)\n',
                '    .filter(pl.col("age_group").is_not_null())\n',
                '    .group_by("age_group")\n',
                '    .agg(pl.col("order_count").mean())\n',
                '    .sort("order_count", descending=True)\n',
                ')\n',
                'print("Q6 Answer:")\n',
                'print(age_group_orders)'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': 'a9bf0efd',
            'metadata': {},
            'source': ['### Q7: Vùng có doanh thu cao nhất']
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': 'edf0accc',
            'metadata': {},
            'outputs': [],
            'source': [
                'order_items = dfs["order_items"]\n',
                'orders = dfs["orders"]\n',
                'geography = dfs["geography"]\n',
                '\n',
                'item_revenue = order_items.with_columns(\n',
                '    revenue = pl.col("quantity") * pl.col("unit_price")\n',
                ')\n',
                '\n',
                'region_revenue = (\n',
                '    item_revenue.join(orders, on="order_id")\n',
                '    .join(geography, on="zip")\n',
                '    .group_by("region")\n',
                '    .agg(pl.col("revenue").sum())\n',
                '    .sort("revenue", descending=True)\n',
                ')\n',
                'print("Q7 Answer:")\n',
                'print(region_revenue)'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': 'f0504018',
            'metadata': {},
            'source': ['### Q8: Phương thức thanh toán nhiều nhất trong đơn huỷ']
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': 'b7c2554b',
            'metadata': {},
            'outputs': [],
            'source': [
                'orders = dfs["orders"]\n',
                'payments = dfs["payments"]\n',
                '\n',
                'cancelled_orders = orders.filter(pl.col("order_status") == "cancelled")\n',
                '\n',
                'top_payment = (\n',
                '    cancelled_orders.join(payments, on="order_id")\n',
                '    .group_by("payment_method")\n',
                '    .agg(pl.count().alias("count"))\n',
                '    .sort("count", descending=True)\n',
                ')\n',
                'print("Q8 Answer:")\n',
                'print(top_payment)'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': 'f643d228',
            'metadata': {},
            'source': ['### Q9: Kích thước sản phẩm có tỷ lệ trả hàng cao nhất']
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': '286f1a8b',
            'metadata': {},
            'outputs': [],
            'source': [
                'order_items = dfs["order_items"]\n',
                'returns = dfs["returns"]\n',
                'products = dfs["products"]\n',
                '\n',
                'size_sales = (\n',
                '    order_items.join(products.select(["product_id", "size"]), on="product_id")\n',
                '    .group_by("size")\n',
                '    .agg(pl.count().alias("sale_count"))\n',
                ')\n',
                '\n',
                'size_returns = (\n',
                '    returns.join(products.select(["product_id", "size"]), on="product_id")\n',
                '    .group_by("size")\n',
                '    .agg(pl.count().alias("return_count"))\n',
                ')\n',
                '\n',
                'return_ratio = (\n',
                '    size_sales.join(size_returns, on="size")\n',
                '    .with_columns(\n',
                '        ratio = pl.col("return_count") / pl.col("sale_count")\n',
                '    )\n',
                '    .sort("ratio", descending=True)\n',
                ')\n',
                'print("Q9 Answer:")\n',
                'print(return_ratio)'
            ]
        },
        {
            'cell_type': 'markdown',
            'id': '4dd3400e',
            'metadata': {},
            'source': ['### Q10: Kế hoạch trả góp có giá trị thanh toán trung bình cao nhất']
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'id': '30739978',
            'metadata': {},
            'outputs': [],
            'source': [
                'payments = dfs["payments"]\n',
                'avg_payment_installments = (\n',
                '    payments.group_by("installments")\n',
                '    .agg(pl.col("payment_value").mean())\n',
                '    .sort("payment_value", descending=True)\n',
                ')\n',
                'print("Q10 Answer:")\n',
                'print(avg_payment_installments)\n',
                'print("--- HOÀN THÀNH ---")'
            ]
        }
    ],
    'metadata': {
        'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
        'language_info': {'name': 'python', 'version': '3'}
    },
    'nbformat': 4,
    'nbformat_minor': 5
}

with open(r'd:\Datathon_Outliers\notebooks\01_mcq_answers.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)
