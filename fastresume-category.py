import os
import shutil
import bencodepy

# Заменяет символы, запрещённые в путях
def sanitize_folder_name(name):
    return name.replace("/", "#")

# Извлекает qBt-category из fastresume-файла
def extract_category(fastresume_path):
    try:
        with open(fastresume_path, "rb") as f:
            data = bencodepy.decode(f.read())
        if b"qBt-category" in data:
            return data[b"qBt-category"].decode("utf-8")
    except Exception as e:
        print(f"[!] Ошибка чтения {fastresume_path}: {e}")
    return None

# Основная логика
def process_fastresume_files(source_dir, target_root):
    for file in os.listdir(source_dir):
        if not file.endswith(".fastresume"):
            continue

        fastresume_path = os.path.join(source_dir, file)
        base_name = os.path.splitext(file)[0]
        torrent_file = os.path.join(source_dir, base_name + ".torrent")

        category = extract_category(fastresume_path)
        if not category:
            print(f"[!] Категория не найдена в {file}")
            continue

        safe_folder = sanitize_folder_name(category)
        target_folder = os.path.join(target_root, safe_folder)
        os.makedirs(target_folder, exist_ok=True)

        try:
            shutil.move(fastresume_path, os.path.join(target_folder, file))
            print(f"[+] Перемещён: {file} → {target_folder}")
        except Exception as e:
            print(f"[!] Ошибка при перемещении .fastresume: {e}")

        if os.path.exists(torrent_file):
            try:
                shutil.move(torrent_file, os.path.join(target_folder, base_name + ".torrent"))
                print(f"[+] Перемещён: {base_name}.torrent → {target_folder}")
            except Exception as e:
                print(f"[!] Ошибка при перемещении .torrent: {e}")
        else:
            print(f"[!] .torrent не найден для {base_name}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Использование: python sort_fastresume_by_category.py <папка_с_файлами> <папка_назначения>")
        sys.exit(1)

    source = sys.argv[1]
    target = sys.argv[2]

    process_fastresume_files(source, target)
