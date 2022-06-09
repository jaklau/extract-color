from flask import Flask, render_template
from extract_colors import ExtractColors
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import FileField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

import os

file_formats = ["gif", "pgm", "ppm", "png", "jpg", "jpeg", "bmp"]


class UploadImage(FlaskForm):
    name = FileField('Upload your file', validators=[
        FileRequired(message="file is not selected"),
        FileAllowed(file_formats, message="wrong format")])
    number = IntegerField("Number of colors:", default=10, validators=[
        DataRequired(message="number is required")])
    submit = SubmitField("Run")


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'TopSecretKey'


@app.route("/", methods=["GET", "POST"])
def home():
    data = []
    filename = ""
    upload_img = UploadImage()
    if upload_img.validate_on_submit():
        f = upload_img.name.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.static_folder, "img", filename))
        img = ExtractColors(f"static/img/{filename}")

        data = img.extract(upload_img.number.data)
        # os.remove(os.path.join(app.static_folder, "img", filename))
        return render_template("index.html", form=upload_img, image=filename, data=data)
    return render_template("index.html", form=upload_img, image=filename, data=data)


if __name__ == "__main__":
    app.run(debug=True)
