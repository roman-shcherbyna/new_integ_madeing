from pathlib import Path
import os
import shutil
from dotenv import load_dotenv


load_dotenv()
FILES_PATH = os.getenv('FILES_PATH')
ARCHIVE_PATH = os.getenv('ARCHIVE_PATH')

def check_and_replace_file(filename):

    # 3) Строим полный путь к исходному и к архивному файлу
    src_path = Path(FILES_PATH) / filename
    dst_path = Path(ARCHIVE_PATH) / filename

    # 4) Проверяем, что исходный файл существует, и создаём папку архива, если нужно
    if not src_path.exists():
        raise FileNotFoundError(f'File not found: {src_path} {filename}')
    Path(ARCHIVE_PATH).mkdir(exist_ok=True)

    # 5) Перемещаем файл
    shutil.move(str(src_path), str(dst_path))

    print(f'File {filename} has been successfully moved')
