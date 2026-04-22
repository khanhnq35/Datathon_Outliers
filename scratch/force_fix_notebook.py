import json
import re

file_path = r'd:\Datathon_Outliers\notebooks\01_mcq_answers.ipynb'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Các từ khóa thường thấy ở đầu cell code Python
code_keywords = ['import ', 'from ', 'df =', 'plt.', 'sns.', 'print(', '#', 'orders', 'products', 'returns']

for cell in data['cells']:
    source = "".join(cell.get('source', []))
    
    # Nếu cell là markdown nhưng chứa nhiều code Python
    if cell['cell_type'] == 'markdown':
        # Kiểm tra nếu source trông giống code (không bắt đầu bằng # hoặc chỉ có vài dòng)
        if any(source.strip().startswith(kw) for kw in ['import ', 'from ', 'pd.', 'print(']):
             print(f"Chuyển đổi cell từ markdown sang code: {source[:30]}...")
             cell['cell_type'] = 'code'
             cell['outputs'] = []
             cell['execution_count'] = None

    # Reset metadata cho tất cả cell code
    if cell['cell_type'] == 'code':
        cell['metadata'] = {}
        # Đôi khi VS Code cần cái này
        cell['metadata']['vscode'] = {'languageId': 'python'}

# Đảm bảo metadata của cả notebook là chuẩn
if 'metadata' not in data:
    data['metadata'] = {}

data['metadata']['kernelspec'] = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3"
}
data['metadata']['language_info'] = {
    "codemirror_mode": {
        "name": "ipython",
        "version": 3
    },
    "file_extension": ".py",
    "mimetype": "text/x-python",
    "name": "python",
    "nbconvert_exporter": "python",
    "pygments_lexer": "ipython3",
    "version": "3"
}

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=1, ensure_ascii=False)

print("Đã thực hiện fix triệt để metadata và loại cell.")
