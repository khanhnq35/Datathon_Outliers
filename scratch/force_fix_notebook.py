import json

with open('../notebooks/01_mcq_answers.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "region_revenue = orders_geo.groupby('region')['total_amount']" in source:
            new_source = [
                "# Merge orders với customers (bỏ cột zip của orders để tránh trùng lặp khi merge)\n",
                "orders_cust = orders.drop(columns=['zip']).merge(customers, on='customer_id', how='inner')\n",
                "# Merge với geography để lấy region\n",
                "orders_geo = orders_cust.merge(geography, on=['zip', 'city'], how='inner')\n",
                "# Merge với payments để lấy doanh thu (payment_value)\n",
                "orders_full = orders_geo.merge(payments, on='order_id', how='inner')\n\n",
                "# Tính tổng doanh thu theo region\n",
                "region_revenue = orders_full.groupby('region')['payment_value'].sum().sort_values(ascending=False)\n",
                "print(\"Q7 Answer:\")\n",
                "print(region_revenue.head())"
            ]
            cell['source'] = new_source

with open('../notebooks/01_mcq_answers.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
    f.write('\n')
