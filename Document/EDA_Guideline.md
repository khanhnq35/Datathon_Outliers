# 📊 EDA Guideline — Datathon 2026

> **Mục tiêu**: Đạt tối đa **60/60 điểm** EDA bằng cách bao phủ đầy đủ 4 cấp độ phân tích và kết nối insights với giá trị kinh doanh thực tế.

---

## Rubric chấm điểm (nhắc lại)

| Tiêu chí | Điểm tối đa | Yêu cầu cốt lõi |
|----------|-------------|-------------------|
| Chất lượng trực quan | 15 | Biểu đồ chuẩn, nhãn trục, chú thích, thẩm mỹ |
| Chiều sâu phân tích | 25 | Đạt 4 cấp: Descriptive → Diagnostic → Predictive → Prescriptive |
| Insight kinh doanh | 15 | Phát hiện thực tiễn, đề xuất hành động cụ thể, có số liệu |
| Tính sáng tạo | 5 | Góc nhìn độc đáo, kết hợp nhiều nguồn dữ liệu, storytelling |

---

## Quy tắc trình bày biểu đồ

Mỗi biểu đồ trong report **bắt buộc** phải có:
1. **Tiêu đề** rõ ràng, mô tả nội dung (không chung chung như "Biểu đồ 1")
2. **Nhãn trục X, Y** với đơn vị (VND, ngày, %, số lượng...)
3. **Chú thích (legend)** nếu có nhiều series
4. **Annotation** trên các điểm nổi bật (peak, anomaly, milestone)
5. **Nguồn dữ liệu** ghi chú bên dưới (ví dụ: "Nguồn: orders.csv ↔ payments.csv")

**Palette màu thống nhất**: Chọn 1 palette và dùng xuyên suốt (ví dụ: `seaborn="Set2"` hoặc custom palette).

---

## Cấu trúc EDA đề xuất

---

### Cấp 1: DESCRIPTIVE — "Chuyện gì đã xảy ra?"
> Mô tả tổng quan bức tranh kinh doanh qua dữ liệu.

#### 1.1 Tổng quan doanh thu theo thời gian
- **Dữ liệu**: `sales.csv` (3,834 dòng, daily từ 07/2012 → 12/2022)
- **Biểu đồ**:
  - Line chart: Revenue & COGS theo ngày/tuần/tháng
  - Bar chart: Revenue theo năm, so sánh YoY growth
  - Area chart: Gross Profit = Revenue − COGS theo thời gian
- **Insight tiềm năng**: Xu hướng tăng trưởng, tính seasonality (Tết, Black Friday, 11/11), COVID impact (2020-2021)

#### 1.2 Phân bố đơn hàng
- **Dữ liệu**: `orders.csv` (646,946 đơn) ↔ `geography.csv`
- **Biểu đồ**:
  - Bar chart: Số đơn hàng theo `region` (East/Central/West)
  - Heatmap: Số đơn hàng theo tháng × năm
  - Pie chart: Tỷ lệ `order_status` (delivered, cancelled, returned, shipped)
  - Bar chart: Phân bố theo `device_type` và `order_source`
- **Insight tiềm năng**: Vùng nào mạnh nhất? Kênh bán hàng nào hiệu quả? Mobile vs Desktop trend qua các năm?

#### 1.3 Chân dung khách hàng
- **Dữ liệu**: `customers.csv` (121,931 KH) ↔ `orders.csv`
- **Biểu đồ**:
  - Bar chart: Phân bố khách hàng theo `age_group`, `gender`
  - Bar chart: Số KH theo `acquisition_channel`
  - Histogram: Phân bố số đơn hàng trên mỗi KH
- **Insight tiềm năng**: Nhóm tuổi nào đông nhất? Tỷ lệ KH mua lại (repeat rate)?

#### 1.4 Danh mục sản phẩm
- **Dữ liệu**: `products.csv` (2,413 SP) ↔ `order_items.csv` (714,670 dòng)
- **Biểu đồ**:
  - Treemap: Doanh thu theo category → segment
  - Bar chart: Top 10 sản phẩm bán chạy nhất
  - Box plot: Phân bố giá (`price`) và margin (`price - cogs`) theo segment
