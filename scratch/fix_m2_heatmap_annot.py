import json

file_path = r'd:\Datathon_Outliers\notebooks\02_M2_customer_retention.ipynb'

with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "sns.heatmap(retention_percentage" in source:
            new_source = []
            for line in cell['source']:
                if "sns.heatmap(" in line:
                    new_source.append(line.replace("annot=True", "annot=False"))
                else:
                    new_source.append(line)
            cell['source'] = new_source

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
    f.write('\n')
