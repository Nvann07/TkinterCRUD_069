import tkinter as tk
from tkinter import messagebox
import sqlite3


# 1. Buat Database

conn = sqlite3.connect("nilai.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS nilai_siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_siswa TEXT,
    biologi INTEGER,
    fisika INTEGER,
    inggris INTEGER,
    prediksi_fakultas TEXT
)
""")

conn.commit()

# 2. Fungsi Hitung & Simpan

def submit_nilai():
    nama = entry_nama.get()
    bio = entry_biologi.get()
    fis = entry_fisika.get()
    ing = entry_inggris.get()

    # Validasi input
    if not(nama and bio and fis and ing):
        messagebox.showerror("Error", "Semua field harus diisi!")
        return

    try:
        bio = int(bio)
        fis = int(fis)
        ing = int(ing)
    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka!")
        return

    # Logika Prediksi Fakultas
    if bio > fis and bio > ing:
        prediksi = "Kedokteran"
    elif fis > bio and fis > ing:
        prediksi = "Teknik"
    else:
        prediksi = "Bahasa"

    # Simpan ke database
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, prediksi))
    conn.commit()

    messagebox.showinfo("Sukses", f"Data disimpan!\nPrediksi Fakultas: {prediksi}")

    entry_nama.delete(0, tk.END)
    entry_biologi.delete(0, tk.END)
    entry_fisika.delete(0, tk.END)
    entry_inggris.delete(0, tk.END)


# 3. Fungsi SELECT Data

def lihat_data():
    # Ambil semua data dari SQLite
    cursor.execute("SELECT * FROM nilai_siswa")
    data = cursor.fetchall()

    # Buat window baru
    win = tk.Toplevel(root)
    win.title("Data Nilai Siswa")
    win.geometry("600x400")

    # Header
    header = "ID | Nama Siswa | Biologi | Fisika | Inggris | Prediksi Fakultas\n"
    tk.Label(win, text=header, font=("Arial", 10, "bold")).pack()

    # List data
    text_area = tk.Text(win, width=80, height=20)
    text_area.pack()

    for row in data:
        line = f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}\n"
        text_area.insert(tk.END, line)


# 4. Tkinter GUI

root = tk.Tk()
root.title("Prediksi Fakultas Siswa")
root.geometry("400x380")

tk.Label(root, text="Nama Siswa:").pack()
entry_nama = tk.Entry(root)
entry_nama.pack()

tk.Label(root, text="Nilai Biologi:").pack()
entry_biologi = tk.Entry(root)
entry_biologi.pack()

tk.Label(root, text="Nilai Fisika:").pack()
entry_fisika = tk.Entry(root)
entry_fisika.pack()

tk.Label(root, text="Nilai Inggris:").pack()
entry_inggris = tk.Entry(root)
entry_inggris.pack()

# Button Submit
btn_submit = tk.Button(root, text="Submit Nilai", command=submit_nilai)
btn_submit.pack(pady=10)

# Button Lihat Data
btn_lihat = tk.Button(root, text="Lihat Data", command=lihat_data)
btn_lihat.pack(pady=5)

root.mainloop()
