import tempfile
import zipfile
import os
import json
from langchain.schema import Document

def process_zip_of_json(uploaded_file):
    chunks = []
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_file:
        tmp_file.write(uploaded_file.file.read())
        tmp_path = tmp_file.name

    with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.endswith('.json'):
                with zip_ref.open(file_info) as json_file:
                    data = json.load(json_file)
                    if isinstance(data, list):
                        for entry in data:
                            chunks.append(Document(page_content=entry))

    os.unlink(tmp_path)
    return chunks