- **Insight tiềm năng**: Segment nào có margin cao nhất? Category nào chiếm tỷ trọng doanh thu lớn nhất?

---

### Cấp 2: DIAGNOSTIC — "Tại sao điều đó xảy ra?"
> Đào sâu nguyên nhân gốc rễ bằng cách kết nối nhiều bảng dữ liệu.

#### 2.1 Phân tích trả hàng — Root Cause Analysis
- **Dữ liệu**: `returns.csv` (39,940 dòng) ↔ `products.csv` ↔ `orders.csv`
- **Biểu đồ**:
  - Stacked bar: Return rate theo `category` × `return_reason`
  - Heatmap: Return rate theo `size` × `category`
  - Line chart: Return rate trend theo thời gian
- **Câu hỏi cần trả lời**:
  - Tại sao `wrong_size` chiếm nhiều? → Sản phẩm nào? Size nào?
  - Category nào có return rate cao bất thường?
  - Return rate tăng hay giảm qua các năm? Tại sao?
- **Business insight**: Đề xuất cải thiện size guide, QC cho category có defect rate cao

#### 2.2 Hiệu quả khuyến mãi
- **Dữ liệu**: `promotions.csv` (50 chiến dịch) ↔ `order_items.csv` ↔ `orders.csv`
- **Biểu đồ**:
  - Grouped bar: AOV (Average Order Value) có KM vs. không KM
  - Scatter plot: `discount_value` vs. số đơn hàng (demand elasticity)
  - Timeline: Doanh thu trước/trong/sau mỗi chiến dịch KM
- **Câu hỏi cần trả lời**:
  - KM `percentage` hay `fixed` hiệu quả hơn?
  - KM có thực sự tăng doanh thu hay chỉ "kéo" doanh thu từ trước/sau?
  - `stackable_flag` ảnh hưởng thế nào đến discount amount?
- **Business insight**: ROI thực sự của chiến dịch KM, đề xuất loại KM nên ưu tiên

#### 2.3 Tác động của tồn kho đến doanh thu
- **Dữ liệu**: `inventory.csv` (60,248 dòng) ↔ `sales.csv`
- **Biểu đồ**:
  - Dual-axis: Doanh thu vs. stockout_days theo tháng
  - Scatter plot: `fill_rate` vs. revenue per product
  - Bar chart: Lost sales estimation khi `stockout_flag = 1`
- **Câu hỏi cần trả lời**:
  - Stockout gây mất bao nhiêu doanh thu?
  - Sản phẩm nào bị overstock nặng nhất (lãng phí vốn)?
- **Business insight**: Đề xuất reorder point, safety stock level

#### 2.4 Web Traffic → Conversion Funnel
- **Dữ liệu**: `web_traffic.csv` (3,653 dòng) ↔ `sales.csv`
- **Biểu đồ**:
  - Dual-axis: Sessions vs. Revenue theo ngày
  - Funnel chart: Sessions → Unique visitors → Conversion
  - Bar chart: `bounce_rate` và `conversion_rate` theo `traffic_source`
- **Câu hỏi cần trả lời**:
  - Kênh nào có conversion rate tốt nhất?
  - Bounce rate cao ở kênh nào? Tại sao?
  - Có correlation giữa `avg_session_duration` và conversion không?
- **Business insight**: Đề xuất phân bổ ngân sách marketing theo kênh

---

### Cấp 3: PREDICTIVE — "Điều gì sẽ xảy ra tiếp?"
> Dùng mô hình đơn giản để dự đoán xu hướng tương lai.

#### 3.1 Customer Lifetime Value (CLV) Prediction
- **Dữ liệu**: `customers.csv` ↔ `orders.csv` ↔ `payments.csv`
- **Phương pháp**: RFM (Recency, Frequency, Monetary) scoring → phân nhóm KH
- **Biểu đồ**:
  - 3D scatter: R × F × M colored by segment
  - Bar chart: Projected CLV theo segment
