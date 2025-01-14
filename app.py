from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from models.calculation import calculate_retirement

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database setup
client = MongoClient("mongodb://localhost:27017/")
db = client.retirement_app
calculations_collection = db.calculations


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Retrieve form data
        salary = float(request.form["salary"])
        investment_percentage = float(request.form["investment_percentage"])
        current_savings = float(request.form["current_savings"])
        years_until_retirement = int(request.form["years_until_retirement"])
        profession = request.form.get("profession", "Unknown")

        # Calculate future value
        future_value = calculate_retirement(
            salary, investment_percentage, current_savings, years_until_retirement
        )

        # Save to database
        calculations_collection.insert_one({
            "profession": profession,
            "salary": salary,
            "investment_percentage": investment_percentage,
            "current_savings": current_savings,
            "years_until_retirement": years_until_retirement,
            "future_value": future_value
        })

        # Flash a success message
        flash(f"Calculation saved! Future Value: ${future_value:,.2f}")
        return redirect(url_for("index"))

    # Retrieve saved calculations for display
    saved_calculations = list(calculations_collection.find())
    return render_template("index.html", saved_calculations=saved_calculations)


if __name__ == "__main__":
    app.run(debug=True)
