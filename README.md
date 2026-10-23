# EconScope V1

A dashboard showing how employment changes in one industry ripples through Solano County, CA.

**Live app:** https://economicscenarioplanner.streamlit.app/

## What it does
- **Current Employment Status:** Solano County unemployment, the gap to a 96% employment benchmark, workers needed to close it, consumption capacity, a comparison with the state of California, and estimated annual lost wages.
- **Investment Scenario Analysis:** pick a sector and what changes in direct jobs to see total jobs, indirect jobs, and wage impact using Type I or Type II multipliers.
- **Where To Invest:** ranks 24 sectors by multiplier, per direct job.

## How to read it
The multiplier shows a ripple effect of additional jobs added for each direct job input, not a return on investment analysis.

This is to help decision makers get a fuller picture by comparing how employment changes ripple through the local economy


## Method
- Type I = 1 + supplier / 100; Type II = 1 + total indirect / 100.
- Employment gap uses an assumed 96% benchmark.

## Limitations
- Multipliers are 2019 national averages, not Solano-specific.
- Growth timelines are illustrative estimates.
- The 96% benchmark is an assumption, and one blended wage is used for all sectors.
- Utilities ranks highest because the measure is ripple per direct job, not return per dollar or local presence.
- Free-tier hosting: the app may sleep when idle, so open the link before a demo.


## Data Sources
- **Employment data:** U.S. Bureau of Labor Statistics LAUS series for Solano County and California, 2020-2026, not seasonally adjusted, model-based and subject to revision.
- **Multipliers:** Economic Policy Institute (Jan 2019), "Updated employment multipliers for the U.S. economy," national averages per 100 direct jobs.
- **Government sector:** Texas Comptroller state average (approximate), Type II only.

## Tech Stack
Python | Pandas | Requests | python-dotenv | Streamlit | Plotly

## Roadmap
V2: A business-level cost model for Solano County using local data

## Author
- **Frandu Taylor**