- **Insight**: Nhóm KH nào có giá trị cao nhất? Dự báo revenue từ mỗi nhóm?

#### 3.2 Churn Risk Analysis
- **Dữ liệu**: `customers.csv` ↔ `orders.csv` (tính inter-order gap)
- **Phương pháp**: Xác suất churn dựa trên thời gian kể từ đơn hàng cuối
- **Biểu đồ**:
  - Survival curve: Xác suất KH quay lại theo thời gian
  - Bar chart: Churn rate theo `age_group`, `acquisition_channel`
- **Insight**: Bao nhiêu KH có nguy cơ rời bỏ? Nhóm nào cần can thiệp?

#### 3.3 Seasonal Demand Forecasting (mini)
- **Dữ liệu**: `sales.csv` + `inventory.csv`
- **Phương pháp**: Decomposition (trend + seasonality + residual)
- **Biểu đồ**:
  - Decomposition plot: Tách trend, seasonal, residual
  - Prediction interval cho 3-6 tháng tới
- **Insight**: Dự báo nhu cầu theo quý, đề xuất nhập hàng

---

### Cấp 4: PRESCRIPTIVE — "Nên làm gì?"
> Đề xuất hành động cụ thể, có số liệu, áp dụng được ngay.

#### 4.1 Tối ưu danh mục sản phẩm
- **Phân tích**: BCG Matrix (Market share × Growth) cho từng category
- **Đề xuất**:
  - **Stars**: Tiếp tục đầu tư, mở rộng (segment nào?)
  - **Cash cows**: Duy trì, tối ưu margin
  - **Dogs**: Cân nhắc loại bỏ, giải phóng tồn kho
  - **Question marks**: Thử nghiệm thêm

#### 4.2 Chiến lược khuyến mãi tối ưu
- **Đề xuất** (dựa trên dữ liệu thực):
  - Thời điểm chạy KM hiệu quả nhất (dựa trên seasonality)
  - Mức discount tối ưu (maximize revenue, không phải maximize đơn hàng)
  - Category nào nên ưu tiên KM (cao return vs. thấp margin)

#### 4.3 Cải thiện trải nghiệm khách hàng
- **Đề xuất**:
  - Cải thiện size guide cho category có `wrong_size` return rate cao
  - Tăng cường QC cho segment có `defective` return rate cao
  - Xây dựng chương trình loyalty cho KH có CLV cao nhưng đang có dấu hiệu churn

#### 4.4 Tối ưu vận hành & logistics
- **Đề xuất**:
  - Reorder points cho top products (dựa trên `days_of_supply`)
  - Tối ưu phân bổ kho theo region (based on demand heatmap)
  - Giảm delivery time: phân tích `ship_date → delivery_date` gap theo vùng

---

## 🔗 Ma trận kết nối dữ liệu — Ý tưởng cross-table

Sức mạnh của EDA nằm ở việc kết nối NHIỀU bảng. Dưới đây là các cặp kết hợp giá trị:

| Kết hợp | Join Key | Insight tiềm năng |
|---------|----------|-------------------|
| `orders` ↔ `customers` ↔ `geography` | `customer_id`, `zip` | Phân bố doanh thu theo vùng, thành phố |
| `order_items` ↔ `products` ↔ `returns` | `product_id` | Return rate theo category, size, color |
| `orders` ↔ `payments` | `order_id` | Phương thức thanh toán ảnh hưởng đến cancellation? |
| `orders` ↔ `shipments` | `order_id` | Delivery time vs. review rating |
| `shipments` ↔ `reviews` ↔ `returns` | `order_id` | Late delivery → bad review → return? |
| `web_traffic` ↔ `sales` | `date` | Traffic → Revenue correlation |
| `promotions` ↔ `order_items` ↔ `sales` | `promo_id`, `date` | KM impact on daily revenue |
| `inventory` ↔ `sales` ↔ `products` | `product_id`, date | Stockout → lost sales analysis |
| `customers` ↔ `orders` (self-join) | `customer_id` | Repeat purchase pattern, cohort analysis |

