import pandas as pd

multiplier_data = [
    {"sector_name": "Agriculture, forestry, fishing, hunting", "naics_code": "11", "supplier": 93.6, "induced": 134.8, "total_indirect": 228.5, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Mining", "naics_code": "21", "supplier": 224.0, "induced": 166.0, "total_indirect": 390.0, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Utilities", "naics_code": "22", "supplier": 515.4, "induced": 442.2, "total_indirect": 957.7, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Construction", "naics_code": "23", "supplier": 88.0, "induced": 138.1, "total_indirect": 226.1, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Durable manufacturing", "naics_code": "33", "supplier": 289.1, "induced": 454.9, "total_indirect": 744.1, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Nondurable manufacturing", "naics_code": "31", "supplier": 184.8, "induced": 329.5, "total_indirect": 514.3, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Wholesale trade", "naics_code": "42", "supplier": 107.3, "induced": 128.0, "total_indirect": 235.3, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Retail trade", "naics_code": "44", "supplier": 46.7, "induced": 75.4, "total_indirect": 122.1, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Transportation and warehousing", "naics_code": "48", "supplier": 112.8, "induced": 163.3, "total_indirect": 276.0, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Truck transportation", "naics_code": "484", "supplier": 108.2, "induced": 83.1, "total_indirect": 191.3, "source": "EPI 2019 (national avg, detailed)"},
    {"sector_name": "Warehousing and storage", "naics_code": "493", "supplier": 53.2, "induced": 58.5, "total_indirect": 111.7, "source": "EPI 2019 (national avg, detailed)"},
    {"sector_name": "Couriers and messengers", "naics_code": "492", "supplier": 84.5, "induced": 72.6, "total_indirect": 157.1, "source": "EPI 2019 (national avg, detailed)"},
    {"sector_name": "Information", "naics_code": "51", "supplier": 252.0, "induced": 321.1, "total_indirect": 573.1, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Finance and insurance", "naics_code": "52", "supplier": 149.7, "induced": 214.7, "total_indirect": 364.4, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Real estate and rental leasing", "naics_code": "53", "supplier": 396.6, "induced": 483.1, "total_indirect": 879.7, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Professional, scientific, technical services", "naics_code": "54", "supplier": 142.1, "induced": 276.2, "total_indirect": 418.3, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Management of companies", "naics_code": "55", "supplier": 144.4, "induced": 255.4, "total_indirect": 399.9, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Administrative, support, waste management", "naics_code": "56", "supplier": 45.5, "induced": 89.1, "total_indirect": 134.5, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Educational services", "naics_code": "61", "supplier": 63.8, "induced": 129.9, "total_indirect": 193.7, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Health care and social assistance", "naics_code": "62", "supplier": 69.4, "induced": 136.2, "total_indirect": 205.6, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Arts, entertainment, recreation", "naics_code": "71", "supplier": 123.3, "induced": 255.2, "total_indirect": 378.5, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Accommodation and food services", "naics_code": "72", "supplier": 53.8, "induced": 107.4, "total_indirect": 161.2, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Other services", "naics_code": "81", "supplier": 70.7, "induced": 139.6, "total_indirect": 210.3, "source": "EPI 2019 (national avg)"},
    {"sector_name": "Government / public administration", "naics_code": "92", "supplier": None, "induced": None, "total_indirect": 189.0, "source": "Texas Comptroller (state avg, approximation)"},
]

#converts the list of dictionaries into a pandas df
multiplier_df = pd.DataFrame(multiplier_data)

#calculates multiplier effect of adding any amount of direct job into an industry
#this would be the floor
multiplier_df["type1_mult"] = 1 + (multiplier_df["supplier"] / 100)

#calculates what type 1 does but adds any additional jobs induced that may not be directly related to the industry, but where employees spend their money
#this would be the ceiling
multiplier_df["type2_mult"] = 1 + (multiplier_df["total_indirect"] / 100)

#converts to csv file
multiplier_df.to_csv("data/multipliers.csv", index=False)