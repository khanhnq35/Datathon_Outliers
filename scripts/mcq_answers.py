"""
Phần 1: Câu hỏi Trắc nghiệm (MCQ) — 10 câu
Owner: Nguyễn Quốc Khánh
Output: 01_mcq_answers.ipynb

Mỗi CELL tương ứng 1 câu hỏi. Copy từng block vào notebook.
"""

# ============================================================
# CELL 0: Setup & Load Data
# ============================================================
import polars as pl
import sys
import os
import warnings

# %matplotlib inline

warnings.filterwarnings("ignore")
sys.path.append(os.path.abspath(os.path.join("..", "src")))
sys.path.append(os.path.abspath("src"))

try:
    from data_loader import DataLoader
except ImportError:
    print("Warning: data_loader module not found.")

loader = DataLoader()

orders = loader.load("orders")
order_items = loader.load("order_items")
customers = loader.load("customers")
products = loader.load("products")
returns = loader.load("returns")
web_traffic = loader.load("web_traffic")
payments = loader.load("payments")
sales = loader.load("sales")

# geography không nằm trong date_columns mapping nên load trực tiếp
geography = pl.read_csv(os.path.join(os.path.abspath("../Data"), "geography.csv"))

print("✅ All data loaded.")
print(f"  orders:      {orders.shape}")
print(f"  order_items: {order_items.shape}")
print(f"  customers:   {customers.shape}")
print(f"  products:    {products.shape}")
print(f"  returns:     {returns.shape}")
print(f"  web_traffic: {web_traffic.shape}")
print(f"  payments:    {payments.shape}")
print(f"  sales:       {sales.shape}")
print(f"  geography:   {geography.shape}")


# ============================================================
# CELL 1: Q1 — Trung vị inter-order gap (ngày)
# ============================================================
# Trong số các khách hàng có >1 đơn, trung vị số ngày giữa 2 lần mua liên tiếp?
# Đáp án: A) 30  B) 90  C) 180  D) 365

print("\n" + "=" * 60)
print("Q1: Trung vị inter-order gap")
print("=" * 60)

# Cast order_date
orders_q1 = orders.with_columns(
    pl.col("order_date").cast(pl.Date)
).sort(["customer_id", "order_date"])

# Tính gap giữa 2 lần mua liên tiếp cho mỗi customer
orders_q1 = orders_q1.with_columns(
    pl.col("order_date").shift(1).over("customer_id").alias("prev_order_date")
)
orders_q1 = orders_q1.filter(pl.col("prev_order_date").is_not_null())
orders_q1 = orders_q1.with_columns(
    (pl.col("order_date") - pl.col("prev_order_date")).dt.total_days().alias("inter_order_gap_days")
)

median_gap = orders_q1["inter_order_gap_days"].median()
mean_gap = orders_q1["inter_order_gap_days"].mean()

print(f"  Median inter-order gap: {median_gap:.1f} days")
print(f"  Mean inter-order gap:   {mean_gap:.1f} days")

if median_gap is not None:
    if abs(median_gap - 30) < 30:
        print("  → Đáp án: A) 30 ngày")
    elif abs(median_gap - 90) < 30:
        print("  → Đáp án: B) 90 ngày")
    elif abs(median_gap - 180) < 45:
        print("  → Đáp án: C) 180 ngày")
    else:
        print("  → Đáp án: D) 365 ngày")


# ============================================================
# CELL 2: Q2 — Segment có tỷ suất lợi nhuận gộp cao nhất
# ============================================================
# (price - cogs) / price theo segment
# Đáp án: A) Premium  B) Performance  C) Activewear  D) Standard

print("\n" + "=" * 60)
print("Q2: Segment có margin cao nhất")
print("=" * 60)

margin_by_segment = products.with_columns(
    ((pl.col("price") - pl.col("cogs")) / pl.col("price")).alias("gross_margin")
).group_by("segment").agg(
    pl.col("gross_margin").mean().alias("avg_gross_margin")
).sort("avg_gross_margin", descending=True)