---

## 📝 Template viết narrative cho mỗi biểu đồ

```
### [Tên phân tích]

**Biểu đồ**: [Loại biểu đồ] — [Tiêu đề cụ thể]

**Mô tả**: Biểu đồ này thể hiện [gì], sử dụng dữ liệu từ [bảng nào],
trong giai đoạn [thời gian].

**Phát hiện chính**:
1. [Phát hiện 1] — cụ thể bằng số liệu (ví dụ: "Category X chiếm 45% tổng doanh thu")
2. [Phát hiện 2]
3. [Phát hiện 3]

**Ý nghĩa kinh doanh**: [Phát hiện này có nghĩa gì cho doanh nghiệp?]

**Đề xuất hành động**: [Cụ thể, khả thi, có thể đo lường được]
```

---

## ⚡ Gợi ý EDA sáng tạo (5đ tính sáng tạo)

Những ý tưởng nổi bật để ghi điểm tiêu chí "Tính sáng tạo":

1. **Cohort Analysis**: Theo dõi hành vi mua hàng của KH theo tháng đăng ký (retention curve)
2. **Market Basket Analysis**: Sản phẩm nào thường được mua cùng nhau? (association rules)
3. **Price Sensitivity Analysis**: Elasticity — tăng giá 10% thì demand giảm bao nhiêu %?
4. **Geographic Heatmap**: Bản đồ Việt Nam thể hiện doanh thu theo thành phố/vùng
5. **Day-of-week / Hour pattern**: Thời điểm nào trong tuần/ngày bán hàng tốt nhất?
6. **Payment Behavior**: Mối quan hệ giữa installments (trả góp) vs. order value vs. age_group
7. **Review Sentiment vs. Return**: Rating thấp có dẫn đến return không?
8. **Promo Cannibalization**: KM có "ăn" doanh thu của tuần trước/sau không?

---

## 🚀 Thứ tự thực hiện khuyến nghị

| Ưu tiên | Phân tích | Lý do |
|---------|-----------|-------|
| 1 | Revenue Overview (1.1) | Nền tảng, bắt buộc phải có |
| 2 | Return Analysis (2.1) | Cross-table, diagnostic depth |
| 3 | Customer RFM (3.1) | Predictive level |
| 4 | Promo Effectiveness (2.2) | Diagnostic + Prescriptive |
| 5 | Web Traffic Funnel (2.4) | Creative cross-data |
| 6 | Inventory Impact (2.3) | Operational insight |
| 7 | Product Portfolio (4.1) | Prescriptive BCG |
| 8 | Cohort / Churn (3.2) | Creative + Predictive |

---

## ⚠️ Lưu ý quan trọng khi thực hiện EDA

### 1. Kiểm tra chất lượng dữ liệu trước khi phân tích

- **Null values**: `customers.csv` có nhiều cột nullable (`gender`, `age_group`, `acquisition_channel`). Khi tính trung bình hoặc phân bố, phải ghi rõ "loại bỏ N dòng null" hoặc xử lý riêng nhóm unknown.
- **Duplicates**: Kiểm tra xem `order_id` trong `orders.csv` (646,946 dòng) có thực sự unique không. Tương tự cho `customer_id`.
- **Data type**: Các cột `date` có thể được đọc thành `string` — luôn convert sang `datetime` trước khi phân tích time series.
- **Outliers**: `products.csv` có sản phẩm giá rất thấp (ví dụ product_id 543 giá chỉ ~40 VND) → cần quyết định giữ hay loại, và ghi chú rõ trong report.
- **Consistency**: Kiểm tra `orders.order_status` có bao nhiêu giá trị unique? Có giá trị nào viết sai chính tả không?

### 2. Tránh những lỗi phân tích phổ biến

