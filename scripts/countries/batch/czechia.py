import pandas as pd
from covid_updater.iso import merge_iso
from covid_updater.tracking import update_country_tracking
from covid_updater.utils import keep_min_date


COUNTRY = "Czechia"
COUNTRY_ISO = "CZ"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani.csv"
DATA_URL_REFERENCE = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/"
REGION_RENAMING = {
    "Hlavní město Praha": "Praha, Hlavni mesto",
    "Jihomoravský kraj": "Jihomoravsky kraj",
    "Moravskoslezský kraj": "Moravskoslezsky kraj",
    "Ústecký kraj": "Ustecky kraj",
    "Středočeský kraj": "Stredocesky kraj",
    "Plzeňský kraj": "Plzensky kraj",
    "Pardubický kraj": "Pardubicky kraj",
    "Olomoucký kraj": "Olomoucky kraj",
    "Zlínský kraj": "Zlinsky kraj",
    "Královéhradecký kraj": "Kralovehradecky kraj",
    "Kraj Vysočina": "Kraj Vysocina",
    "Karlovarský kraj": "Karlovarsky kraj",
    "Jihočeský kraj": "Jihocesky kraj",
    "Liberecký kraj": "Liberecky kraj"
}


def main():
    # Load data
    df = pd.read_csv(DATA_URL)

    # Check 1
    cols = ["datum", "vakcina", "kraj_nuts_kod", "kraj_nazev", "vekova_skupina", "prvnich_davek", "druhych_davek", "celkem_davek"]
    if not all([col in df.columns for col in cols]):
        raise Exception("API changed")

    # Column renaming
    df = df.rename(columns={
        "datum": "date",
        "kraj_nazev": "region",
        "prvnich_davek": "people_vaccinated",
        "druhych_davek": "people_fully_vaccinated",
        "celkem_davek": "total_vaccinations"
    })

    # Add counts per day
    df = df.groupby(by=["date", "region"]).agg(
        people_vaccinated=("people_vaccinated", sum),
        people_fully_vaccinated=("people_fully_vaccinated", sum),
        total_vaccinations=("total_vaccinations", sum)
    ).reset_index()

    # Check 2
    if not (df["total_vaccinations"] == df["people_vaccinated"] + df["people_fully_vaccinated"]).all():
        raise Exception("Error in columns. dose_1 + dose_2 != total_doses")

    # Rename regions
    df.loc[:, "region"] = df.loc[:, "region"].replace(REGION_RENAMING)
    df.loc[:, "location"] = COUNTRY

    # ISO
    df = merge_iso(df, COUNTRY_ISO)

    # Compute cumsums
    df = df.sort_values(by="date")
    df.loc[:, "total_vaccinations"] = df.groupby("region")["total_vaccinations"].cumsum().values
    df.loc[:, "people_vaccinated"] = df.groupby("region")["people_vaccinated"].cumsum().values
    df.loc[:, "people_fully_vaccinated"] = df.groupby("region")["people_fully_vaccinated"].cumsum().values

    # Avoid repeating reports
    df = keep_min_date(df)

    # Export
    df = df[["location", "region", "date", "location_iso", "region_iso", 
             "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv(OUTPUT_FILE, index=False)

    # Tracking
    update_country_tracking(
        country=COUNTRY,
        url=DATA_URL_REFERENCE,
        last_update=df["date"].max()
    )

if __name__ == "__main__":
    main()