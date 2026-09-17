import sqlite3
from cryptography.fernet import Fernet

# Kunci rahasia ditulis langsung di dalam kode sumber


def inisialisasi_db():
    conn = sqlite3.connect('keuangan_hardcoded.db')
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

    conn = sqlite3.connect('keuangan_hardcoded.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO catatan (data_terenkripsi) VALUES (?)', (ciphertext,))
    conn.commit()
    conn.close()
    print("[Hardcoded] Data berhasil dienkripsi dan disimpan.")

def baca_catatan():
    f = Fernet(SECRET_KEY)
    conn = sqlite3.connect('keuangan_hardcoded.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, data_terenkripsi FROM catatan')
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        teks_asli = f.decrypt(row[1].encode()).decode()
        print(f"[Hardcoded] ID: {row[0]} | Data Dekripsi: {teks_asli}")

if __name__ == "__main__":
    inisialisasi_db()
    simpan_catatan(5000000, 1500000, 3500000)
    baca_catatan()