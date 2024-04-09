from PIL import Image, UnidentifiedImageError
import tkinter
from tkinter.messagebox import showinfo
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import ttk
from PIL import ImageFont, ImageDraw  # text Watermark


class ImageWatermark:
    def __init__(self):
        self.img_source = ""


def add_watermark():
    if not image_work.img_source:
        messagebox.showinfo(
            title="File not found",
            message="Please choose correct file before adding watermark.",
        )
    else:
        try:
            # Open Image & Create New Text Layer
            image = Image.open(image_work.img_source).convert("RGBA")
            txt = Image.new("RGBA", image.size, (255, 255, 255, 0))

            # Creating Draw Object
            draw = ImageDraw.Draw(txt)

            # Positioning of Text
            w, h = image.size
            x, y = int(w / 2), int(h / 2)

            if x > y:
                font_size = y
            elif y > x:
                font_size = x
            else:
                font_size = x

            # Creating Text
            text = watermark_entry.get()
            font = ImageFont.truetype("arial.ttf", int(font_size / 6))

            # Applying Text
            draw.text((x, y), text, fill=(255, 255, 255, 125), font=font)

            # Combining Original Image with Text and Saving
            watermarked = Image.alpha_composite(image, txt)
            watermarked.convert("RGB").save("watermarked.jpg")
            messagebox.showinfo(
                title="Watermark added",
                message="File with watermark was saved as 'watermarked.jpg' in python script root folder."
                "\n\nWatermarked picture preview is going to be displayed in a few seconds.",
            )
            watermarked.show()
        except UnidentifiedImageError as e:
            messagebox.showinfo(
                title="Wrong file type",
                message=f"Chosen file is not an image file, please choose different file. \n\nFull error message:\n{e}",
            )
        except Exception as e:
            print(str(e))


def select_file():
    # filetypes = (("text files", "*.txt"), ("All files", "*.*"))
    filename = fd.askopenfilename(title="Open a file", initialdir="/")
    image_work.img_source = filename
    showinfo(title="Selected File", message=f"Chosen file path: {filename}")


# ------ GUI ------
image_work = ImageWatermark()

window = tkinter.Tk()
window.title("Watermark adder")
window.config(padx=50, pady=50)

watermark_label = tkinter.Label(text="Watermark text:", font=("Arial", 14, "bold"))
watermark_label.grid(column=0, row=0)
watermark_label.config(padx=20, pady=20)

watermark_entry = tkinter.Entry(width=30)
watermark_entry.insert(tkinter.END, string="Watermark text")
watermark_entry.grid(column=1, row=0)

file_label = tkinter.Label(text="Choose file:", font=("Arial", 14, "bold"))
file_label.grid(column=0, row=1)
file_label.config(padx=20, pady=20)

open_button = ttk.Button(window, text="Open a File", command=select_file)
open_button.grid(column=1, row=1, sticky="EW")

convert_button = tkinter.Button(text="Apply watermark", command=add_watermark)
convert_button.grid(column=0, row=2, columnspan=2)

window.mainloop()
