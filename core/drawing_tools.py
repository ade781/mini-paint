# core/drawing_tools.py

# Import pustaka yang mungkin diperlukan untuk menggambar
# from PIL import ImageDraw

class BaseTool:
    """
    Kelas dasar abstrak untuk semua alat gambar.
    """

    def __init__(self, drawing_context):
        self.drawing_context = drawing_context  # Objek PIL ImageDraw

    def start_draw(self, x: int, y: int):
        """
        Dipanggil saat mouse ditekan untuk memulai operasi gambar.
        """
        raise NotImplementedError

    def draw(self, x1: int, y1: int, x2: int, y2: int):
        """
        Dipanggil saat mouse digeser untuk melanjutkan operasi gambar.
        """
        raise NotImplementedError

    def end_draw(self, x: int, y: int):
        """
        Dipanggil saat mouse dilepas untuk mengakhiri operasi gambar.
        """
        raise NotImplementedError


class BrushTool(BaseTool):
    """
    Alat kuas untuk menggambar garis bebas.
    """

    def __init__(self, drawing_context, color: str, size: int):
        super().__init__(drawing_context)
        self.color = color
        self.size = size
        self._last_x, self._last_y = None, None

    def start_draw(self, x: int, y: int):
        self._last_x, self._last_y = x, y

    def draw(self, x1: int, y1: int, x2: int, y2: int):
        if self._last_x is not None:
            try:
                # Menggambar garis antara titik terakhir dan titik saat ini
                self.drawing_context.line(
                    [self._last_x, self._last_y, x2, y2],
                    fill=self.color,
                    width=self.size,
                    joint="curve"  # Membuat garis lebih halus
                )
                self._last_x, self._last_y = x2, y2
            except ImportError:
                print("PIL tidak terinstal, tidak dapat menggambar dengan kuas.")

    def end_draw(self, x: int, y: int):
        self._last_x, self._last_y = None, None


class EraserTool(BaseTool):
    """
    Alat penghapus, pada dasarnya adalah kuas yang menggambar dengan warna latar belakang.
    """

    def __init__(self, drawing_context, background_color: str, size: int):
        super().__init__(drawing_context)
        self.color = background_color  # Warna penghapus adalah warna latar belakang
        self.size = size
        self._last_x, self._last_y = None, None

    def start_draw(self, x: int, y: int):
        self._last_x, self._last_y = x, y

    def draw(self, x1: int, y1: int, x2: int, y2: int):
        if self._last_x is not None:
            try:
                self.drawing_context.line(
                    [self._last_x, self._last_y, x2, y2],
                    fill=self.color,
                    width=self.size,
                    joint="curve"
                )
                self._last_x, self._last_y = x2, y2
            except ImportError:
                print("PIL tidak terinstal, tidak dapat menghapus.")

    def end_draw(self, x: int, y: int):
        self._last_x, self._last_y = None, None


class LineTool(BaseTool):
    """
    Alat garis lurus.
    """

    def __init__(self, drawing_context, color: str, size: int):
        super().__init__(drawing_context)
        self.color = color
        self.size = size
        self._start_x, self._start_y = None, None
        self._current_line_id = None  # Untuk menggambar garis pratinjau

    def start_draw(self, x: int, y: int):
        self._start_x, self._start_y = x, y
        # Buat pratinjau garis di kanvas Tkinter (bukan di gambar PIL)
        # Akan diimplementasikan di CanvasManager nanti
        # self._current_line_id = self.drawing_context.canvas.create_line(...)

    def draw(self, x1: int, y1: int, x2: int, y2: int):
        # Update pratinjau garis
        # self.drawing_context.canvas.coords(self._current_line_id, self._start_x, self._start_y, x2, y2)
        pass  # Tidak langsung menggambar di PIL Image saat drag untuk alat bentuk

    def end_draw(self, x: int, y: int):
        if self._start_x is not None:
            try:
                # Hapus pratinjau
                # self.drawing_context.canvas.delete(self._current_line_id)
                # Gambar garis final ke gambar PIL
                self.drawing_context.line(
                    [self._start_x, self._start_y, x, y],
                    fill=self.color,
                    width=self.size
                )
            except ImportError:
                print("PIL tidak terinstal, tidak dapat menggambar garis.")
            finally:
                self._start_x, self._start_y = None, None
                self._current_line_id = None


class RectangleTool(BaseTool):
    """
    Alat persegi panjang.
    """

    def __init__(self, drawing_context, color: str, size: int, fill: bool = False):
        super().__init__(drawing_context)
        self.color = color
        self.size = size  # Untuk outline
        self.fill = fill
        self._start_x, self._start_y = None, None
        self._current_rect_id = None

    def start_draw(self, x: int, y: int):
        self._start_x, self._start_y = x, y
        # Buat pratinjau persegi panjang
        # self._current_rect_id = self.drawing_context.canvas.create_rectangle(...)

    def draw(self, x1: int, y1: int, x2: int, y2: int):
        # Update pratinjau persegi panjang
        # self.drawing_context.canvas.coords(self._current_rect_id, self._start_x, self._start_y, x2, y2)
        pass

    def end_draw(self, x: int, y: int):
        if self._start_x is not None:
            try:
                # Hapus pratinjau
                # self.drawing_context.canvas.delete(self._current_rect_id)
                # Gambar persegi panjang final ke gambar PIL
                bbox = [self._start_x, self._start_y, x, y]
                if self.fill:
                    self.drawing_context.rectangle(bbox, fill=self.color)
                else:
                    self.drawing_context.rectangle(
                        bbox, outline=self.color, width=self.size)
            except ImportError:
                print("PIL tidak terinstal, tidak dapat menggambar persegi panjang.")
            finally:
                self._start_x, self._start_y = None, None
                self._current_rect_id = None

# Anda bisa menambahkan alat gambar lainnya di sini, seperti:
# CircleTool, ElipseTool, TextTool, FillTool, SelectionTool, dll.
