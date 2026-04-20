# 💼 Business Analytics — Góc nhìn Kinh doanh cho Datathon 2026

> Tài liệu này phân tích bộ dữ liệu từ góc nhìn kinh doanh, giúp team xác định **các câu chuyện có giá trị** (high-impact stories), đặt đúng câu hỏi, và trình bày insight theo ngôn ngữ mà ban giám khảo muốn nghe.

---

## 1. Bối cảnh doanh nghiệp

### Doanh nghiệp này là ai?
Dựa trên dữ liệu, ta đang phân tích một **công ty thời trang e-commerce tại Việt Nam** với các đặc điểm:

| Đặc điểm | Chi tiết (từ dữ liệu thực) |
|----------|---------------------------|
| **Quy mô** | ~122K khách hàng, ~647K đơn hàng, ~2,400 SKU (sản phẩm) |
| **Doanh thu** | ~1M–6.5M VND/ngày — ước tính **~1,000–2,500 tỷ VND/năm** |
| **Thời gian hoạt động** | 10.5 năm (07/2012 → 12/2022) |
| **Thị trường** | Toàn quốc, 3 vùng (East, Central, West), nhiều thành phố |
| **Kênh bán** | Website (desktop, mobile, tablet) — đa kênh marketing |
| **Sản phẩm** | 5 category: Streetwear, Casual, Outdoor, ... với các segment (Everyday, Premium, Performance, ...) |
| **Giá trị đơn hàng** | AOV dao động ~8K–70K VND (dựa trên payments) |
| **Khuyến mãi** | 50 chiến dịch trong 10 năm (~5/năm), cả percentage và fixed |

### Stakeholders cần phục vụ
Khi viết report, hãy tưởng tượng bạn đang trình bày cho:
- **CEO/COO**: Quan tâm tăng trưởng doanh thu, lợi nhuận, market position
- **CMO (Marketing)**: Hiệu quả kênh, chi phí thu hút khách hàng, ROI khuyến mãi
- **VP Operations**: Tồn kho, logistics, tỷ lệ trả hàng, delivery performance
- **VP Product**: Danh mục sản phẩm, pricing, product-market fit

---

## 2. Năm câu hỏi kinh doanh cốt lõi

Mọi phân tích EDA nên xoay quanh **5 trụ cột** sau. Mỗi trụ cột tương ứng với một quyết định kinh doanh cụ thể:

### ❶ Tăng trưởng & Sức khoẻ tài chính
> _"Doanh nghiệp đang tăng trưởng hay suy giảm? Lợi nhuận có bền vững không?"_

**Dữ liệu**: `sales.csv`, `order_items.csv`, `products.csv`

**Phân tích cần làm:**
- Revenue YoY growth rate — có tăng đều hay bão hoà?
- Gross margin trend = `(Revenue - COGS) / Revenue` — margin đang co lại hay mở rộng?
- **Phát hiện quan trọng từ data**: Cuối 2022, có nhiều ngày `COGS > Revenue` (margin âm). Đây là dấu hiệu cảnh báo nghiêm trọng — doanh nghiệp đang **bán lỗ**. Phải highlight trong report.
- Revenue per customer (RPU) trend — mỗi khách hàng chi tiêu nhiều hơn hay ít đi?

**Câu hỏi cho ban giám khảo:**
- "Doanh thu tăng 15% YoY nhưng margin giảm từ 25% xuống 18% — tăng trưởng này có bền vững?"
- "Chi phí vốn hàng bán (COGS) tăng nhanh hơn doanh thu từ Q3/2022 — cần rà soát chiến lược pricing"

---

### ❷ Khách hàng & Retention
> _"Khách hàng trung thành đến mức nào? Chi phí giữ chân vs. thu hút mới?"_

**Dữ liệu**: `customers.csv`, `orders.csv`, `payments.csv`, `reviews.csv`

**Phân tích cần làm:**
- **Repeat Purchase Rate**: Bao nhiêu % KH mua lần 2? Lần 3?
- **Cohort Retention**: KH đăng ký tháng 1/2020 — sau 3, 6, 12 tháng còn bao nhiêu % quay lại?
- **RFM Segmentation**: Phân nhóm KH thành Champions, Loyal, At Risk, Lost
- **Customer Lifetime Value (CLV)**: Nhóm KH nào đóng góp nhiều nhất cho tổng doanh thu?
- **Acquisition Channel Effectiveness**: Kênh nào (`organic_search`, `paid_search`, `email_campaign`, `referral`, `social_media`) thu hút KH có giá trị cao nhất (không phải nhiều nhất)?

