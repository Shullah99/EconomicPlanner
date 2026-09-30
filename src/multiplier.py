import pandas as pd
from data_loader import get_solano_data, cleaned_data, clean_dataframe, load_multipliers

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

def mult_effect(sector_name, direct_job, multiplier_type, avg_wage, tax_rate):
    multiplier_df = load_multipliers()

    #strips the load_multipliers csv down to the specific sector name inputted in the function's parameters
    result = multiplier_df[multiplier_df["sector_name"] == sector_name]

    #determines multiplier type
    if multiplier_type == "type1":
        selected_type = result["type1_mult"].iloc[0]
    else:
        selected_type = result["type2_mult"].iloc[0]


    #total jobs added from multiplier type and direct added jobs
    total_jobs = direct_job * selected_type
    
    #only for ripple out jobs
    indirect_jobs = total_jobs - direct_job

    #the wage impacts of direct, indirect, and the total jobs
    direct_wage_impact = direct_job * avg_wage
    indirect_wage_impact = indirect_jobs * avg_wage
    total_wage_impact = direct_wage_impact + indirect_wage_impact


    #the additional tax revenue recieved from the additional wages
    tax_revenue = (tax_rate / 100) * total_wage_impact

    return total_jobs, indirect_jobs, direct_wage_impact, indirect_wage_impact, total_wage_impact, tax_revenue

if __name__ == "__main__":
    test = employment_gap(92, 150000, 19.25, 95.1)
    print(test)
    tax = lost_taxes(test[3], 8.25)
    print(tax)
    mult = mult_effect("Mining", 1000, "type2", 62000, 8.25)
    print(mult)