import pandas as pd
from data_loader import get_solano_data, cleaned_data, clean_dataframe

#what is our employment gap, and what is it's relation to the state's employment rate
def employment_gap(employment_rate, labor_size, avg_wage, state_employment_rate):
    #as a percentage, with 96% being the benchmark, how far off are we from the benchmark employment rate
    #positive means there's a gap, negative means no gap
    gap_percentage_point = 96 - employment_rate

    #how does the percentage gap translate to actual labor force loss
    worker_gap = (gap_percentage_point / 100) * labor_size

    #how far off are we from full capacity
    consump_capacity = (employment_rate / 96)  * 100

    #calculates lost wages by multiplying worker headcount by average wages
    lost_wages = worker_gap * avg_wage

    #what is solano's employment gap in relation to california
    #positive means there's a gap, negative means no gap
    state_gap = state_employment_rate - employment_rate

    return gap_percentage_point, worker_gap, consump_capacity, lost_wages, state_gap


#calculates potential tax revenue loss by multiplying tax rate by lost wages
def lost_taxes(lost_wages, tax_rate):
    tax_loss = (tax_rate / 100) * lost_wages

    return tax_loss

if __name__ == "__main__":
    test = employment_gap(92, 150000, 19.25, 95.1)
    print(test)
    tax = lost_taxes(test[3], 8.25)
    print(tax)