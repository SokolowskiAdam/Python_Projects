from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__)

upload_folder = os.path.join("static", "uploads")
app.config["UPLOAD"] = upload_folder


def rgb_to_hex(rgb):
    r, g, b = rgb
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Get and save uploaded image
        file = request.files["img"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD"], filename))
        img = os.path.join(app.config["UPLOAD"], filename)

        # Check colors
        img_pil = Image.open(img)
        max_colors = 1000000000  # It needs to be as high as possible, if too low it returns None - PIL library

        list_of_colors = img_pil.getcolors(max_colors)
        colors_dict = {color[0]: color[1] for color in list_of_colors}

        # 10 most common colors
        color_occurrences = list(colors_dict.keys())
        color_occurrences.sort(reverse=True)
        top_10_col_occurrences = color_occurrences[0:10]

        top_10_col_list_rgb = [colors_dict[color] for color in top_10_col_occurrences]
        top_10_col_list_hex = [rgb_to_hex(rgb) for rgb in top_10_col_list_rgb]
        top_10_col_dict = dict(zip(top_10_col_list_hex, top_10_col_list_rgb))

        return render_template("index.html", img=img, top_10_col_dict=top_10_col_dict)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
