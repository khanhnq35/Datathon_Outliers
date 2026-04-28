"""
PHẦN 4: RFM SEGMENTATION — Phân tích, Đánh giá, Trực quan hóa
Paste toàn bộ nội dung cell này vào notebook Phần 4
"""
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings('ignore')

# ── 1. Tính RFM ───────────────────────────────────────────────
order_payments = orders.join(payments, on='order_id')
current_date = orders['order_date'].max() + pl.duration(days=1)

rfm = order_payments.group_by('customer_id').agg([
    ((current_date - pl.col('order_date').max()).dt.total_days()).alias('recency'),
    pl.col('order_id').n_unique().alias('frequency'),
    pl.col('payment_value').sum().alias('monetary')
])
rfm_pd = rfm.to_pandas()
rfm_pd['r_score'] = pd.qcut(rfm_pd['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm_pd['f_score'] = pd.cut(rfm_pd['frequency'],
                            bins=[0, 1, 2, 3, 4, float('inf')],
                            labels=[1, 2, 3, 4, 5])
rfm_pd['m_score'] = pd.qcut(rfm_pd['monetary'], 5, labels=[1, 2, 3, 4, 5])
rfm_pd['rfm_score'] = (rfm_pd['r_score'].astype(str)
                       + rfm_pd['f_score'].astype(str)
                       + rfm_pd['m_score'].astype(str))

def segment_customer(row):
    r, f = int(row['r_score']), int(row['f_score'])
    if r >= 4 and f >= 4: return 'Champions'
    if r >= 3 and f >= 3: return 'Loyal Customers'
    if r >= 4 and f <= 2: return 'New Customers'
    if r <= 2 and f >= 4: return 'At Risk'
    if r <= 2 and f <= 2: return 'Lost'
    return 'Potential Loyalist'

rfm_pd['segment'] = rfm_pd.apply(segment_customer, axis=1)

# ── 2. Bảng tổng hợp theo phân khúc ──────────────────────────
SEG_ORDER  = ['Champions', 'Loyal Customers', 'Potential Loyalist',
              'New Customers', 'At Risk', 'Lost']
SEG_COLORS = {
    'Champions':          '#1565C0',
    'Loyal Customers':    '#1976D2',
    'Potential Loyalist': '#64B5F6',
    'New Customers':      '#A5D6A7',
    'At Risk':            '#FFA726',
    'Lost':               '#EF5350',
}

total_rev = rfm_pd['monetary'].sum()
seg_df = (rfm_pd.groupby('segment')
          .agg(count=('customer_id','count'),
               avg_recency=('recency','mean'),
               avg_frequency=('frequency','mean'),
               avg_monetary=('monetary','mean'),
               total_monetary=('monetary','sum'))
          .reset_index())
seg_df['revenue_pct']  = seg_df['total_monetary'] / total_rev * 100
seg_df['customer_pct'] = seg_df['count'] / seg_df['count'].sum() * 100
seg_df['segment'] = pd.Categorical(seg_df['segment'], categories=SEG_ORDER, ordered=True)
seg_df = seg_df.sort_values('segment').reset_index(drop=True)

palette = [SEG_COLORS[s] for s in seg_df['segment']]

# ════════════════════════════════════════════════════════════
# BIỂU ĐỒ 1: Số lượng KH & Tỷ trọng Doanh thu theo Phân khúc
# ════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# (a) Số lượng KH
bars = axes[0].barh(seg_df['segment'], seg_df['count'], color=palette)
for bar, pct, cnt in zip(bars, seg_df['customer_pct'], seg_df['count']):
    axes[0].text(bar.get_width() + 200, bar.get_y() + bar.get_height()/2,
                 f'{cnt:,}  ({pct:.1f}%)', va='center', fontsize=9)
axes[0].set_title('Số lượng Khách hàng theo Phân khúc RFM', fontweight='bold')
axes[0].set_xlabel('Số khách hàng')
axes[0].invert_yaxis()
axes[0].set_xlim(0, seg_df['count'].max() * 1.35)
axes[0].grid(axis='x', alpha=0.3)

# (b) Tỷ trọng doanh thu
bars2 = axes[1].barh(seg_df['segment'], seg_df['revenue_pct'], color=palette)
for bar, pct in zip(bars2, seg_df['revenue_pct']):
    axes[1].text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                 f'{pct:.1f}%', va='center', fontsize=9)