print(margin_by_segment)
top_segment = margin_by_segment["segment"][0]
top_margin = margin_by_segment["avg_gross_margin"][0]
print(f"  → Segment cao nhất: {top_segment} ({top_margin:.4f})")

answer_map_q2 = {"Premium": "A", "Performance": "B", "Activewear": "C", "Standard": "D"}
print(f"  → Đáp án: {answer_map_q2.get(top_segment, '?')})")


# ============================================================
# CELL 3: Q3 — Lý do trả hàng phổ biến nhất cho Streetwear
# ============================================================
# Join returns + products (product_id), lọc category = Streetwear
# Đáp án: A) defective  B) wrong_size  C) changed_mind  D) not_as_described

print("\n" + "=" * 60)
print("Q3: Top return reason cho Streetwear")
print("=" * 60)

returns_with_product = returns.join(
    products.select(["product_id", "category"]),
    on="product_id",
    how="left",
)

streetwear_returns = returns_with_product.filter(pl.col("category") == "Streetwear")
reason_counts = streetwear_returns.group_by("return_reason").agg(
    pl.count().alias("count")
).sort("count", descending=True)

print(reason_counts)
top_reason = reason_counts["return_reason"][0]
print(f"  → Top reason: {top_reason}")

answer_map_q3 = {"defective": "A", "wrong_size": "B", "changed_mind": "C", "not_as_described": "D"}
print(f"  → Đáp án: {answer_map_q3.get(top_reason, '?')})")


# ============================================================
# CELL 4: Q4 — Traffic source có bounce_rate trung bình thấp nhất
# ============================================================
# Đáp án: A) organic_search  B) paid_search  C) email_campaign  D) social_media

print("\n" + "=" * 60)
print("Q4: Traffic source có bounce rate thấp nhất")
print("=" * 60)

bounce_by_source = web_traffic.group_by("traffic_source").agg(
    pl.col("bounce_rate").mean().alias("avg_bounce_rate")
).sort("avg_bounce_rate")

print(bounce_by_source)
lowest_bounce = bounce_by_source["traffic_source"][0]
print(f"  → Lowest bounce rate: {lowest_bounce}")

answer_map_q4 = {"organic_search": "A", "paid_search": "B", "email_campaign": "C", "social_media": "D"}
print(f"  → Đáp án: {answer_map_q4.get(lowest_bounce, '?')})")


# ============================================================
# CELL 5: Q5 — % order_items có promo_id
# ============================================================
# Đáp án: A) 12%  B) 25%  C) 39%  D) 54%

print("\n" + "=" * 60)
print("Q5: % order_items có promo_id (not null)")
print("=" * 60)

total_items = order_items.height
with_promo = order_items.filter(pl.col("promo_id").is_not_null()).height
pct_promo = with_promo / total_items * 100

print(f"  Total items:    {total_items:,}")
print(f"  With promo_id:  {with_promo:,}")
print(f"  Percentage:     {pct_promo:.1f}%")

if abs(pct_promo - 12) < 5:
    print("  → Đáp án: A) 12%")
elif abs(pct_promo - 25) < 7:
    print("  → Đáp án: B) 25%")
elif abs(pct_promo - 39) < 7:
    print("  → Đáp án: C) 39%")
else:
    print("  → Đáp án: D) 54%")


# ============================================================
# CELL 6: Q6 — Age group có avg orders/customer cao nhất
# ============================================================
# Chỉ xét age_group != null
# Đáp án: A) 55+  B) 25–34  C) 35–44  D) 45–54

print("\n" + "=" * 60)
print("Q6: Age group có avg orders/customer cao nhất")
print("=" * 60)

# Đếm orders theo customer
orders_per_customer = orders.group_by("customer_id").agg(
    pl.count().alias("order_count")
)