**Insight tiềm năng:**
- "80% doanh thu đến từ 20% khách hàng" — kiểm tra xem Pareto rule có đúng không
- "KH từ `email_campaign` có CLV cao gấp 2x so với `social_media`" → đề xuất tái phân bổ ngân sách
- "Nhóm tuổi 35-44 có số đơn/KH cao nhất nhưng chỉ chiếm 18% tổng KH" → cơ hội mở rộng target

**Prescriptive (đề xuất):**
- Xây chương trình loyalty cho Top 20% KH (Champions)
- Thiết kế win-back campaign cho nhóm At Risk (mua lần cuối > 6 tháng)
- Tăng ngân sách cho kênh acquisition có CLV cao nhất

---

### ❸ Sản phẩm & Pricing
> _"Bán cái gì, giá bao nhiêu, và có hợp lý không?"_

**Dữ liệu**: `products.csv`, `order_items.csv`, `returns.csv`, `inventory.csv`

**Phân tích cần làm:**
- **BCG Matrix**: Phân loại category/segment theo Market share × Growth
  - Stars: Tăng trưởng nhanh + thị phần lớn → đầu tư mạnh
  - Cash Cows: Tăng trưởng chậm + thị phần lớn → duy trì, tối ưu
  - Question Marks: Tăng trưởng nhanh + thị phần nhỏ → thử nghiệm
  - Dogs: Tăng trưởng chậm + thị phần nhỏ → cân nhắc loại bỏ
- **Price vs. Volume**: Sản phẩm giá cao bán ít nhưng margin tốt vs. sản phẩm giá rẻ bán nhiều nhưng margin mỏng
- **Size Distribution vs. Return Rate**: Size nào bán nhiều nhất? Size nào bị trả lại nhiều nhất? Có mismatch không?
- **Color Preference**: Màu nào bán chạy theo mùa? Có thể tối ưu tồn kho theo màu?

**Insight tiềm năng:**
- "Segment Premium chỉ chiếm 12% số SKU nhưng đóng góp 35% gross profit" → nên mở rộng
- "Sản phẩm giá < 100 VND (product_id 543) có margin gần 0" → review lại pricing hoặc loại bỏ
- "Size XL có return rate cao nhất (wrong_size)" → cần cải thiện size guide cho XL

**Prescriptive:**
- Loại bỏ hoặc re-price sản phẩm Dogs (margin < 5%, volume bottom 10%)
- Mở rộng dòng Premium — thêm 20% SKU mới vào segment này
- A/B test pricing strategy: tăng giá 5-10% cho sản phẩm elastic thấp

---

### ❹ Vận hành & Supply Chain
> _"Có đang vận hành hiệu quả không? Hàng tồn có tối ưu không?"_

**Dữ liệu**: `inventory.csv`, `shipments.csv`, `returns.csv`, `orders.csv`

**Phân tích cần làm:**
- **Stockout Impact**: Bao nhiêu ngày trong năm không có hàng? Ước tính lost revenue
- **Overstock Cost**: Sản phẩm nào tồn kho > 90 ngày? Chi phí vốn bị đọng?
- **Delivery Performance**: Thời gian trung bình từ `order_date` → `ship_date` → `delivery_date`? Vùng nào giao chậm nhất?
- **Return Cost**: Tổng `refund_amount` theo năm — chi phí reverse logistics đang tăng hay giảm?
- **Fulfillment Rate**: `fill_rate` trung bình? Có đang cải thiện qua các năm?

**Insight tiềm năng:**
- "Stockout trung bình 2 ngày/tháng ở Top 10 sản phẩm → ước tính mất ~X tỷ VND/năm"
- "Thời gian giao hàng trung bình ở vùng Central chậm hơn East 2 ngày" → cần partner logistics bổ sung
- "Return chi phí ~X tỷ VND/năm, trong đó 40% do `wrong_size`" → ROI của việc làm size guide = tiết kiệm 40% return cost

**Prescriptive:**
- Thiết lập reorder point tự động cho Top 50 sản phẩm dựa trên `days_of_supply`
- Giảm delivery time ở Central bằng cách đặt kho phân phối phụ
- Đầu tư vào size guide và hình ảnh sản phẩm chuẩn → giảm 30% returns do wrong_size

---

### ❺ Marketing & Digital Performance
> _"Kênh nào hiệu quả? Đang chi tiêu marketing đúng chỗ chưa?"_

**Dữ liệu**: `web_traffic.csv`, `orders.csv`, `promotions.csv`, `customers.csv`