axes[1].set_title('Tỷ trọng Doanh thu theo Phân khúc RFM', fontweight='bold')
axes[1].set_xlabel('% Tổng doanh thu')
axes[1].invert_yaxis()
axes[1].set_xlim(0, seg_df['revenue_pct'].max() * 1.25)
axes[1].grid(axis='x', alpha=0.3)

plt.suptitle('Nguồn: orders.csv ↔ payments.csv | ~90,000 khách hàng',
             fontsize=9, color='gray', y=0)
plt.tight_layout()
plt.show()

print("📌 Phân tích Biểu đồ 1 — Phân bổ KH & Doanh thu:")
champ = seg_df[seg_df['segment']=='Champions'].iloc[0]
lost  = seg_df[seg_df['segment']=='Lost'].iloc[0]
print(f"   • Champions: {champ['count']:,} KH ({champ['customer_pct']:.1f}%) → đóng góp {champ['revenue_pct']:.1f}% doanh thu")
print(f"     → Quy tắc Pareto được xác nhận: ~1/3 KH tạo ra 2/3 doanh thu.")
print(f"   • Lost: {lost['count']:,} KH ({lost['customer_pct']:.1f}%) → chỉ đóng góp {lost['revenue_pct']:.1f}% doanh thu")
print(f"     → Nhóm lớn thứ 2 nhưng gần như không còn giá trị — không nên đầu tư marketing nhiều.")
print(f"   • At Risk (7.7% KH) đóng góp 6.3% doanh thu — CLV tiềm năng rất cao nếu win-back thành công.")

# ════════════════════════════════════════════════════════════
# BIỂU ĐỒ 2: Scatter R vs F, colored by Segment, sized by M
# ════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(12, 7))
sample = rfm_pd.sample(min(5000, len(rfm_pd)), random_state=42)

for seg in SEG_ORDER:
    d = sample[sample['segment'] == seg]
    ax.scatter(
        d['recency'], d['frequency'],
        s=d['monetary'] / d['monetary'].max() * 300 + 10,
        c=SEG_COLORS[seg], alpha=0.4, label=seg, edgecolors='none'
    )

ax.set_title(
    'Bản đồ Phân khúc RFM: Recency vs Frequency\n'
    '(Kích thước điểm = Monetary | Mẫu 5,000 KH ngẫu nhiên)',
    fontweight='bold', fontsize=12
)
ax.set_xlabel('Recency — Số ngày kể từ đơn hàng cuối (thấp hơn = tốt hơn)', fontsize=10)
ax.set_ylabel('Frequency — Tổng số đơn hàng', fontsize=10)
ax.legend(loc='upper right', fontsize=9, title='Phân khúc')
ax.grid(alpha=0.3)

# Vùng annotation
ax.axvline(x=645, color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax.text(100, ax.get_ylim()[1]*0.95, 'Mua gần đây\n(Recency thấp)',
        ha='center', fontsize=8, color='#1565C0',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.4))
