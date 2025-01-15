def calculate_retirement(current_age, retirement_age, salary, increase_percentage,
                         current_savings, percentage_year_saved, spend_in_retirement,
                         expected_return_before, expected_return_during):
    # Convert percentages to decimals
    increase_percentage /= 100
    percentage_year_saved /= 100
    expected_return_before /= 100
    expected_return_during /= 100

    # Calculate the years for each phase
    years_until_retirement = retirement_age - current_age
    retirement_years = 80 - retirement_age  # Assume lifespan is 80 years

    # Initialize values
    savings = current_savings
    annual_salary = salary
    total_savings = current_savings  # Start with the initial savings

    # Data for the graph
    years = []
    balances = []

    # Pre-Retirement simulation
    for year in range(years_until_retirement):
        years.append(current_age + year)
        balances.append(savings)

        # Calculate contribution and investment growth
        annual_contribution = annual_salary * percentage_year_saved
        investment_growth = savings * expected_return_before

        # Update total savings
        total_savings += annual_contribution + investment_growth

        # Update savings and salary
        savings = savings + investment_growth + annual_contribution
        annual_salary = annual_salary * (1 + increase_percentage)

    # Retirement simulation
    for year in range(retirement_years):
        years.append(retirement_age + year)
        balances.append(savings)

        # Calculate investment growth during retirement
        investment_growth = savings * expected_return_during
        total_savings += investment_growth  # Add investment growth during retirement

        # Update savings for withdrawals
        savings = savings + investment_growth - spend_in_retirement
        if savings < 0:
            savings = 0  # Stop at zero balance
            break

    print("*total savings ->", total_savings)

    return years, balances, total_savings