**Phân tích cần làm:**
- **Channel Attribution**: Kênh nào dẫn đến conversion cao nhất? (`traffic_source` → `order_source`)
- **Promo ROI**: Mỗi chiến dịch KM tăng bao nhiêu đơn? Tăng đúng doanh thu hay chỉ forward demand?
- **Bounce Rate Analysis**: Kênh nào có bounce rate cao? Tại sao?
- **Device Trend**: Mobile đang tăng so với Desktop qua các năm? UX mobile cần cải thiện?
- **Session-to-Revenue Pipeline**: Cần bao nhiêu sessions để tạo 1 đơn hàng?

**Insight tiềm năng:**
- "`organic_search` chiếm 40% traffic nhưng 55% revenue — SEO là kênh hiệu quả nhất"
- "KM `percentage` tạo ra nhiều đơn hơn nhưng `fixed` có AOV cao hơn 25%"
- "Mobile conversion rate chỉ bằng 60% desktop → cơ hội cải thiện UX mobile = tăng 15% revenue"

**Prescriptive:**
- Tăng 30% ngân sách SEO, giảm 20% paid_search (bounce rate cao)
- Chạy KM `fixed` cho segment Premium (AOV cao) và `percentage` cho Everyday (volume)
- Ưu tiên mobile-first design sprint — đặt target tăng mobile conversion lên 80% desktop level

---

## 3. Framework kể chuyện cho Report

### Storytelling Arc (Mạch truyện)
Report 4 trang nên follow cấu trúc narrative này:

```
📖 Mở đầu:  "Doanh nghiệp thời trang e-commerce VN đã tăng trưởng ấn tượng 
             trong 10 năm qua, nhưng đang đối mặt với thách thức..."

🔍 Thân bài: 
   Act 1 — NHỮNG GÌ ĐÃ DIỄN RA (Descriptive)
     → Revenue trend, customer growth, product portfolio overview
   
   Act 2 — TẠI SAO (Diagnostic) 
     → Margin bị ép, return rate tăng, stockout gây mất doanh thu
   
   Act 3 — ĐIỀU GÌ SẼ XẢY RA (Predictive)
     → CLV forecast, churn prediction, seasonal demand
   
   Act 4 — NÊN LÀM GÌ (Prescriptive)
     → 5 đề xuất cụ thể, có số liệu, đo lường được

🎯 Kết luận: "3 hành động ưu tiên cao nhất để tăng 15% lợi nhuận trong 
             12 tháng tới: (1)..., (2)..., (3)..."
```

### Template cho mỗi Insight
```
[Phát hiện]: "Return rate cho category Streetwear tăng 40% YoY trong 2022"
[Nguyên nhân]: "83% returns do wrong_size, tập trung ở size XL"  
[Tác động]: "Chi phí refund ~2.5 tỷ VND/năm, chiếm 8% gross profit"
[Đề xuất]: "Đầu tư 200 triệu VND vào detailed size guide + virtual try-on → 
            ROI ước tính 10x trong 12 tháng"
```

---

## 4. Góc nhìn sáng tạo (ghi điểm Tính sáng tạo 5đ)

Những góc phân tích **ít đội nghĩ đến** nhưng mang lại giá trị cao:

### 4.1 "The Hidden Revenue Leak" — Doanh thu bị rò rỉ ở đâu?
Tính tổng "lost revenue" từ 3 nguồn:
1. **Cancellation**: Đơn bị huỷ × AOV = revenue mất
2. **Returns**: `refund_amount` tổng = revenue hoàn lại
3. **Stockout**: Ngày hết hàng × avg daily sales = revenue không bán được

→ Vẽ waterfall chart: Revenue tiềm năng → Actual Revenue → Gap analysis

### 4.2 "The Promotion Paradox" — KM có đang hại doanh nghiệp?
- So sánh doanh thu **2 tuần trước** vs. **trong** vs. **2 tuần sau** mỗi chiến dịch KM
- Nếu doanh thu **sau KM giảm mạnh** → KM chỉ kéo demand từ tương lai, không tạo demand mới
- Tính "Promotion Efficiency": `incremental_revenue / discount_amount`

### 4.3 "The Size Paradox" — Bán nhiều nhưng trả cũng nhiều
- Cross-tabulation: `size` × `quantity_sold` × `return_rate`
- Kỳ vọng: size phổ biến (M, L) bán nhiều nhất → nhưng XL có return rate vượt trội?
- Business question: "Có nên tiếp tục sản xuất size XL cho tất cả category?"

### 4.4 "Weekend Warriors vs. Weekday Shoppers"
- Phân tích hành vi mua hàng theo ngày trong tuần
- Weekend shoppers có AOV, return rate, payment method khác weekday không?
- → Đề xuất chiến lược KM khác nhau cho weekend vs. weekday