# Join với customers
cust_orders = orders_per_customer.join(
    customers.select(["customer_id", "age_group"]),
    on="customer_id",
    how="left",
)

# Lọc age_group != null
cust_orders = cust_orders.filter(pl.col("age_group").is_not_null())

avg_orders_by_age = cust_orders.group_by("age_group").agg(
    pl.col("order_count").mean().alias("avg_orders_per_customer"),
    pl.count().alias("n_customers"),
).sort("avg_orders_per_customer", descending=True)

print(avg_orders_by_age)
top_age = avg_orders_by_age["age_group"][0]
print(f"  → Top age group: {top_age}")

answer_map_q6 = {"55+": "A", "25-34": "B", "35-44": "C", "45-54": "D"}
print(f"  → Đáp án: {answer_map_q6.get(top_age, '?')})")


# ============================================================
# CELL 7: Q7 — Region có tổng doanh thu cao nhất
# ============================================================
# Join geography (zip → region) + sales hoặc orders+payments
# Lưu ý: sales.csv chỉ có Date, Revenue, COGS → không có zip
# → Dùng orders + payments + geography
# Đáp án: A) West  B) Central  C) East  D) Xấp xỉ bằng nhau

print("\n" + "=" * 60)
print("Q7: Region có tổng doanh thu cao nhất")
print("=" * 60)

# Tính revenue từng order
order_revenue = payments.group_by("order_id").agg(
    pl.col("payment_value").sum().alias("order_revenue")
)

orders_rev = orders.join(order_revenue, on="order_id", how="left")

# Join geography qua zip
# Kiểm tra cột trong geography
print(f"  geography columns: {geography.columns}")

if "zip" in geography.columns and "region" in geography.columns:
    orders_geo = orders_rev.join(
        geography.select(["zip", "region"]).unique(),
        on="zip",
        how="left",
    )

    revenue_by_region = orders_geo.group_by("region").agg(
        pl.col("order_revenue").sum().alias("total_revenue")
    ).sort("total_revenue", descending=True)

    print(revenue_by_region)

    if revenue_by_region.height > 0:
        top_region = revenue_by_region["region"][0]
        top_rev = revenue_by_region["total_revenue"][0]

        # Kiểm tra xem các region có xấp xỉ bằng nhau không
        all_revs = revenue_by_region["total_revenue"].to_list()
        if len(all_revs) > 1:
            max_rev = max(all_revs)
            min_rev = min(all_revs)
            spread_pct = (max_rev - min_rev) / max_rev * 100
            print(f"  Revenue spread: {spread_pct:.1f}%")

            if spread_pct < 15:
                print("  → Đáp án: D) Cả ba vùng có doanh thu xấp xỉ bằng nhau")
            else:
                answer_map_q7 = {"West": "A", "Central": "B", "East": "C"}
                print(f"  → Top region: {top_region}")
                print(f"  → Đáp án: {answer_map_q7.get(top_region, '?')})")
else:
    print("  ⚠️ geography.csv không có cột zip hoặc region phù hợp.")
    print(f"  Columns: {geography.columns}")


# ============================================================
# CELL 8: Q8 — Payment method phổ biến nhất trong đơn cancelled
# ============================================================
# Đáp án: A) credit_card  B) cod  C) paypal  D) bank_transfer

print("\n" + "=" * 60)
print("Q8: Payment method phổ biến nhất trong đơn cancelled")
print("=" * 60)

cancelled = orders.filter(pl.col("order_status") == "Cancelled")
print(f"  Cancelled orders: {cancelled.height:,}")

# Dùng payment_method từ chính bảng orders
if "payment_method" in cancelled.columns:
    pm_counts = cancelled.group_by("payment_method").agg(
        pl.count().alias("count")
    ).sort("count", descending=True)

    print(pm_counts)
    top_pm = pm_counts["payment_method"][0]
    print(f"  → Top payment method: {top_pm}")

    answer_map_q8 = {"credit_card": "A", "cod": "B", "paypal": "C", "bank_transfer": "D"}
    print(f"  → Đáp án: {answer_map_q8.get(top_pm, '?')})")
