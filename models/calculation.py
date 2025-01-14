def calculate_retirement(salary, investment_percentage):
    """
    Calculate the retirement savings projection.

    :param salary: Annual salary (float)
    :param investment_percentage: Percentage of salary to invest annually (float)
    :return: Projected retirement savings after 35 years (float)
    """
    years = 35
    annual_return_rate = 0.07
    investment = salary * (investment_percentage / 100)
    total_savings = 0

    for _ in range(years):
        total_savings = (total_savings + investment) * (1 + annual_return_rate)

    return round(total_savings, 2)
