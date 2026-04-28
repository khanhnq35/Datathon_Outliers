import json

notebook_path = 'd:/Datathon_Outliers/notebooks/01_mcq_answers.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# New source for Q1 with simplified output
new_source = [
    "# Sắp xếp theo khách hàng và ngày\n",
    "orders_sorted = orders.sort_values(by=['customer_id', 'order_date'])\n",
    "\n",
    "# Lọc khách hàng có nhiều hơn 1 đơn (Dùng duplicated để tối ưu hơn isin)\n",
    "df_multi = orders_sorted[orders_sorted.duplicated(subset='customer_id', keep=False)].copy()\n",
    "\n",
    "# Tính chênh lệch ngày giữa các đơn liên tiếp\n",
    "df_multi['diff_days'] = df_multi.groupby('customer_id')['order_date'].diff().dt.days\n",
    "\n",
    "# Tính trung vị\n",
    "median_gap = df_multi['diff_days'].median()\n",
    "options_q1 = {30: 'A', 90: 'B', 180: 'C', 365: 'D'}\n",
    "ans_val = min(options_q1.keys(), key=lambda k: abs(k - median_gap))\n",
    "print(f\"Đáp án Q1: {median_gap} ngày => Đáp án {options_q1[ans_val]}\")"
]

# Find and update the cell for Q1
updated = False
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code' and any('median_gap = df_multi[\'diff_days\'].median()' in line for line in cell['source']):
        cell['source'] = new_source
        updated = True
        print(f"Updated cell {i}")
        break

if updated:
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Notebook updated successfully.")
else:
    print("Could not find the target cell.")
