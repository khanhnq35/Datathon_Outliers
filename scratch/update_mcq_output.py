import nbformat

with open('../notebooks/01_mcq_answers.ipynb', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

def update_source(cell_index, append_code):
    lines = nb.cells[cell_index].source.split('\n')
    # remove existing print lines
    lines = [line for line in lines if not line.startswith("print")]
    lines.append(append_code)
    nb.cells[cell_index].source = '\n'.join(lines)

# Q1
q1_code = """
options_q1 = {30: 'A', 90: 'B', 180: 'C', 365: 'D'}
ans_val = min(options_q1.keys(), key=lambda k: abs(k - median_gap))
print(f"Giá trị trung vị: {median_gap} ngày")
print(f"==> Đáp án Q1: {options_q1[ans_val]}")
"""
update_source(5, q1_code.strip())

# Q2
q2_code = """
options_q2 = {'Premium': 'A', 'Performance': 'B', 'Activewear': 'C', 'Standard': 'D'}
top_segment = margin_by_segment.index[0]
print(f"Phân khúc có tỷ suất lợi nhuận cao nhất: {top_segment}")
print(f"==> Đáp án Q2: {options_q2.get(top_segment, 'Không rõ')}")
"""
update_source(7, q2_code.strip())

# Q3
q3_code = """
options_q3 = {'defective': 'A', 'wrong_size': 'B', 'changed_mind': 'C', 'not_as_described': 'D'}
top_reason_val = top_reason.index[0]
print(f"Lý do trả hàng nhiều nhất: {top_reason_val}")
print(f"==> Đáp án Q3: {options_q3.get(top_reason_val, 'Không rõ')}")
"""
update_source(9, q3_code.strip())

# Q4
q4_code = """
options_q4 = {'organic_search': 'A', 'paid_search': 'B', 'email_campaign': 'C', 'social_media': 'D'}
top_source = bounce_rate.index[0]
print(f"Nguồn có tỷ lệ thoát thấp nhất: {top_source}")
print(f"==> Đáp án Q4: {options_q4.get(top_source, 'Không rõ')}")
"""
update_source(11, q4_code.strip())

# Q5
q5_code = """
options_q5 = {12: 'A', 25: 'B', 39: 'C', 54: 'D'}
ans_val = min(options_q5.keys(), key=lambda k: abs(k - promo_ratio))
print(f"Tỷ lệ có khuyến mãi: {promo_ratio:.2f}%")
print(f"==> Đáp án Q5: {options_q5[ans_val]}")
"""
update_source(13, q5_code.strip())

# Q6
q6_code = """
options_q6 = {'55+': 'A', '25-34': 'B', '35-44': 'C', '45-54': 'D'}
# handle format like '25-34' vs '25–34'
top_age_group = age_group_orders.index[0]
normalized_age_group = top_age_group.replace('–', '-')
print(f"Nhóm tuổi có số đơn hàng TB cao nhất: {top_age_group}")
print(f"==> Đáp án Q6: {options_q6.get(normalized_age_group, 'Không rõ')}")
"""
update_source(15, q6_code.strip())

# Q7
q7_code = """
options_q7 = {'West': 'A', 'Central': 'B', 'East': 'C'}
top_region = region_revenue.index[0]
print(f"Vùng có doanh thu cao nhất: {top_region}")
print(f"==> Đáp án Q7: {options_q7.get(top_region, 'D')}") # D is Cả ba vùng xấp xỉ bằng nhau
"""
update_source(17, q7_code.strip())

# Q8
q8_code = """
options_q8 = {'credit_card': 'A', 'cod': 'B', 'paypal': 'C', 'bank_transfer': 'D'}
top_payment_method = top_payment.index[0]
print(f"Phương thức thanh toán nhiều nhất khi huỷ đơn: {top_payment_method}")
print(f"==> Đáp án Q8: {options_q8.get(top_payment_method, 'Không rõ')}")
"""
update_source(19, q8_code.strip())

# Q9
q9_code = """
options_q9 = {'S': 'A', 'M': 'B', 'L': 'C', 'XL': 'D'}
top_size = return_ratio.index[0]
print(f"Kích thước có tỷ lệ trả hàng cao nhất: {top_size}")
print(f"==> Đáp án Q9: {options_q9.get(top_size, 'Không rõ')}")
"""
update_source(21, q9_code.strip())

# Q10
q10_code = """
options_q10 = {1: 'A', 3: 'B', 6: 'C', 12: 'D'}
top_installments = avg_payment_installments.index[0]
print(f"Kế hoạch trả góp có GT thanh toán TB cao nhất: {top_installments} kỳ")
print(f"==> Đáp án Q10: {options_q10.get(top_installments, 'Không rõ')}")
"""
update_source(23, q10_code.strip())

with open('../notebooks/01_mcq_answers.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
print("Updated all cells!")
