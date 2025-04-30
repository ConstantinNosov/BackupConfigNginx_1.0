import paramiko
import os

class SSHClient:
    def __init__(self, hostname, port, username, key_file):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.key_file = key_file
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sftp_client = None  

    # Подключение к серверу
    def connect(self):
        try:
            self.client.connect(self.hostname, port=self.port, username=self.username, key_filename=self.key_file)
            self.sftp_client = self.client.open_sftp()  
            return True 
        except Exception as e:
            return False, f"Ошибка соединения: {str(e)}"
        
    # Загрузка файла с сервера         
    def download_file_with_replacement(self, remote_file_path, local_file_path):
        try:
            self.sftp_client.stat(remote_file_path)
            self.sftp_client.get(remote_file_path, local_file_path)
            return True, None 
        except FileNotFoundError as e:
            return False, f"Файл не найден: {str(e)}"
        except paramiko.SSHException as ssh_error:
            return False, f"Ошибка SSH: {str(ssh_error)}"
        except Exception as e:
            return False, f"Произошла ошибка: {str(e)}" 
                           
    # Загрузка директории с содержимым           
    def download_all_files_from_directory(self, remote_directory, local_directory):
        results = []
        try:
            if not os.path.exists(local_directory):
                os.makedirs(local_directory)
            for filename in self.sftp_client.listdir(remote_directory):
                remote_file_path = os.path.join(remote_directory, filename)
                local_file_path = os.path.join(local_directory, filename)
                success, error = self.download_file_with_replacement(remote_file_path, local_file_path)
                if not success:
                    results.append((filename, error))
        except Exception as e:
             return False, f"Произошла ошибка: {str(e)}"
        
        return True, results  
                         
    # Закрыть соединение           
    def close(self):
        if self.sftp_client:
            self.sftp_client.close()  
        self.client.close()  
                         