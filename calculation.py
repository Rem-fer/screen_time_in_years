def yearly_screen_time(avg_screentime):
    """
    Function calcultating yearly screentime in days from avg hours of use
    """
    days_per_year = int(avg_screentime * 365 / 24)
    months, days = divmod(days_per_year, 30)
    
    return months, days

def life_expectancy(gender,age):
    """
    Function calculates life expectancy based on current age and gender
    """
    if gender == 'male':
        return max(0, 75 - age) #In case the person is over expectancy, it returns 0
    else:
        return max(0, 82 - age)

def lifetime_screentime(avg_screentime, life_exp):
    """
    Function calculating lifetime screentime based on life expectancy and avg_screentime
    """
    life_hours = avg_screentime * 365 * life_exp
    life_days = round(life_hours / 24)  # calculating the amount of time on screen in days
    years, d = divmod(life_days, 365)  # amount of screentime in years and days for a lifetime
    months, days = divmod(d, 30)  # calculating the number of months from the

    return years, months, days
