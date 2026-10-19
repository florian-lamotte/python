import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# === CONSTANTES ===
DEFAULT_ROTATION = -45.5
DEFAULT_CROP_WIDTH = 500
DEFAULT_CROP_HEIGHT = 500
DEFAULT_SCALE = 50
CANVAS_SIZE = 600

def update_entry(entry, value):
    entry.delete(0, tk.END)
    entry.insert(0, str(value))

class CadreEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Éditeur de coin de cadre")

        self.image_path = None
        self.original_image = None
        self.processed_image = None

        self.zoom_factor = 1.0
        self.zoom_step = 0.1
        self.image_offset_x = 0
        self.image_offset_y = 0
        self.drag_data = {"x": 0, "y": 0}
        self.canvas_image_id = None
        self.crop_rect_id = None
        self.rotated_image_cache = None
        self.cached_angle = None

        self.setup_ui()

    def setup_ui(self):
        self.setup_control_panel()
        self.setup_crop_controls()
        self.setup_rotation_controls()
        self.setup_canvas()
        self.setup_bindings()

    def setup_control_panel(self):
        control_frame = tk.Frame(self.master)
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="Charger une image", command=self.load_image).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Appliquer", command=self.apply_processing).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="Sauvegarder", command=self.save_image).grid(row=0, column=2, padx=5)

        tk.Label(control_frame, text="Rotation (°):").grid(row=1, column=0)
        self.rotation_entry = tk.Entry(control_frame, width=5)
        update_entry(self.rotation_entry, DEFAULT_ROTATION)
        self.rotation_entry.grid(row=1, column=1)

        tk.Label(control_frame, text="Crop (LxH):").grid(row=2, column=0)
        self.crop_width_entry = tk.Entry(control_frame, width=5)
        update_entry(self.crop_width_entry, DEFAULT_CROP_WIDTH)
        self.crop_width_entry.grid(row=2, column=1)

        self.crop_height_entry = tk.Entry(control_frame, width=5)
        update_entry(self.crop_height_entry, DEFAULT_CROP_HEIGHT)
        self.crop_height_entry.grid(row=2, column=2)

        tk.Label(control_frame, text="Réduction (%) :").grid(row=3, column=0)
        self.scale_entry = tk.Entry(control_frame, width=5)
        update_entry(self.scale_entry, DEFAULT_SCALE)
        self.scale_entry.grid(row=3, column=1)

    def setup_crop_controls(self):
        arrow_frame = tk.Frame(self.master)
        arrow_frame.pack()

        tk.Button(arrow_frame, text="↑", command=lambda: self.adjust_crop_size(0, -10)).grid(row=0, column=1)
        tk.Button(arrow_frame, text="←", command=lambda: self.adjust_crop_size(-10, 0)).grid(row=1, column=0)
        tk.Button(arrow_frame, text="→", command=lambda: self.adjust_crop_size(10, 0)).grid(row=1, column=2)
        tk.Button(arrow_frame, text="↓", command=lambda: self.adjust_crop_size(0, 10)).grid(row=2, column=1)

        self.size_label = tk.Label(self.master, text="Ajustement de la taille du crop (L x H)")
        self.size_label.pack(pady=5)

    def setup_rotation_controls(self):
        rotation_frame = tk.Frame(self.master)
        rotation_frame.pack(pady=5)

        tk.Label(rotation_frame, text="Ajuster la rotation (°)").grid(row=0, column=0, columnspan=4)

        tk.Button(rotation_frame, text="↺ -1°", command=lambda: self.adjust_rotation(-1)).grid(row=1, column=0, padx=5)
        tk.Button(rotation_frame, text="⮘ -0.5°", command=lambda: self.adjust_rotation(-0.5)).grid(row=1, column=1, padx=5)
        tk.Button(rotation_frame, text="⮚ +0.5°", command=lambda: self.adjust_rotation(0.5)).grid(row=1, column=2, padx=5)
        tk.Button(rotation_frame, text="↻ +1°", command=lambda: self.adjust_rotation(1)).grid(row=1, column=3, padx=5)

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.master, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="grey")
        self.canvas.pack(pady=10)

    def setup_bindings(self):
        self.master.bind("<Alt-Left>", lambda e: self.adjust_rotation(-1))
        self.master.bind("<Alt-Right>", lambda e: self.adjust_rotation(1))
        self.master.bind("<Shift-Left>", lambda e: self.adjust_rotation(-0.5))
        self.master.bind("<Shift-Right>", lambda e: self.adjust_rotation(0.5))

        self.master.bind("<Left>", lambda e: self.adjust_crop_size(-10, 0))
        self.master.bind("<Right>", lambda e: self.adjust_crop_size(10, 0))
        self.master.bind("<Up>", lambda e: self.adjust_crop_size(0, -10))
        self.master.bind("<Down>", lambda e: self.adjust_crop_size(0, 10))

        self.canvas.bind("<MouseWheel>", self.zoom_with_mouse)
        self.canvas.bind("<ButtonPress-1>", self.on_rect_click)
        self.canvas.bind("<B1-Motion>", self.on_rect_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_rect_release)

    def get_processing_params(self):
        try:
            angle = float(self.rotation_entry.get())
            crop_width = int(self.crop_width_entry.get())
            crop_height = int(self.crop_height_entry.get())
            scale = float(self.scale_entry.get()) / 100
            return angle, crop_width, crop_height, scale
        except ValueError:
            messagebox.showerror("Erreur", "Paramètres invalides.")
            return None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp")])
        if not file_path:
            return

        self.image_path = file_path
        self.original_image = Image.open(self.image_path).convert("RGBA")
        self.display_image(self.original_image)

    def apply_processing(self):
        if not self.original_image:
            messagebox.showwarning("Aucune image", "Chargez une image d'abord.")
            return

        params = self.get_processing_params()
        if not params:
            return
        angle, crop_width, crop_height, scale = params

        # === Étape 1 : Rotation (avec cache) ===
        if self.rotated_image_cache is None or self.cached_angle != angle:
            self.rotated_image_cache = self.original_image.rotate(angle, expand=True)
            self.cached_angle = angle

        rotated = self.rotated_image_cache
        rw, rh = rotated.size

        # === Étape 2 : récupérer position réelle du rectangle rouge sur l'image ===

        # Taille affichée après zoom
        display_width = int(rw * self.zoom_factor)
        display_height = int(rh * self.zoom_factor)

        # Centre du canvas
        canvas_center_x = CANVAS_SIZE // 2
        canvas_center_y = CANVAS_SIZE // 2

        # Position de l’image sur le canvas (avec offset)
        img_x = canvas_center_x + int(self.image_offset_x)
        img_y = canvas_center_y + int(self.image_offset_y)

        # Coin haut-gauche de l'image sur le canvas
        image_canvas_left = img_x - display_width // 2
        image_canvas_top = img_y - display_height // 2

        # Rectangle rouge sur le canvas
        rect_x1 = canvas_center_x - crop_width // 2
        rect_y1 = canvas_center_y - crop_height // 2
        rect_x2 = canvas_center_x + crop_width // 2
        rect_y2 = canvas_center_y + crop_height // 2

        # === Étape 3 : Convertir le rectangle rouge (canvas) vers coordonnées image ===

        # Coordonnées du rectangle rouge dans l'image pivotée réelle :
        crop_left = int((rect_x1 - image_canvas_left) / self.zoom_factor)
        crop_top = int((rect_y1 - image_canvas_top) / self.zoom_factor)
        crop_right = int((rect_x2 - image_canvas_left) / self.zoom_factor)
        crop_bottom = int((rect_y2 - image_canvas_top) / self.zoom_factor)

        # Clamp aux bords de l'image
        crop_left = max(0, crop_left)
        crop_top = max(0, crop_top)
        crop_right = min(rw, crop_right)
        crop_bottom = min(rh, crop_bottom)

        # === Étape 4 : Crop et Resize ===
        cropped = rotated.crop((crop_left, crop_top, crop_right, crop_bottom))

        new_width = max(1, int((crop_right - crop_left) * scale))
        new_height = max(1, int((crop_bottom - crop_top) * scale))
        resized = cropped.resize((new_width, new_height), resample=Image.LANCZOS)

        self.processed_image = resized
        self.display_image(resized)

    def save_image(self):
        if not self.processed_image:
            messagebox.showwarning("Rien à sauvegarder", "Cliquez sur 'Appliquer' d'abord.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if save_path:
            self.processed_image.save(save_path)
            messagebox.showinfo("Succès", f"Image sauvegardée :\n{save_path}")

    def display_image(self, img=None):
        if self.original_image is None:
            return

        params = self.get_processing_params()
        if not params:
            return
        angle, crop_width, crop_height, _ = params

        rotated = self.original_image.rotate(angle, expand=True)
        rw, rh = rotated.size

        # Redimensionner pour le canvas
        rotated.thumbnail((CANVAS_SIZE, CANVAS_SIZE), Image.LANCZOS)
        r_width, r_height = rotated.size

        zoomed_width = int(r_width * self.zoom_factor)
        zoomed_height = int(r_height * self.zoom_factor)
        display_img = rotated.resize((zoomed_width, zoomed_height), Image.LANCZOS)

        center_x = CANVAS_SIZE // 2
        center_y = CANVAS_SIZE // 2

        img_x = center_x + int(self.image_offset_x * self.zoom_factor)
        img_y = center_y + int(self.image_offset_y * self.zoom_factor)

        tk_img = ImageTk.PhotoImage(display_img)
        self.canvas.image = tk_img  # Référence pour éviter le garbage collection
        self.canvas.image = tk_img  # garde une référence
        if self.canvas_image_id:
            self.canvas.coords(self.canvas_image_id, img_x, img_y)
            self.canvas.itemconfig(self.canvas_image_id, image=tk_img)
        else:
            self.canvas_image_id = self.canvas.create_image(img_x, img_y, image=tk_img)

        # Rectangle rouge (zone de crop)
        scale_x = zoomed_width / rw
        scale_y = zoomed_height / rh
        rect_x1 = center_x - int(crop_width * scale_x / 2)
        rect_y1 = center_y - int(crop_height * scale_y / 2)
        rect_x2 = center_x + int(crop_width * scale_x / 2)
        rect_y2 = center_y + int(crop_height * scale_y / 2)
        if self.crop_rect_id:
            self.canvas.coords(self.crop_rect_id, rect_x1, rect_y1, rect_x2, rect_y2)
        else:
            self.crop_rect_id = self.canvas.create_rectangle(
                rect_x1, rect_y1, rect_x2, rect_y2, outline="red", width=2
            )

    def adjust_crop_size(self, dx, dy):
        try:
            width = max(10, int(self.crop_width_entry.get()) + dx)
            height = max(10, int(self.crop_height_entry.get()) + dy)
            update_entry(self.crop_width_entry, width)
            update_entry(self.crop_height_entry, height)
            self.quick_crop_update()
        except ValueError:
            messagebox.showerror("Erreur", "Dimensions invalides.")

    def adjust_rotation(self, delta_angle):
        try:
            current_angle = float(self.rotation_entry.get())
            new_angle = current_angle + delta_angle
            update_entry(self.rotation_entry, new_angle)
            self.apply_processing()
        except ValueError:
            messagebox.showerror("Erreur", "Angle invalide.")

    def zoom_with_mouse(self, event):
        if event.delta > 0:
            self.zoom_factor += self.zoom_step
        elif event.delta < 0:
            self.zoom_factor = max(0.1, self.zoom_factor - self.zoom_step)

        self.display_image(self.processed_image or self.original_image)

    def on_rect_click(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_rect_drag(self, event):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        
        self.image_offset_x += dx / self.zoom_factor
        self.image_offset_y += dy / self.zoom_factor

        if self.canvas_image_id:
            self.canvas.move(self.canvas_image_id, dx, dy)

    def on_rect_release(self, event):
        self.display_image()

    def quick_crop_update(self):
        """Mise à jour rapide du rectangle sans recalculer l'image."""
        self.display_image(self.processed_image or self.original_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = CadreEditor(root)
    root.mainloop()