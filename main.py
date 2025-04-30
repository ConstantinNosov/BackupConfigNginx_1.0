import logging
from ssh_client import SSHClient
from backup_dir import FolderCopier

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(r"C:\STORAGE\PYTHON\BackupConfigNginx_1.0\main.log"), logging.StreamHandler()]
    )

def main():
    remote_directory = "conf.d/"  
    current_backup = r"C:\STORAGE\PYTHON\BackupConfigNginx_1.0\backup"
    backup_old = r"C:\STORAGE\PYTHON\BackupConfigNginx_1.0\backup_old/"
    hostname = "ahmad.ftc.ru"  
    port = 22                       
    username = "nginx"      
    key_file = r"C:\STORAGE\Key\key" 
    days_to_keep = 30 #Глубина хранения в днях
    
    
    # Удаляем папки старше указанного количества дней
    logging.info(f'Удаляем папки старше {days_to_keep} дней')
    copier = FolderCopier(current_backup, backup_old)
    copier.remove_old_folders(days_to_keep)
    
   # Переносим текущий backup для хранения в backup_old/ 
    folder_copier = FolderCopier(current_backup, backup_old)
    logging.info(f'Переносим старые файлы для хранения в {backup_old}')
    folder_copier.copy_folder()
    logging.info(f'Копирование файлов в {backup_old} завершено')
    
    
    # Скачиваем новый backup с сервера в backup/
    logging.info(f'Копируем новые файлы с сервера {hostname} в {current_backup}')   
    try:  
        ssh_client = SSHClient(hostname, port, username, key_file)
        ssh_client.connect()    
        ssh_client.download_all_files_from_directory(remote_directory, current_backup)
        logging.info('Загрузка файлов завершена')
    except Exception as e:
        logging.error(f'Ошибка при загрузке файлов: {e}')
    finally:
        ssh_client.close()
        logging.info('Соединение закрыто')
    
    logging.info('Backup конфигураций nginx создан успешно ')        

if __name__ == "__main__":
    main()