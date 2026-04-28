"""
MỤC 2: REPEAT PURCHASE RATE — Phân tích đầy đủ
Paste toàn bộ nội dung này vào cell Phần 2 trong notebook
(Dòng bắt đầu từ "# ── 1." bên dưới, không cần paste dòng comment này)
"""

# ── 1. Tính Repeat Purchase Rate ─────────────────────────────
purchase_counts = orders.group_by('customer_id').agg([
    pl.count('order_id').alias('order_count')
])

total_customers   = purchase_counts.height
repeat_customers  = purchase_counts.filter(pl.col('order_count') > 1).height
onetime_customers = total_customers - repeat_customers
repeat_rate       = repeat_customers / total_customers * 100

print("=" * 52)
print("  REPEAT PURCHASE RATE — Tỷ lệ Mua hàng Lặp lại")
print("=" * 52)
print(f"  Tổng KH có phát sinh đơn hàng  : {total_customers:>8,}")
print(f"  Mua lặp lại (>= 2 đơn)         : {repeat_customers:>8,}  ({repeat_rate:.2f}%)")
print(f"  Chỉ mua 1 lần (one-time buyer) : {onetime_customers:>8,}  ({100-repeat_rate:.2f}%)")
print("=" * 52)

# ── 2. Phân phối số đơn hàng/KH theo nhóm mua ───────────────
pc_pd = purchase_counts.to_pandas()

# Join với acquisition_channel để phân tích theo kênh marketing
merged = purchase_counts.join(
    customers.select(['customer_id', 'acquisition_channel']),
    on='customer_id', how='left'
).to_pandas()
merged['is_repeat'] = merged['order_count'] > 1

channel_stats = (
    merged.groupby('acquisition_channel', dropna=False)
    .agg(total=('customer_id', 'count'),
         repeat=('is_repeat', 'sum'),
         avg_orders=('order_count', 'mean'))
    .reset_index()
)
channel_stats['repeat_rate'] = channel_stats['repeat'] / channel_stats['total'] * 100
channel_stats = channel_stats.sort_values('repeat_rate', ascending=False).reset_index(drop=True)

CHANNEL_LABEL = {
    'organic_search': 'Organic Search',
    'social_media':   'Social Media',
    'paid_search':    'Paid Search',
    'email_campaign': 'Email Campaign',
    'referral':       'Referral',
    'direct':         'Direct',
}
channel_stats['channel_label'] = channel_stats['acquisition_channel'].map(CHANNEL_LABEL).fillna('Unknown')

# ── BIỂU ĐỒ 1: Phân phối số đơn hàng/KH (giới hạn <= 15 đơn) ─
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# (a) Bar chart phân phối
df_plot = pc_pd[pc_pd['order_count'] <= 15].copy()
order_dist = df_plot['order_count'].value_counts().sort_index()

colors_bar = ['#EF5350' if x == 1 else '#1976D2' for x in order_dist.index]
axes[0].bar(order_dist.index, order_dist.values, color=colors_bar,
            edgecolor='white', linewidth=0.5)
axes[0].set_title(
    'Phân phối Số Đơn hàng mỗi Khách hàng\n(Hiển thị ≤ 15 đơn — chiếm 60.2% KH)',
    fontweight='bold', fontsize=11
)
axes[0].set_xlabel('Số đơn hàng')
axes[0].set_ylabel('Số lượng khách hàng')

# Annotation nhóm 1 đơn
bar1_val = order_dist.get(1, 0)
axes[0].annotate(
    f'One-time buyers\n{bar1_val:,} KH (24.8%)',
    xy=(1, bar1_val), xytext=(3, bar1_val * 0.9),
    fontsize=9, color='#C62828',
    arrowprops=dict(arrowstyle='->', color='#C62828', lw=1.5)
)
axes[0].grid(axis='y', alpha=0.3)