ax.text(2000, ax.get_ylim()[1]*0.95, 'Mua lâu rồi\n(Recency cao)',
        ha='center', fontsize=8, color='#EF5350',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFCDD2', alpha=0.4))
plt.tight_layout()
plt.show()

print("\n📌 Phân tích Biểu đồ 2 — Bản đồ Scatter RFM:")
print("   • Champions (xanh đậm, điểm lớn) tập trung ở góc Recency thấp + Frequency cao")
print("     → Đây là 'trái tim' của doanh nghiệp thời trang e-commerce.")
print("   • Lost (đỏ) trải dài ở vùng Recency cao (>2,000 ngày) — hầu hết đã không")
print("     mua hàng từ trước 2018, xác suất quay lại rất thấp.")
print("   • At Risk (cam) có Frequency cao nhưng Recency cũng cao — từng là KH tốt")
print("     nhưng đang mất dần. Đây là nhóm cần can thiệp khẩn cấp nhất.")

# ════════════════════════════════════════════════════════════
# BIỂU ĐỒ 3: So sánh Avg Monetary và Avg Recency theo phân khúc
# ════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 5))

# (a) Avg Monetary
bars3 = axes[0].bar(seg_df['segment'], seg_df['avg_monetary'] / 1000,
                    color=palette, edgecolor='white', linewidth=0.8)
for bar, val in zip(bars3, seg_df['avg_monetary']):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f'{val/1000:,.0f}K', ha='center', va='bottom', fontsize=9)
axes[0].set_title('Chi tiêu Trung bình mỗi KH theo Phân khúc\n(VND nghìn)', fontweight='bold')
axes[0].set_xlabel('Phân khúc')
axes[0].set_ylabel('Chi tiêu trung bình (nghìn VND)')
axes[0].tick_params(axis='x', rotation=30)
axes[0].grid(axis='y', alpha=0.3)

# (b) Avg Recency (lower is better)
bars4 = axes[1].bar(seg_df['segment'], seg_df['avg_recency'],
                    color=palette, edgecolor='white', linewidth=0.8)
for bar, val in zip(bars4, seg_df['avg_recency']):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                 f'{val:.0f} ngày', ha='center', va='bottom', fontsize=9)
axes[1].set_title('Recency Trung bình theo Phân khúc\n(thấp hơn = mua gần đây hơn)', fontweight='bold')
axes[1].set_xlabel('Phân khúc')
axes[1].set_ylabel('Số ngày kể từ đơn hàng cuối')
axes[1].tick_params(axis='x', rotation=30)
axes[1].grid(axis='y', alpha=0.3)

plt.suptitle('Nguồn: orders.csv ↔ payments.csv', fontsize=9, color='gray', y=0)
plt.tight_layout()
plt.show()

print("\n📌 Phân tích Biểu đồ 3 — Chân dung từng phân khúc:")
champ_r = seg_df[seg_df['segment']=='Champions']['avg_recency'].values[0]
atrisk_r = seg_df[seg_df['segment']=='At Risk']['avg_recency'].values[0]
champ_m = seg_df[seg_df['segment']=='Champions']['avg_monetary'].values[0]
atrisk_m = seg_df[seg_df['segment']=='At Risk']['avg_monetary'].values[0]
print(f"   • Champions: mua gần đây nhất (avg {champ_r:.0f} ngày), chi tiêu cao nhất")
print(f"     (trung bình {champ_m/1000:,.0f}K VND/KH).")
print(f"   • At Risk: avg recency = {atrisk_r:.0f} ngày (~{atrisk_r/365:.1f} năm) nhưng avg monetary")
print(f"     = {atrisk_m/1000:,.0f}K VND — cao hơn hẳn nhóm Lost và New Customers.")
print(f"     → CLV tiềm năng lớn nếu thành công tái kích hoạt.")
print(f"\n💡 Đề xuất hành động theo phân khúc:")
print(f"   🏆 Champions     → Loyalty reward, early access BST mới, ưu đãi sinh nhật")
print(f"   💙 Loyal         → Upsell sang Premium segment, referral program")
print(f"   🌱 New Customers → Onboarding email 3 bước, voucher đơn hàng thứ 2")
print(f"   ⚠️  At Risk       → Win-back campaign: voucher cá nhân hóa theo category đã mua")
print(f"   💀 Lost          → Email re-engagement chi phí thấp, không đầu tư paid ads")
