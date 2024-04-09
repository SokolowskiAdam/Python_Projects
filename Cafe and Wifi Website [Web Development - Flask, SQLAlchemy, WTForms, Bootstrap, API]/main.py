from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, URLField, BooleanField
from wtforms.validators import DataRequired, URL
import random
import os


# Flask config
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_KEY")
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI")
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    # Create dict from table
    def to_dict(self):
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Dict key: name of the column and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


with app.app_context():
    db.create_all()


# Flask form - add cafe
class CafeForm(FlaskForm):
    cafe = StringField("Cafe name", validators=[DataRequired()])
    map_url = URLField(
        label="Cafe Location in Google Maps (URL)", validators=[DataRequired(), URL()]
    )
    img_url = URLField(label="Cafe Image (URL)", validators=[DataRequired(), URL()])
    location = StringField("Cafe location", validators=[DataRequired()])
    has_sockets = BooleanField("Electric sockets available")
    has_toilet = BooleanField("Toilet available")
    has_wifi = BooleanField("Wifi available")
    can_take_calls = BooleanField("Taking calls possible")
    seats = SelectField(
        label="Number of seats available",
        choices=["0-10", "10-20", "20-30", "30-40", "40-50", "50+"],
        validators=[DataRequired()],
    )
    coffe_price = StringField("Coffe price (ex. £2.40)", validators=[DataRequired()])
    submit = SubmitField("Submit")


# -------- Flask Routes --------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("Success")
        new_cafe = Cafe(
            name=form.cafe.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffe_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("cafes"))

    return render_template("add.html", form=form)


@app.route("/cafes")
def cafes():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes_db = result.scalars().all()
    column_names = [
        "Cafe Name",
        "Google Maps",
        "Image",
        "Location",
        "Sockets",
        "Toilet",
        "Wifi",
        "Can take calls",
        "Seats",
        "Coffee price",
    ]

    return render_template("cafes.html", cafes=all_cafes_db, columns=column_names)


@app.route("/api")
def api_documentation():
    return render_template("api.html")


# -------- API Routes --------
@app.route("/api/random")  # GET statement is allowed by default
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes_db = result.scalars().all()
    random_cafe = random.choice(all_cafes_db)
    # return json
    random_cafe_json = jsonify(cafe=random_cafe.to_dict())
    return random_cafe_json


@app.route("/api/all")
def get_all_cafes():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes_db = result.scalars().all()
    all_cafes_list = [cafe.to_dict() for cafe in all_cafes_db]
    all_cafes_json = jsonify(cafes=all_cafes_list)

    return all_cafes_json


@app.route("/api/search")
def find_cafe():
    query_location = request.args.get("loc")
    query = Cafe.query.filter(Cafe.name.ilike(f"%{query_location}%"))
    result = db.session.execute(query)
    found_cafes_db = result.scalars().all()

    if found_cafes_db:
        found_cafes_list = [cafe.to_dict() for cafe in found_cafes_db]
        found_cafes_json = jsonify(cafes=found_cafes_list)
        return found_cafes_json
    else:
        return (
            jsonify(
                error={"Not Found": "Sorry, we don't have a cafe at that location."}
            ),
            404,
        )


# Request type: Post ->  Body ->  x-www-form-urlencoded
@app.route("/api/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


@app.route("/update-price/<cafe_id>", methods=["GET", "PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.get_or_404(Cafe, cafe_id)

    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
    else:
        return (
            jsonify(
                error={
                    "Not Found": "Sorry a cafe with that id was not found in the database."
                }
            ),
            404,
        )


@app.route("/report_closed/<int:cafe_id>", methods=["GET", "DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    cafe_to_del = db.get_or_404(Cafe, cafe_id)

    if cafe_to_del:
        if api_key == os.environ.get("API_KEY"):
            db.session.delete(cafe_to_del)
            db.session.commit()

            return (
                jsonify(
                    response={"success": "Successfully deleted Cafe from database."}
                ),
                200,
            )
        else:
            return (
                jsonify(
                    response={
                        "error": "You are not authorized to delete Cafe from database. Wrong API KEY."
                    }
                ),
                403,
            )
    else:
        return (
            jsonify(
                error={
                    "Not Found": "Sorry a Cafe with that id was not found in the database."
                }
            ),
            404,
        )


if __name__ == "__main__":
    app.run(debug=True)
