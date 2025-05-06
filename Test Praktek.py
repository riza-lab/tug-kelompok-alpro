import csv
from datetime import datetime
import os

# Nama file CSV untuk menyimpan data
DATA_FILE = "data_mobil.csv"

# Daftar kolom dalam file
FIELDNAMES = ['NoPol', 'NamaPemilik', 'MerkMobil', 'MasaBerlaku', 'BahanBakar']

# Fungsi untuk memuat data dari file
def load_data():
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            data = list(reader)
    return data

# Fungsi untuk menyimpan data ke file
def save_data(data):
    with open(DATA_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(data)

# Fungsi untuk menampilkan semua data
def lihat_data():
    data = load_data()
    if not data:
        print("Data masih kosong.")
        return
    print("\nData Mobil:")
    for i, row in enumerate(data, start=1):
        print(f"{i}. {row['NoPol']} - {row['NamaPemilik']} - {row['MerkMobil']} - Berlaku sampai: {row['MasaBerlaku']} - BBM: {row['BahanBakar']}")

# Fungsi untuk menambahkan data
def tambah_data():
    data = load_data()
    nopol = input("Masukkan No. Polisi: ")
    pemilik = input("Masukkan Nama Pemilik: ")
    merk = input("Masukkan Merk Mobil: ")
    berlaku = input("Masukkan Masa Berlaku (format: YYYY-MM-DD): ")
    bbm = input("Masukkan Jenis Bahan Bakar: ")

    data.append({
        'NoPol': nopol,
        'NamaPemilik': pemilik,
        'MerkMobil': merk,
        'MasaBerlaku': berlaku,
        'BahanBakar': bbm
    })

    save_data(data)
    print("Data berhasil ditambahkan.")

# Fungsi untuk mengedit data
def edit_data():
    data = load_data()
    nopol = input("Masukkan No. Polisi yang ingin diedit: ")

    for row in data:
        if row['NoPol'] == nopol:
            print("Data ditemukan. Masukkan data baru.")
            row['NamaPemilik'] = input("Nama Pemilik baru: ")
            row['MerkMobil'] = input("Merk Mobil baru: ")
            row['MasaBerlaku'] = input("Masa Berlaku baru (YYYY-MM-DD): ")
            row['BahanBakar'] = input("Jenis Bahan Bakar baru: ")
            save_data(data)
            print("Data berhasil diperbarui.")
            return

    print("No. Polisi tidak ditemukan.")

# Fungsi untuk menghapus data
def hapus_data():
    data = load_data()
    nopol = input("Masukkan No. Polisi yang ingin dihapus: ")
    new_data = [row for row in data if row['NoPol'] != nopol]

    if len(new_data) == len(data):
        print("No. Polisi tidak ditemukan.")
    else:
        save_data(new_data)
        print("Data berhasil dihapus.")

# Fungsi untuk menghitung sisa masa berlaku
def cek_masa_berlaku():
    data = load_data()
    nopol = input("Masukkan No. Polisi yang ingin dicek: ")

    for row in data:
        if row['NoPol'] == nopol:
            try:
                masa_berlaku = datetime.strptime(row['MasaBerlaku'], "%Y-%m-%d")
                sekarang = datetime.now()
                selisih = (masa_berlaku.year - sekarang.year) * 12 + masa_berlaku.month - sekarang.month
                print(f"Sisa masa berlaku No. Polisi {nopol}: {selisih} bulan lagi.")
            except ValueError:
                print("Format tanggal tidak valid. Harus YYYY-MM-DD.")
            return

    print("No. Polisi tidak ditemukan.")

# Menu utama aplikasi
def main():
    while True:
        print("\n=== MENU PENGELOLAAN DATA MOBIL ===")
        print("1. Lihat Data Mobil")
        print("2. Tambah Data Mobil")
        print("3. Edit Data Mobil")
        print("4. Hapus Data Mobil")
        print("5. Cek Masa Berlaku No. Polisi")
        print("6. Keluar")

        pilihan = input("Pilih menu (1-6): ")

        if pilihan == '1':
            lihat_data()
        elif pilihan == '2':
            tambah_data()
        elif pilihan == '3':
            edit_data()
        elif pilihan == '4':
            hapus_data()
        elif pilihan == '5':
            cek_masa_berlaku()
        elif pilihan == '6':
            print("Terima kasih. Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

# Menjalankan program
if __name__ == "__main__":
    main()