else:
    print("  ⚠️ Không có cột payment_method trong orders.")


# ============================================================
# CELL 9: Q9 — Size nào có tỷ lệ trả hàng cao nhất
# ============================================================
# return rate = count(returns) / count(order_items) per size
# Đáp án: A) S  B) M  C) L  D) XL

print("\n" + "=" * 60)
print("Q9: Size có tỷ lệ trả hàng cao nhất")
print("=" * 60)

# Join order_items + products để lấy size
items_with_size = order_items.join(
    products.select(["product_id", "size"]),
    on="product_id",
    how="left",
)

# Đếm tổng items theo size
items_by_size = items_with_size.group_by("size").agg(
    pl.count().alias("total_items")
)

# Join returns + products để lấy size
returns_with_size = returns.join(
    products.select(["product_id", "size"]),
    on="product_id",
    how="left",
)

returns_by_size = returns_with_size.group_by("size").agg(
    pl.count().alias("return_count")
)

# Merge
return_rate = items_by_size.join(returns_by_size, on="size", how="left")
return_rate = return_rate.with_columns(
    (pl.col("return_count").fill_null(0) / pl.col("total_items") * 100).alias("return_rate_pct")
).sort("return_rate_pct", descending=True)

# Chỉ lọc S, M, L, XL
target_sizes = ["S", "M", "L", "XL"]
return_rate_filtered = return_rate.filter(pl.col("size").is_in(target_sizes)).sort("return_rate_pct", descending=True)

print(return_rate_filtered)

if return_rate_filtered.height > 0:
    top_size = return_rate_filtered["size"][0]
    print(f"  → Highest return rate size: {top_size}")

    answer_map_q9 = {"S": "A", "M": "B", "L": "C", "XL": "D"}
    print(f"  → Đáp án: {answer_map_q9.get(top_size, '?')})")


# ============================================================
# CELL 10: Q10 — Installment nào có avg payment_value cao nhất
# ============================================================
# Đáp án: A) 1  B) 3  C) 6  D) 12

print("\n" + "=" * 60)
print("Q10: Installment plan có avg payment_value cao nhất")
print("=" * 60)

# Tính avg payment_value per order, grouped by installments
# Trước hết tính total payment per order
order_payment = payments.group_by(["order_id", "installments"]).agg(
    pl.col("payment_value").sum().alias("total_payment_per_order")
)

avg_by_installment = order_payment.group_by("installments").agg(
    pl.col("total_payment_per_order").mean().alias("avg_payment_per_order"),
    pl.count().alias("n_orders"),
).sort("installments")

print(avg_by_installment)

# Lọc các mức installment trong đáp án
target_installments = [1, 3, 6, 12]
filtered = avg_by_installment.filter(pl.col("installments").is_in(target_installments))
filtered = filtered.sort("avg_payment_per_order", descending=True)

print("\nFiltered (1, 3, 6, 12 kỳ):")
print(filtered)

if filtered.height > 0:
    top_inst = filtered["installments"][0]
    print(f"  → Highest avg payment: {top_inst} kỳ")

    answer_map_q10 = {1: "A", 3: "B", 6: "C", 12: "D"}
    print(f"  → Đáp án: {answer_map_q10.get(top_inst, '?')})")


# ============================================================
# CELL 11: Summary — Tổng hợp đáp án
# ============================================================
print("\n" + "=" * 60)
print("📝 TỔNG HỢP ĐÁP ÁN MCQ")
print("=" * 60)
print("""
Chạy từng cell ở trên để xác nhận đáp án chính xác từ dữ liệu.
Sau khi chạy xong, điền đáp án vào form nộp bài.

Lưu ý:
- Các đáp án được tự động xác định dựa trên kết quả tính toán.
- Nên kiểm tra lại kết quả output trước khi nộp.
""")
