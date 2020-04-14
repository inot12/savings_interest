#! /home/toni/.pyenv/shims/python3
'''
Created on Apr 13, 2020

@author:toni
'''

import datetime as dt


def calculate_interest_rates(start,end,yearly_rate):
    """
    Calculate interest rate for each month and return total rate.
    
    start - tuple of integers; start_date, (y, m, d)
    end - tuple of integers; end_date, (y, m, d)
    yearly_rate - float; yearly interest rate in percent
    """
    
    years_months = saving_period_months(start,end)
    print('Days in a month: {}'.format(years_months))
    rates = []
    
    for year in years_months.keys():
        if not is_leap_year(year):
            for days in years_months[year]:
                rates.append(interest_rate(yearly_rate, days))
        else:
            for days in years_months[year]:
                rates.append(leap_interest_rate(yearly_rate, days))
    
    print('Rates (in percent) for each month: {}'.format(rates)) 
             
    return total_interest_rate(rates)
    

def interest_rate(p,d):
    """
    The formula for interest rate.
    
    p - real; interest rate in percent, for the whole year
    d - integer; number of days in a month
    """
    return 100 * ((1+p/100)**(d/365) - 1)
    
    
def leap_interest_rate(p,d):
    """
    The formula for interest rate, if a year is a leap year.
    
    p - real; interest rate in percent, for the whole year
    d - integer; number of days in a month
    """
    return 100 * ((1+p/100)**(d/366) - 1)


def total_interest_rate(monthly_interest):
    """
    Calculates the total interest rate by summing rates for each month.
    
    monthly_interest - list of floats
    
    Added the rounding of sum because if in one of the arguments 
    there's only a 5 without any following numbers, because of 
    computer arithmetic, the sum is returned as a float with more than 
    two decimals.
    Example:
    (You will see that instead of 3.98 you get 3.9800000000000004)
    
    a = 1.3
    b = 1.275
    c = 1.413
    args = [a,b,c]
    print(sum([round(rate,2) for rate in args])) 
    """
    return round(sum([round(rate,2) for rate in monthly_interest]),2)


def saving_period_months(s_d,e_d):
    """
    Creates a dictionary of years as keys where values are lists of 
    days of months for interest calculation.
    
    s_d - tuple of integers; start_date, (y, m, d)
    e_d - tuple of integers; end_date, (y, m, d)
    """
    
    start = dt.date(s_d[0],s_d[1],s_d[2])
    end = dt.date(e_d[0],e_d[1],e_d[2])
    
    year_and_months = {}
    temp_start = start
    current_year = temp_start.year
    
    while temp_start < end:
        
        if temp_start.month % 12 != 0:
            current_month = temp_start.month + 1
        else:
            current_month = 1
            current_year += 1
            
        intermediate = dt.date(current_year,current_month,1)
        days_in_month = (intermediate-temp_start).days

        temp_year = current_year
        if current_month == 1:
            temp_year = current_year - 1
            
        if temp_year in year_and_months:
            year_and_months[temp_year].append(days_in_month)
        else:
            year_and_months[temp_year] = [days_in_month]

        temp_start = intermediate
    
    if current_month == 1:
        current_month = 12
        current_year -= 1
    else:
        current_month -= 1
    
    current_date = dt.date(current_year,current_month,1)
    year_and_months[temp_year].pop(-1)
    year_and_months[temp_year].append((end-current_date).days)

    return year_and_months
    
    
def saving_period(s_d,e_d):
    """
    Calculates the number of days in the saving period.
    
    s_d - tuple of integers; start_date, (y, m, d)
    e_d - tuple of integers; end_date, (y, m, d)
    """
    
    start = dt.date(s_d[0],s_d[1],s_d[2])
    end = dt.date(e_d[0],e_d[1],e_d[2])
    return (end - start).days

    
def is_leap_year(year):
    """Determine whether a year is a leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def total_interest(C,p):
    """Calculate the total interest for amount C and rate p."""
    return C * p/100


def main():
    interest = calculate_interest_rates((2014,2,15), (2016,5,18), 2.85)
    print('Total interest rate: {} %'.format(interest))
    
    total_days = saving_period((2014,2,15), (2016,5,18))
    print('Total number of days of saving period: {}'.format(total_days))
    
    C = 10000
    K = total_interest(C, interest)
    print('Total interest for the sum of {} in a period of {} days: {} Ccy.'
          .format(C,total_days,K))


if __name__ == '__main__':
    main()