import tkinter as tk
from tkinter import messagebox, ttk
import csv
from datetime import datetime
import os

DATA_FILE = "data_mobil.csv"
FIELDNAMES = ['NoPol', 'NamaPemilik', 'MerkMobil', 'MasaBerlaku', 'BahanBakar']

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

def save_data(data):
    with open(DATA_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(data)

class MobilApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Data Mobil")

        self.tree = ttk.Treeview(root, columns=FIELDNAMES, show='headings')
        for col in FIELDNAMES:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(padx=10, pady=10, fill='x')

        self.load_table()

        # Tombol-tombol
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Button(frame, text="Tambah", command=self.tambah).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Edit", command=self.edit).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Hapus", command=self.hapus).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Cek Masa Berlaku", command=self.cek_masa_berlaku).grid(row=0, column=3, padx=5)
        tk.Button(frame, text="Refresh", command=self.load_table).grid(row=0, column=4, padx=5)

    def load_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in load_data():
            self.tree.insert('', 'end', values=[row[col] for col in FIELDNAMES])

    def tambah(self):
        self.buka_form("Tambah Data Mobil")

    def edit(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data terlebih dahulu.")
            return
        values = self.tree.item(selected[0])['values']
        self.buka_form("Edit Data Mobil", values)

    def hapus(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data untuk dihapus.")
            return
        nopol = self.tree.item(selected[0])['values'][0]
        data = load_data()
        new_data = [row for row in data if row['NoPol'] != nopol]
        save_data(new_data)
        self.load_table()
        messagebox.showinfo("Sukses", "Data berhasil dihapus.")

    def cek_masa_berlaku(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data terlebih dahulu.")
            return
        values = self.tree.item(selected[0])['values']
        try:
            masa_berlaku = datetime.strptime(values[3], "%Y-%m-%d")
            sekarang = datetime.now()
            selisih = (masa_berlaku.year - sekarang.year) * 12 + (masa_berlaku.month - sekarang.month)
            messagebox.showinfo("Info", f"No. Polisi {values[0]} berlaku {selisih} bulan lagi.")
        except:
            messagebox.showerror("Error", "Format tanggal tidak valid (harus YYYY-MM-DD).")

    def buka_form(self, title, data=None):
        form = tk.Toplevel(self.root)
        form.title(title)

        labels = ["No. Polisi", "Nama Pemilik", "Merk Mobil", "Masa Berlaku (YYYY-MM-DD)", "Jenis Bahan Bakar"]
        entries = []

        for i, label in enumerate(labels):
            tk.Label(form, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
            entry = tk.Entry(form)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        if data:
            for i, value in enumerate(data):
                entries[i].insert(0, value)
            entries[0].config(state='disabled')  # NoPol tidak bisa diedit

        def simpan():
            input_data = [e.get().strip() for e in entries]
            if any(not val for val in input_data):
                messagebox.showerror("Error", "Semua kolom harus diisi.")
                return

            all_data = load_data()

            if data:  # Edit
                for row in all_data:
                    if row['NoPol'] == input_data[0]:
                        row.update(dict(zip(FIELDNAMES, input_data)))
                        break
            else:  # Tambah
                for row in all_data:
                    if row['NoPol'] == input_data[0]:
                        messagebox.showerror("Error", "No. Polisi sudah ada.")
                        return
                all_data.append(dict(zip(FIELDNAMES, input_data)))

            save_data(all_data)
            self.load_table()
            form.destroy()
            messagebox.showinfo("Sukses", "Data berhasil disimpan.")

        tk.Button(form, text="Simpan", command=simpan).grid(row=len(labels), columnspan=2, pady=10)

# Jalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = MobilApp(root)
    root.mainloop()