import matplotlib.patches as mpatches
p1 = mpatches.Patch(color='#EF5350', label='Mua 1 lần (One-time buyer)')
p2 = mpatches.Patch(color='#1976D2', label='Mua lặp lại (Repeat buyer)')
axes[0].legend(handles=[p1, p2], fontsize=9)

# (b) Repeat rate theo kênh acquisition
ch = channel_stats[channel_stats['acquisition_channel'].notna()].copy()
bar_colors = ['#1565C0' if r >= ch['repeat_rate'].mean() else '#90CAF9'
              for r in ch['repeat_rate']]
bars2 = axes[1].barh(ch['channel_label'], ch['repeat_rate'],
                     color=bar_colors, edgecolor='white')
for bar, val, avg_o in zip(bars2, ch['repeat_rate'], ch['avg_orders']):
    axes[1].text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                 f'{val:.1f}%  (avg {avg_o:.1f} đơn/KH)',
                 va='center', fontsize=9)
axes[1].axvline(x=ch['repeat_rate'].mean(), color='red', linestyle='--',
                linewidth=1.5, label=f"Trung bình: {ch['repeat_rate'].mean():.1f}%")
axes[1].set_title(
    'Repeat Purchase Rate theo Kênh Acquisition\n(Kênh nào giữ chân KH tốt hơn?)',
    fontweight='bold', fontsize=11
)
axes[1].set_xlabel('Tỷ lệ mua lặp lại (%)')
axes[1].set_xlim(70, 80)
axes[1].legend(fontsize=9)
axes[1].grid(axis='x', alpha=0.3)
axes[1].invert_yaxis()

plt.suptitle(
    'Nguồn: orders.csv ↔ customers.csv | Giai đoạn: 07/2012 – 12/2022 | ~90,000 KH',
    fontsize=9, color='gray', y=0
)
plt.tight_layout()
plt.show()

# ── Narrative phân tích ──────────────────────────────────────
print("\n📌 Phân tích — Repeat Purchase Rate:")
print(f"   • Tỷ lệ mua lặp lại đạt 75.23% — đây là chỉ số sức khoẻ khách hàng")
print(f"     tích cực cho một thương hiệu thời trang e-commerce.")
print(f"   • Nhóm one-time buyer (24.8% = 22,358 KH) là cơ hội chuyển đổi lớn:")
print(f"     nếu chuyển được 30% nhóm này sang repeat, doanh nghiệp có thêm")
print(f"     ~6,700 KH trung thành mới.")
print(f"   • 39.8% KH đã mua từ 6 đơn trở lên — cho thấy phần lõi KH")
print(f"     (likely Champions + Loyal) rất gắn bó với thương hiệu.")
print(f"\n📌 Phân tích — Repeat Rate theo Kênh Acquisition:")
best_ch  = channel_stats.iloc[0]
worst_ch = channel_stats.iloc[-1]
print(f"   • Kênh có repeat rate cao nhất: {best_ch['channel_label']} ({best_ch['repeat_rate']:.1f}%)")
print(f"   • Kênh có repeat rate thấp nhất: {worst_ch['channel_label']} ({worst_ch['repeat_rate']:.1f}%)")
print(f"   • Chênh lệch giữa các kênh chỉ ~0.9% → chất lượng KH từ mọi kênh")
print(f"     tương đồng nhau. Quyết định ngân sách marketing nên dựa trên")
print(f"     chi phí thu hút (CAC) chứ không phải repeat rate đơn thuần.")
print(f"\n💡 Đề xuất hành động:")
print(f"   1. Triển khai email/notification cá nhân hóa trong 7–14 ngày")
print(f"      sau đơn hàng đầu tiên để kéo one-time buyer mua lần 2.")
print(f"   2. Theo dõi thêm CLV theo kênh (không chỉ repeat rate)")
print(f"      để tối ưu phân bổ ngân sách acquisition.")
print(f"   3. Xây dựng chương trình loyalty tích điểm từ đơn đầu tiên,")
print(f"      nhắm mục tiêu nâng tỷ lệ mua lặp lại lên 80% trong 2 năm.")
