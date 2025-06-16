# ui/menus.py

import tkinter as tk


class MainMenu:
    """
    Mengelola menu bar utama aplikasi (File, Edit, View, Tools, Help).
    """

    def __init__(self, root: tk.Tk, app_instance):
        """
        Inisialisasi menu bar.

        Args:
            root (tk.Tk): Objek Tkinter root window.
            app_instance: Instance dari kelas Application.
        """
        self.root = root
        self.app = app_instance
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self._create_file_menu()
        self._create_edit_menu()
        self._create_tools_menu()
        self._create_help_menu()

        print("Menu bar diinisialisasi.")

    def _create_file_menu(self):
        """
        Membuat menu 'File'.
        """
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label="New", command=self.app.clear_canvas, accelerator="Ctrl+N")
        file_menu.add_command(
            label="Open...", command=self.app.main_window.open_file, accelerator="Ctrl+O")
        file_menu.add_command(
            label="Save", command=self.app.main_window.save_file, accelerator="Ctrl+S")
        file_menu.add_command(
            label="Save As...", command=self.app.main_window.save_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Bind keyboard shortcuts
        self.root.bind_all(
            "<Control-n>", lambda event: self.app.clear_canvas())
        self.root.bind_all(
            "<Control-o>", lambda event: self.app.main_window.open_file())
        self.root.bind_all(
            "<Control-s>", lambda event: self.app.main_window.save_file())
        self.root.bind_all("<Control-Shift-s>",
                           lambda event: self.app.main_window.save_file())
        print("Menu 'File' dibuat.")

    def _create_edit_menu(self):
        """
        Membuat menu 'Edit'.
        """
        edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(
            label="Undo", command=self.app.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(
            label="Redo", command=self.app.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear Canvas",
                              command=self.app.clear_canvas)

        # Bind keyboard shortcuts
        self.root.bind_all("<Control-z>", lambda event: self.app.undo())
        self.root.bind_all("<Control-y>", lambda event: self.app.redo())
        print("Menu 'Edit' dibuat.")

    def _create_tools_menu(self):
        """
        Membuat menu 'Tools'.
        """
        tools_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(
            label="Brush", command=lambda: self.app.set_tool("brush"))
        tools_menu.add_command(
            label="Eraser", command=lambda: self.app.set_tool("eraser"))
        tools_menu.add_command(
            label="Line", command=lambda: self.app.set_tool("line"))
        tools_menu.add_command(
            label="Rectangle", command=lambda: self.app.set_tool("rectangle"))
        # Anda dapat menambahkan lebih banyak alat di sini
        tools_menu.add_separator()
        tools_menu.add_command(label="Color Picker...",
                               command=self.app.main_window.show_color_picker)
        print("Menu 'Tools' dibuat.")

    def _create_help_menu(self):
        """
        Membuat menu 'Help'.
        """
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(
            label="About", command=self.app.main_window.show_about_dialog)
        print("Menu 'Help' dibuat.")
