import paramiko
import os

# Informasi SSH
hostname = '2.0.0.217'
port = 22
username = 'pswaix'
password = 'pswaix'

# Direktori dan nama file lokal
local_dir1 = '/home/projects/irwin/project_web/Backend/pythonWebMdo/'
local_dir2 = '/home/projects/irwin/project_web/Backend/pythonWebMdo/'
local_file1 = 'conn-up2.p'
local_file2 = 'connup2.sh'

# Direktori tujuan di server
remote_dir1 = '/u/pswaix/psw/1a/main/'
remote_dir2 = '/u/pswaix/psw/1a/bin/'

try:
    # Inisialisasi koneksi SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)

    # Upload file 1
    sftp = ssh.open_sftp()
    sftp.put(os.path.join(local_dir1, local_file1), os.path.join(remote_dir1, local_file1))
    sftp.close()

    # Upload file 2
    sftp = ssh.open_sftp()
    sftp.put(os.path.join(local_dir2, local_file2), os.path.join(remote_dir2, local_file2))
    sftp.close()

    # Jalankan perintah chmod dan file conndown2.sh
    stdin, stdout, stderr = ssh.exec_command(f'chmod 775 {remote_dir2}/{local_file2}')
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    if error:
        print(f"Error running chmod command: {error}")
    else:
        print("chmod command executed successfully.")

    # Jalankan perintah conndown2.sh dengan parameter 7168
    #stdin, stdout, stderr = ssh.exec_command(f'{remote_dir2}/{local_file2} 7168')
    stdin, stdout, stderr = ssh.exec_command(f'{remote_dir2}/{local_file2} 7168', get_pty=True)
    #output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    if error:
        print(f"Error running connup2.sh command: {error}")
    else:
        print("connup2.sh command executed successfully.")

finally:
    # Tutup koneksi SSH
    ssh.close()
