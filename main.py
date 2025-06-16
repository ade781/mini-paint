from core.application import Application
import tkinter as tk
import sys
import os
import time  # Import modul time untuk mengukur durasi

# Menambahkan direktori 'core' ke path sistem agar modul dapat diimpor
# Ini penting karena Application akan berada di 'core/application.py'
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'core')))
# Juga tambahkan direktori 'ui', 'features', dan 'utils' ke path sistem
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'ui')))
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'features')))
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'utils')))


def main():
    """
    Fungsi utama untuk menjalankan aplikasi Paint yang kompleks.
    """
    start_time_main = time.time()  # Mulai pengukuran waktu untuk main.py

    root = tk.Tk()

    # Nonaktifkan root.withdraw() jika Anda ingin jendela utama langsung terlihat
    # root.withdraw() # Sembunyikan jendela root sementara selama inisialisasi

    app = Application(root)
    app.run()

    end_time_main = time.time()  # Akhiri pengukuran waktu untuk main.py
    print(
        f"DEBUG: main.py selesai dalam {end_time_main - start_time_main:.4f} detik.")


if __name__ == "__main__":
    main()
