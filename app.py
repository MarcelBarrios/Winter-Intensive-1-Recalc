from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from models.calculation import calculate_retirement
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Database setup
client = MongoClient("mongodb://localhost:27017/")
db = client.retirement_app
calculations_collection = db.calculations


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Retrieve form data
            age = int(request.form["age"])
            retirement_age = int(request.form["retirement_age"])
            salary = float(request.form["salary"])
            increase_percentage = float(request.form["increase_percentage"])
            retirement_so_far = float(request.form["retirement_so_far"])
            percentage_year_saved = float(
                request.form["percentage_year_saved"])
            spend_in_retirement = float(request.form["spend_in_retirement"])
            expected_return_before = float(
                request.form["expected_return_before"])
            expected_return_during = float(
                request.form["expected_return_during"])

            # Calculate years until retirement
            years_until_retirement = retirement_age - age
            if years_until_retirement <= 0:
                flash("Retirement age must be greater than your current age.", "error")
                return redirect(url_for("index"))

            # Call the retirement calculation function
            future_value = calculate_retirement(
                salary,
                percentage_year_saved,
                retirement_so_far,
                years_until_retirement,
                increase_percentage,
                expected_return_before,
                expected_return_during,
                spend_in_retirement
            )

            # Save the calculation to the database
            calculations_collection.insert_one({
                "age": age,
                "retirement_age": retirement_age,
                "salary": salary,
                "increase_percentage": increase_percentage,
                "retirement_so_far": retirement_so_far,
                "percentage_year_saved": percentage_year_saved,
                "spend_in_retirement": spend_in_retirement,
                "expected_return_before": expected_return_before,
                "expected_return_during": expected_return_during,
                "future_value": future_value
            })

            # Flash success message
            flash(f"Calculation saved! Future Value: ${
                  future_value:,.2f}", "success")
        except ValueError:
            flash(
                "Invalid input. Please make sure all fields are filled correctly.", "error")

        return redirect(url_for("index"))

    # Retrieve saved calculations for display
    saved_calculations = list(calculations_collection.find())
    return render_template("index.html", saved_calculations=saved_calculations)


if __name__ == "__main__":
    app.run(debug=True)
