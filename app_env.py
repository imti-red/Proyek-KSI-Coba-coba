import os
import sqlite3
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Mengambil secret key dari environment variable
SECRET_KEY_ENV = os.getenv("APP_SECRET_KEY")

if not SECRET_KEY_ENV:
    raise ValueError("Error: APP_SECRET_KEY tidak ditemukan di file .env atau environment!")

SECRET_KEY = SECRET_KEY_ENV.encode()

def inisialisasi_db():
    conn = sqlite3.connect('keuangan_env.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS catatan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_terenkripsi TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def simpan_catatan(pemasukan, pengeluaran, saldo):
    f = Fernet(SECRET_KEY)
    data_mentah = f"Pemasukan: {pemasukan} | Pengeluaran: {pengeluaran} | Saldo: {saldo}"
    ciphertext = f.encrypt(data_mentah.encode()).decode()

    conn = sqlite3.connect('keuangan_env.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO catatan (data_terenkripsi) VALUES (?)', (ciphertext,))
    conn.commit()
    conn.close()
    print("[Environment Variable] Data berhasil dienkripsi dan disimpan ke database.")

def baca_catatan():
    f = Fernet(SECRET_KEY)
    conn = sqlite3.connect('keuangan_env.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, data_terenkripsi FROM catatan')
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        teks_asli = f.decrypt(row[1].encode()).decode()
        print(f"[Environment Variable] ID: {row[0]} | Data Hasil Dekripsi: {teks_asli}")

if __name__ == "__main__":
    inisialisasi_db()
    simpan_catatan(5000000, 1500000, 3500000)
    baca_catatan()
    