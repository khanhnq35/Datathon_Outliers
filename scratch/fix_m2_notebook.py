import json

file_path = r'd:\Datathon_Outliers\notebooks\02_M2_customer_retention.ipynb'

with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "sns.heatmap(retention_percentage" in source:
            new_source = [
                "# 7. Chuyển sang tỷ lệ %\n",
                "cohort_sizes = retention_matrix.iloc[:, 0]\n",
                "retention_percentage = retention_matrix.divide(cohort_sizes, axis=0) * 100\n",
                "\n",
                "# Format lại index (Cohort Month) cho đẹp, loại bỏ ngày giờ\n",
                "retention_percentage.index = pd.to_datetime(retention_percentage.index).strftime('%Y-%m')\n",
                "\n",
                "# 8. Vẽ Heatmap\n",
                "plt.figure(figsize=(16, 10))\n",
                "sns.heatmap(retention_percentage, annot=True, fmt='.1f', cmap='YlGnBu')\n",
                "plt.title('Cohort Retention Matrix (%)')\n",
                "plt.ylabel('Cohort Month')\n",
                "plt.xlabel('Months Since First Purchase')\n",
                "plt.show()"
            ]
            
            old_source = cell['source']
            final_source = []
            skip = False
            for line in old_source:
                if "# 7. Chuyển sang tỷ lệ %" in line:
                    skip = True
                    final_source.extend(new_source)
                elif skip and "plt.show()" in line:
                    skip = False
                elif not skip:
                    final_source.append(line)
            
            cell['source'] = final_source

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
    f.write('\n')
