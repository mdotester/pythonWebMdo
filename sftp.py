from ftplib import FTP
import os
from functools import partial

# Informasi FTP
ftp_host = '2.0.0.217'
ftp_user = 'pswaix'
ftp_pass = 'pswaix'

# Directory dan nama file di lokal
local_dir1 = '/home/projects/irwin/project_web/Backend/pythonWebMdo/'
local_dir2 = '/home/projects/irwin/project_web/Backend/pythonWebMdo/'
file1 = 'conn-down2.p'
file2 = 'conndown2.sh'

# Directory di server FTP
ftp_dir1 = '/u/pswaix/psw/1a/main/'
ftp_dir2 = '/u/pswaix/psw/1a/bin/'
file_path = '/u/pswaix/psw/1a/bin/parm.sh'


def upload_file_ftp(local_dir, file_name, ftp_dir):
    # Koneksi FTP
    ftp = FTP(ftp_host)
    ftp.login(user=ftp_user, passwd=ftp_pass)

    # Pindah ke direktori FTP yang diinginkan
    ftp.cwd(ftp_dir)

    # Buka file lokal untuk diunggah
    with open(os.path.join(local_dir, file_name), 'rb') as file:
        ftp.storbinary(f'STOR {file_name}', file)

    # Untuk file .sh, berikan izin eksekusi dan jalankan
    if file_name == 'conndown2.sh':
        # Berikan izin eksekusi
        ftp.sendcmd(f'SITE CHMOD 775 {file_name}')

        # Jalankan file
        cmd = f'bash {file_name}'
        ftp.voidcmd(f'SITE {cmd}')

    # Tutup koneksi FTP
    ftp.quit()

# Upload file 1 ke direktori 1 di server FTP
upload_file_ftp(local_dir1, file1, ftp_dir1)

# Upload file 2 ke direktori 2 di server FTP
upload_file_ftp(local_dir2, file2, ftp_dir2)

print('Upload dan CHMOD selesai.')
