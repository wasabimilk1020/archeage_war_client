import os
import json

def file_path(_file, _folder=None, _sub_folder=None):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # None이 아닌 값만 경로에 포함
    path_parts = [BASE_DIR]
    if _folder:
        path_parts.append(_folder)
    if _sub_folder:
        path_parts.append(_sub_folder)
    path_parts.append(_file)

    # 경로 조합
    full_path = os.path.join(*path_parts)

    return full_path

def load_json(json_file, json_folder): #file, folder
  full_path=file_path(json_file, json_folder)  #file, folder, sub_folder

  try:
    with open(full_path, "r", encoding="utf-8") as f:
      return json.load(f)
  except (FileNotFoundError, json.JSONDecodeError):
    return {}  # 파일이 없거나 잘못된 JSON이면 빈 데이터 반환

