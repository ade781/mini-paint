# main.py

import tkinter as tk
from src.app import PaintApp


def main():
    """
    Titik masuk utama aplikasi Paint.
    Menginisialisasi jendela Tkinter dan menjalankan aplikasi.
    """
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
