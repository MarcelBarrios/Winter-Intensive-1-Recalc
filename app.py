from flask import Flask, render_template, request, redirect, url_for, flash, session
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
    years = session.pop('years', [])
    balances = session.pop('balances', [])
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

            # Validation
            if age < 0 or retirement_age < 0:
                flash("Age and retirement age must be positive numbers.", "error")
                return redirect(url_for("index"))
            if age >= 80:
                flash("Age must be less than 80.", "error")
                return redirect(url_for("index"))
            if retirement_age <= age:
                flash("Retirement age must be greater than current age.", "error")
                return redirect(url_for("index"))

            # Call the retirement calculation function
            years, balances = calculate_retirement(
                age, retirement_age, salary, increase_percentage,
                retirement_so_far, percentage_year_saved, spend_in_retirement,
                expected_return_before, expected_return_during
            )

            # Save the calculation to the database
            try:
                calculations_collection.insert_one({
                    "current_age": age,
                    "retirement_age": retirement_age,
                    "salary": salary,
                    "increase_percentage": increase_percentage,
                    "current_savings": retirement_so_far,
                    "percentage_year_saved": percentage_year_saved,
                    "spend_in_retirement": spend_in_retirement,
                    "expected_return_before": expected_return_before,
                    "expected_return_during": expected_return_during,
                    "years": years,
                    "balances": balances
                })

                session['years'] = years
                session['balances'] = balances

            except Exception as e:
                flash("Failed to save calculation to the database.", "error")
                print(f"Database error: {e}")
                return redirect(url_for("index"))

            # Flash success message
            flash(f"Calculation saved! Final Balance: ${
                  balances[-1]:,.2f}", "success")
        except ValueError:
            flash(
                "Invalid input. Please make sure all fields are filled correctly.", "error")
        except Exception as e:
            flash("An unexpected error occurred.", "error")
            print(f"Error: {e}")

        return redirect(url_for("index"))

    print("years -> ", years)
    print("balances -> ", balances)
    # Retrieve saved calculations for display
    saved_calculations = list(calculations_collection.find())
    return render_template("index.html",
                           saved_calculations=saved_calculations,
                           years=years if years else [],
                           balances=balances if balances else [])


if __name__ == "__main__":
    app.run(debug=True)
