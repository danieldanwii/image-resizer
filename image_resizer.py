import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os

def resize_images(input_folder, output_folder, width, height):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', 'JPG')):
            with Image.open(os.path.join(input_folder, filename)) as img:
                image_resized = img.resize((height, width))

                # Get the original orientation and rotate if necessary
                if hasattr(img, '_getexif'):
                    exif = img._getexif()
                    if exif is not None:
                        orientation = exif.get(0x0112)
                        if orientation in [3, 6, 8]:
                            image_resized = image_resized.rotate({
                                3: 180,
                                6: 270,
                                8: 90
                            }[orientation], expand=True)

                # Create a new file path for the resized image
                output_path = os.path.join(output_folder, filename)

                # Save the resized image without re-encoding to maintain quality
                image_resized.save(output_path, format=img.format)

def browse_button(entry):
    filename = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def resize_images_gui():
    def resize_images_command():
        input_folder = input_entry.get()
        output_folder = output_entry.get()
        width = int(width_entry.get())
        height = int(height_entry.get())
        resize_images(input_folder, output_folder, width, height)

    root = tk.Tk()
    root.title("Image Resizer")

    input_label = tk.Label(root, text="Input Folder:")
    input_label.grid(row=0, column=0, padx=5, pady=5)

    input_entry = tk.Entry(root, width=50)
    input_entry.grid(row=0, column=1, padx=5, pady=5)

    input_button = tk.Button(root, text="Browse", command=lambda: browse_button(input_entry))
    input_button.grid(row=0, column=2, padx=5, pady=5)

    output_label = tk.Label(root, text="Output Folder:")
    output_label.grid(row=1, column=0, padx=5, pady=5)

    output_entry = tk.Entry(root, width=50)
    output_entry.grid(row=1, column=1, padx=5, pady=5)

    output_button = tk.Button(root, text="Browse", command=lambda: browse_button(output_entry))
    output_button.grid(row=1, column=2, padx=5, pady=5)

    width_label = tk.Label(root, text="Width:")
    width_label.grid(row=2, column=0, padx=5, pady=5)

    width_entry = tk.Entry(root, width=10)
    width_entry.grid(row=2, column=1, padx=5, pady=5)

    height_label = tk.Label(root, text="Height:")
    height_label.grid(row=3, column=0, padx=5, pady=5)

    height_entry = tk.Entry(root, width=10)
    height_entry.grid(row=3, column=1, padx=5, pady=5)

    resize_button = tk.Button(root, text="Resize Images", command=resize_images_command)
    resize_button.grid(row=4, column=1, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    resize_images_gui()