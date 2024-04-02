import socket

def cek_koneksi(server_ip, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((server_ip, server_port))
        return "Koneksi berhasil terhubung ke server tujuan."
    except socket.error as err:
        return f"Gagal terhubung ke server tujuan: {err}"
    finally:
        sock.close()

server_ip = '2.0.0.217'
server_port = 80

try:
    response = cek_koneksi(server_ip, server_port)
    print(response)
except Exception as e:
    print(f"Terjadi kesalahan: {e}")
