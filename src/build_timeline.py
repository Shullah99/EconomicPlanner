import pandas as pd

timeline_data = [
    {"sector_name": "Agriculture, forestry, fishing, hunting", "min_years": 0.5, "max_years": 1, "note": "seasonal, annual cycles"},
    {"sector_name": "Mining", "min_years": 2, "max_years": 4, "note": "capital-intensive ramp-up"},
    {"sector_name": "Utilities", "min_years": 2, "max_years": 4, "note": "infrastructure-dependent"},
    {"sector_name": "Construction", "min_years": 1, "max_years": 2, "note": "project-based"},
    {"sector_name": "Durable manufacturing", "min_years": 2, "max_years": 4, "note": "facility/equipment ramp-up"},
    {"sector_name": "Nondurable manufacturing", "min_years": 2, "max_years": 4, "note": "facility/equipment ramp-up"},
    {"sector_name": "Wholesale trade", "min_years": 1, "max_years": 2, "note": "supply chain dependent"},
    {"sector_name": "Retail trade", "min_years": 0.5, "max_years": 1, "note": "fast hiring ramp"},
    {"sector_name": "Transportation and warehousing", "min_years": 1, "max_years": 2, "note": "fleet/facility dependent"},
    {"sector_name": "Truck transportation", "min_years": 0.5, "max_years": 1, "note": "fast hiring ramp"},
    {"sector_name": "Warehousing and storage", "min_years": 0.5, "max_years": 1, "note": "fast hiring ramp"},
    {"sector_name": "Couriers and messengers", "min_years": 0.5, "max_years": 1, "note": "fast hiring ramp"},
    {"sector_name": "Information", "min_years": 1, "max_years": 3, "note": "tech/talent dependent"},
    {"sector_name": "Finance and insurance", "min_years": 1, "max_years": 2, "note": "licensing/training dependent"},
    {"sector_name": "Real estate and rental leasing", "min_years": 1, "max_years": 3, "note": "market cycle dependent"},
    {"sector_name": "Professional, scientific, technical services", "min_years": 1, "max_years": 2, "note": "talent dependent"},
    {"sector_name": "Management of companies", "min_years": 1, "max_years": 2, "note": "org growth dependent"},
    {"sector_name": "Administrative, support, waste management", "min_years": 0.5, "max_years": 1, "note": "fast hiring ramp"},
    {"sector_name": "Educational services", "min_years": 1, "max_years": 2, "note": "academic calendar dependent"},
    {"sector_name": "Health care and social assistance", "min_years": 1, "max_years": 2, "note": "licensing/training dependent"},
    {"sector_name": "Arts, entertainment, recreation", "min_years": 0.5, "max_years": 1, "note": "fast hiring ramp"},
    {"sector_name": "Accommodation and food services", "min_years": 0.5, "max_years": 1, "note": "fast hiring ramp"},
    {"sector_name": "Other services", "min_years": 0.5, "max_years": 1, "note": "fast hiring ramp"},
    {"sector_name": "Government / public administration", "min_years": 2, "max_years": 3, "note": "budget cycle dependent"},
]

timeline_df = pd.DataFrame(timeline_data)
timeline_df.to_csv("data/growth_timeline.csv", index=False)