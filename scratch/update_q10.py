import json

notebook_path = 'd:/Datathon_Outliers/notebooks/01_mcq_answers.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# New source for Q10 with simplified output
new_source = [
    "# Tính trung bình giá trị thanh toán theo số tháng trả góp\n",
    "avg_payment_installments = payments.groupby('installments')['payment_value'].mean().sort_values(ascending=False)\n",
    "options_q10 = {1: 'A', 3: 'B', 6: 'C', 12: 'D'}\n",
    "top_installments = avg_payment_installments.index[0]\n",
    "print(f\"Đáp án Q10: {top_installments} kỳ => Đáp án {options_q10.get(top_installments, 'Không rõ')}\")"
]

# Find and update the cell for Q10
updated = False
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code' and any('avg_payment_installments = payments.groupby(\'installments\')[\'payment_value\'].mean()' in line for line in cell['source']):
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
