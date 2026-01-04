"""Passport Photo Editor - A GUI application for enhancing passport and visa photos."""

import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageEnhance, ImageTk


class PassportPhotoEditor:
    """GUI application for editing and enhancing passport/visa photos."""

    def __init__(self, root):
        """Initialize the application with the main window."""
        self.root = root
        self.root.title("Passport Photo Editor v1.0.1")
        self.root.geometry("1000x750")
        self.root.configure(bg="#f0f0f0")

        self.image = None
        self.original_image = None
        self.image_path = None

        # Default enhancement values
        self.brightness_val = 1.2
        self.contrast_val = 1.15
        self.color_val = 1.1
        self.sharpness_val = 1.1

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface."""
        # Top frame for file operations
        top_frame = tk.Frame(self.root, bg="#f0f0f0")
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(top_frame, text="Open Image", command=self.open_image,
                  bg="#4CAF50", fg="white", padx=10, pady=5).pack(
                      side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Save Image", command=self.save_image,
                  bg="#2196F3", fg="white", padx=10, pady=5).pack(
                      side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Reset", command=self.reset_image,
                  bg="#FF9800", fg="white", padx=10, pady=5).pack(
                      side=tk.LEFT, padx=5)

        # Main content frame
        content_frame = tk.Frame(self.root, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel - Image display
        left_panel = tk.Frame(content_frame, bg="white",
                              relief=tk.SUNKEN, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tk.Label(left_panel, text="Image Preview", bg="white",
                 font=("Arial", 10, "bold")).pack(pady=5)
        self.image_label = tk.Label(left_panel, bg="white",
                                    text="No image loaded")
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Right panel - Controls
        right_panel = tk.Frame(content_frame, bg="white",
                               relief=tk.SUNKEN, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0), pady=0)
        right_panel.config(width=280)
        right_panel.pack_propagate(False)

        tk.Label(right_panel, text="Adjustments", bg="white",
                 font=("Arial", 11, "bold")).pack(pady=10)

        # Brightness slider
        self.brightness_frame = tk.Frame(right_panel, bg="white")
        self.brightness_frame.pack(fill=tk.X, padx=15, pady=8)
        tk.Label(self.brightness_frame, text="Brightness", bg="white",
                 font=("Arial", 9)).pack(anchor=tk.W)
        self.brightness_scale = tk.Scale(
            self.brightness_frame, from_=0.5, to=2.0, resolution=0.05,
            orient=tk.HORIZONTAL, command=self.update_preview, bg="white")
        self.brightness_scale.set(self.brightness_val)
        self.brightness_scale.pack(fill=tk.X, pady=5)
        self.brightness_label = tk.Label(
            self.brightness_frame, text=f"{self.brightness_val:.2f}x",
            bg="white", fg="#666", font=("Arial", 9))
        self.brightness_label.pack(anchor=tk.E)

        # Contrast slider
        self.contrast_frame = tk.Frame(right_panel, bg="white")
        self.contrast_frame.pack(fill=tk.X, padx=15, pady=8)
        tk.Label(self.contrast_frame, text="Contrast", bg="white",
                 font=("Arial", 9)).pack(anchor=tk.W)
        self.contrast_scale = tk.Scale(
            self.contrast_frame, from_=0.5, to=2.0, resolution=0.05,
            orient=tk.HORIZONTAL, command=self.update_preview, bg="white")
        self.contrast_scale.set(self.contrast_val)
        self.contrast_scale.pack(fill=tk.X, pady=5)
        self.contrast_label = tk.Label(
            self.contrast_frame, text=f"{self.contrast_val:.2f}x",
            bg="white", fg="#666", font=("Arial", 9))
        self.contrast_label.pack(anchor=tk.E)

        # Color saturation slider
        self.color_frame = tk.Frame(right_panel, bg="white")
        self.color_frame.pack(fill=tk.X, padx=15, pady=8)
        tk.Label(self.color_frame, text="Saturation", bg="white",
                 font=("Arial", 9)).pack(anchor=tk.W)
        self.color_scale = tk.Scale(
            self.color_frame, from_=0.5, to=2.0, resolution=0.05,
            orient=tk.HORIZONTAL, command=self.update_preview, bg="white")
        self.color_scale.set(self.color_val)
        self.color_scale.pack(fill=tk.X, pady=5)
        self.color_label = tk.Label(
            self.color_frame, text=f"{self.color_val:.2f}x",
            bg="white", fg="#666", font=("Arial", 9))
        self.color_label.pack(anchor=tk.E)

        # Sharpness slider
        self.sharpness_frame = tk.Frame(right_panel, bg="white")
        self.sharpness_frame.pack(fill=tk.X, padx=15, pady=8)
        tk.Label(self.sharpness_frame, text="Sharpness", bg="white",
                 font=("Arial", 9)).pack(anchor=tk.W)
        self.sharpness_scale = tk.Scale(
            self.sharpness_frame, from_=0.5, to=2.0, resolution=0.05,
            orient=tk.HORIZONTAL, command=self.update_preview, bg="white")
        self.sharpness_scale.set(self.sharpness_val)
        self.sharpness_scale.pack(fill=tk.X, pady=5)
        self.sharpness_label = tk.Label(
            self.sharpness_frame, text=f"{self.sharpness_val:.2f}x",
            bg="white", fg="#666", font=("Arial", 9))
        self.sharpness_label.pack(anchor=tk.E)

        # Preset buttons
        tk.Label(right_panel, text="Presets", bg="white",
                 font=("Arial", 11, "bold")).pack(pady=(15, 10))

        button_frame = tk.Frame(right_panel, bg="white")
        button_frame.pack(fill=tk.X, padx=15, pady=5)
        tk.Button(button_frame, text="Passport", command=self.preset_passport,
                  bg="#9C27B0", fg="white", width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Visa", command=self.preset_visa,
                  bg="#9C27B0", fg="white", width=12).pack(side=tk.LEFT, padx=2)

        button_frame2 = tk.Frame(right_panel, bg="white")
        button_frame2.pack(fill=tk.X, padx=15, pady=5)
        tk.Button(button_frame2, text="Bright", command=self.preset_bright,
                  bg="#9C27B0", fg="white", width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame2, text="Neutral", command=self.preset_neutral,
                  bg="#9C27B0", fg="white", width=12).pack(side=tk.LEFT, padx=2)

    def open_image(self):
        """Open an image file and display it."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                       ("All files", "*.*")]
        )
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            if self.original_image.mode != 'RGB':
                self.original_image = self.original_image.convert('RGB')
            self.image = self.original_image.copy()
            self.update_preview()
            self.root.title(
                f"Passport Photo Editor - {os.path.basename(file_path)}")

    def update_preview(self, *args):
        """Update the image preview with current adjustment values."""
        if self.original_image is None:
            return

        # Update values from sliders
        self.brightness_val = self.brightness_scale.get()
        self.contrast_val = self.contrast_scale.get()
        self.color_val = self.color_scale.get()
        self.sharpness_val = self.sharpness_scale.get()

        # Update labels
        self.brightness_label.config(text=f"{self.brightness_val:.2f}x")
        self.contrast_label.config(text=f"{self.contrast_val:.2f}x")
        self.color_label.config(text=f"{self.color_val:.2f}x")
        self.sharpness_label.config(text=f"{self.sharpness_val:.2f}x")

        # Apply enhancements
        img = self.original_image.copy()

        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(self.brightness_val)

        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(self.contrast_val)

        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(self.color_val)

        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(self.sharpness_val)

        self.image = img

        # Display preview
        img_display = img.copy()
        img_display.thumbnail((500, 600), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img_display)
        self.image_label.config(image=photo, text="")
        self.image_label.image = photo

    def save_image(self):
        """Save the edited image to a file."""
        if self.image is None:
            messagebox.showwarning(
                "Warning", "No image to save. Please open an image first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"),
                       ("All files", "*.*")],
            initialfile=f"{Path(self.image_path).stem}_whitened.jpg"
        )

        if file_path:
            self.image.save(file_path, quality=95)
            messagebox.showinfo(
                "Success", f"Image saved successfully!\n{file_path}")

    def reset_image(self):
        """Reset all adjustments to default values."""
        if self.original_image is None:
            messagebox.showwarning("Warning", "No image loaded.")
            return

        self.brightness_scale.set(1.2)
        self.contrast_scale.set(1.15)
        self.color_scale.set(1.1)
        self.sharpness_scale.set(1.1)
        self.update_preview()

    def preset_passport(self):
        """Apply passport photo preset settings."""
        self.brightness_scale.set(1.2)
        self.contrast_scale.set(1.15)
        self.color_scale.set(1.1)
        self.sharpness_scale.set(1.1)
        self.update_preview()

    def preset_visa(self):
        """Apply visa photo preset settings."""
        self.brightness_scale.set(1.3)
        self.contrast_scale.set(1.2)
        self.color_scale.set(1.05)
        self.sharpness_scale.set(1.15)
        self.update_preview()

    def preset_bright(self):
        """Apply bright photo preset settings."""
        self.brightness_scale.set(1.5)
        self.contrast_scale.set(1.25)
        self.color_scale.set(1.2)
        self.sharpness_scale.set(1.2)
        self.update_preview()

    def preset_neutral(self):
        """Apply neutral (no change) preset settings."""
        self.brightness_scale.set(1.0)
        self.contrast_scale.set(1.0)
        self.color_scale.set(1.0)
        self.sharpness_scale.set(1.0)
        self.update_preview()


if __name__ == "__main__":
    root = tk.Tk()
    app = PassportPhotoEditor(root)
    root.mainloop()