- **Survivorship bias**: Khi phân tích KH mua lại, đừng quên nhóm KH chỉ mua 1 lần (có thể chiếm >50%). Họ cũng là insight quan trọng.
- **Simpson's paradox**: Một trend có thể đúng ở tổng thể nhưng ngược lại khi chia theo segment. Luôn drill-down kiểm tra.
- **Correlation ≠ Causation**: Web traffic tăng cùng lúc với doanh thu không có nghĩa traffic *gây ra* doanh thu. Có thể cả hai đều bị ảnh hưởng bởi mùa lễ hội.
- **Leakage thời gian**: Khi phân tích predictive, không được dùng dữ liệu tương lai để giải thích quá khứ. Ví dụ: dùng `review_date` xảy ra SAU `order_date` để dự đoán đơn hàng.
- **Tỷ lệ vs. Tuyệt đối**: "Category X có return rate 30%" nghe nghiêm trọng, nhưng nếu chỉ có 10 đơn hàng thì không đáng kể. Luôn kèm sample size.

### 3. Kỹ thuật viết report hiệu quả (4 trang giới hạn)

- **Không liệt kê biểu đồ**: Report không phải notebook. Chỉ chọn **5-7 biểu đồ sắc bén nhất**, mỗi biểu đồ phải phục vụ một insight rõ ràng.
- **Mỗi biểu đồ = 1 câu chuyện**: Đọc biểu đồ → hiểu ngay phát hiện chính → biết doanh nghiệp nên làm gì.
- **Dùng số liệu cụ thể**: Thay vì "doanh thu tăng đáng kể", viết "doanh thu tăng 23% YoY từ 2019 sang 2020, đạt 15.2 tỷ VND".
- **Tránh trùng lặp**: Nếu biểu đồ A và B kể cùng một câu chuyện, chỉ giữ biểu đồ nào rõ ràng hơn.
- **Flow logic**: Mở đầu bằng Descriptive (bức tranh tổng thể) → Diagnostic (tại sao?) → Predictive (dự báo) → Prescriptive (đề xuất). Đây chính là rubric chấm điểm.

### 4. Quy chuẩn kỹ thuật

- **Reproducibility**: Mọi notebook phải chạy được từ đầu đến cuối mà không lỗi. Đặt `random_state=42` cho tất cả model/sampling.
- **File path**: Dùng relative path (`../Data/orders.csv`) thay vì absolute path, để cả team chạy được.
- **Thư viện thống nhất**: Cả team dùng chung version, ghi vào `requirements.txt`. Khuyên dùng:
  - `polars` cho data wrangling (dataset lớn >600K dòng)
  - `matplotlib` + `seaborn` cho static charts (đẹp hơn cho report PDF)
  - `plotly` cho interactive charts (nếu làm dashboard bonus)
- **Encoding**: Lưu ý khi đọc file có ký tự tiếng Việt — dùng `encoding='utf-8'`.

### 5. Lưu ý riêng cho bộ dữ liệu này

- **Dữ liệu là mô phỏng**: Không phải dữ liệu thật, nên có thể có pattern nhân tạo. Tuy nhiên, vẫn phải phân tích và đề xuất như thật.
- **Thời gian dài (10 năm)**: 2012-2022 bao gồm nhiều giai đoạn kinh tế khác nhau. Nên chia phân tích thành các giai đoạn: trước COVID (→2019), COVID (2020-2021), hậu COVID (2022).
- **Không có `conversion_rate` trong `web_traffic`**: Dữ liệu thực cho thấy cột này không tồn tại trong file, cần tính conversion từ cross-reference với `orders.csv` theo `date`.
- **`promotions.csv` chỉ có 50 dòng**: Không nên dùng mô hình ML phức tạp cho phân tích khuyến mãi — sample quá nhỏ. Dùng descriptive + diagnostic là đủ.
- **`order_items` có `promo_id_2`**: Cho thấy một đơn hàng có thể áp dụng 2 mã khuyến mãi cùng lúc (stackable). Đây là góc phân tích sáng tạo tiềm năng.
- **`sales.csv` là dữ liệu aggregated theo ngày**: Không có breakdown theo product/category. Muốn phân tích chi tiết hơn phải tự aggregate từ `order_items` ↔ `products`.
