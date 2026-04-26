import nbformat

with open('../notebooks/01_mcq_answers.ipynb', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

q2_code = """# Tính lợi nhuận gộp: (Price - COGS) / Price
products['margin'] = (products['price'] - products['cogs']) / products['price']

# Tính trung bình theo segment
margin_by_segment = products.groupby('segment')['margin'].mean().sort_values(ascending=False)
options_q2 = {'Premium': 'A', 'Performance': 'B', 'Activewear': 'C', 'Standard': 'D'}

print("Tỷ suất lợi nhuận gộp trung bình của các phân khúc trong đáp án:")
for seg in options_q2.keys():
    if seg in margin_by_segment:
        print(f" - {seg}: {margin_by_segment[seg]:.4f}")

top_segment = margin_by_segment.index[0]
print(f"\\nPhân khúc có tỷ suất lợi nhuận cao nhất toàn bộ dữ liệu: {top_segment} ({margin_by_segment[top_segment]:.4f})")
print(f"==> Đáp án Q2: {options_q2.get(top_segment, 'Không rõ')}")"""

nb.cells[7].source = q2_code

with open('../notebooks/01_mcq_answers.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
print("Fixed Q2!")