### 4.5 "The Payment-Loyalty Connection"
- KH trả góp 12 kỳ có quay lại mua tiếp không? Hay bị "kẹt" trả góp?
- So sánh CLV theo payment method: credit_card vs. cod vs. paypal vs. apple_pay
- → KH dùng payment method nào có giá trị dài hạn cao nhất?

---

## 5. Những con số ban giám khảo muốn nghe

Khi viết report, **luôn đính kèm con số cụ thể**. Dưới đây là checklist các metrics nên tính:

### Metrics tài chính
- [ ] Tổng Revenue theo năm & CAGR (Compound Annual Growth Rate)
- [ ] Gross Margin % theo năm (trend)
- [ ] Revenue per Customer (RPU) trend
- [ ] Average Order Value (AOV) trend

### Metrics khách hàng
- [ ] Customer Acquisition Rate (KH mới/tháng)
- [ ] Repeat Purchase Rate (% KH mua > 1 lần)
- [ ] Customer Churn Rate (% KH không quay lại sau 12 tháng)
- [ ] Net Promoter Score proxy (% rating 4-5 vs. 1-2)

### Metrics vận hành
- [ ] Order Fulfillment Rate
- [ ] Average Delivery Time (ngày)
- [ ] Return Rate (% đơn bị trả)
- [ ] Stockout Frequency (số ngày/tháng hết hàng)

### Metrics marketing
- [ ] Conversion Rate theo kênh
- [ ] Cost per Acquisition proxy (based on channel effectiveness)
- [ ] Promotion ROI per campaign
- [ ] Bounce Rate theo source

---

## 6. Chiến lược trình bày cho người A (Business)

### Trong EDA notebooks
- Viết 2-3 câu narrative **ngay dưới mỗi biểu đồ**
- Dùng ngôn ngữ "So what?" — biểu đồ cho thấy gì → doanh nghiệp nên làm gì
- Tránh jargon kỹ thuật: nói "sản phẩm bán chạy" thay vì "high-frequency SKU"

### Trong Report (4 trang)
- Trang 1: Giới thiệu + Revenue & Margin overview (1 biểu đồ lớn)
- Trang 2: Customer insights + Product insights (2-3 biểu đồ)
- Trang 3: Operational insights + Prescriptive recommendations (1-2 biểu đồ + bảng đề xuất)
- Trang 4: Forecasting methodology + results + SHAP

### Ngôn ngữ nên dùng
| Thay vì... | Nên viết... |
|-----------|------------|
| "Data shows high variance" | "Doanh thu biến động mạnh giữa các ngày, chênh lệch lên tới 5x" |
| "Cluster analysis reveals 4 segments" | "Khách hàng chia thành 4 nhóm rõ rệt: VIP (12%), Trung thành (28%), Tiềm năng (35%), Rời bỏ (25%)" |
| "The model achieves R² of 0.85" | "Mô hình giải thích được 85% biến động doanh thu, với COGS và mùa vụ là hai yếu tố chính" |
| "Feature importance shows..." | "Ba yếu tố quyết định doanh thu nhiều nhất là: (1) Chi phí vốn hàng bán, (2) Ngày trong tuần, (3) Xu hướng thị trường" |

---

## 7. Tóm tắt — Top 5 câu chuyện phải có trong Report

| # | Câu chuyện | Cấp độ | Tại sao quan trọng |
|---|-----------|--------|-------------------|
| 1 | **Doanh thu tăng nhưng margin giảm** — dấu hiệu cảnh báo | Descriptive + Diagnostic | Đây là insight lớn nhất, thể hiện chiều sâu phân tích |
| 2 | **20% KH tạo ra 80% doanh thu** — ai là VIP? | Descriptive + Predictive | RFM/CLV thể hiện level Predictive |
| 3 | **Return cost chiếm X% profit** — nguyên nhân gốc? | Diagnostic | Cross-table analysis, root cause thinking |
| 4 | **Marketing channel ROI** — chi tiền đúng chỗ chưa? | Diagnostic + Prescriptive | Actionable recommendation rõ ràng |
| 5 | **Tồn kho → mất doanh thu** — cơ hội tối ưu vận hành | Prescriptive | Định lượng được, áp dụng được ngay |

> 💡 **Nguyên tắc vàng**: Mỗi biểu đồ trong report phải trả lời được câu hỏi "Rồi sao? Doanh nghiệp nên làm gì với thông tin này?" Nếu không trả lời được → bỏ biểu đồ đó ra.
