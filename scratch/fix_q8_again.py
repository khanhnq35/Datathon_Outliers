import nbformat

with open('../notebooks/01_mcq_answers.ipynb', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

q8_code = """# Lọc các đơn bị hủy
cancelled_orders = orders[orders['order_status'] == 'cancelled']

# Đếm tần suất phương thức thanh toán
top_payment = cancelled_orders['payment_method'].value_counts()
options_q8 = {'credit_card': 'A', 'cod': 'B', 'paypal': 'C', 'bank_transfer': 'D'}
top_payment_method = top_payment.index[0]
print(f"Phương thức thanh toán nhiều nhất khi huỷ đơn: {top_payment_method}")
print(f"==> Đáp án Q8: {options_q8.get(top_payment_method, 'Không rõ')}")"""

nb.cells[19].source = q8_code

with open('../notebooks/01_mcq_answers.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
print("Fixed Q8!")
