import shutil
import os
from datetime import datetime, timedelta

class FolderCopier:
    def __init__(self, source_folder, new_folder):
        self.source_folder = source_folder
        self.new_folder = new_folder
        self.destination_folder = self._generate_destination_folder_name()

    def _generate_destination_folder_name(self):
        current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        return os.path.join(os.path.dirname(self.new_folder), current_date)

    # Копируем содержимое исходной папки в новую папку
    def copy_folder(self):
        try:   
            shutil.copytree(self.source_folder, self.destination_folder)
            return True 
        except Exception as e:
            return False, f"Ошибка копирования: {str(e)}"
        
    # Удаляем папки старше указанного количества дней
    def remove_old_folders(self, days):
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(days=days)

        for folder in os.listdir(os.path.dirname(self.new_folder)):
            folder_path = os.path.join(os.path.dirname(self.new_folder), folder)
            if os.path.isdir(folder_path):
                folder_mod_time = datetime.fromtimestamp(os.path.getmtime(folder_path))
                if folder_mod_time < cutoff_time:
                    try:
                        shutil.rmtree(folder_path)
                        return True
                    except Exception as e:
                        return False, f"Ошибка удаления: {str(e)}"
