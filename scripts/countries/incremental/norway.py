import json
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from covid_updater.iso import merge_iso
from covid_updater.tracking import update_country_tracking
from covid_updater.utils import keep_min_date


COUNTRY = "Norway"
COUNTRY_ISO = "NO"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://www.fhi.no/sv/vaksine/koronavaksinasjonsprogrammet/koronavaksinasjonsstatistikk/"
DATA_URL_REFERENCE = DATA_URL
REGION_RENAMING = {
    "agder": "Agder",
    "innlandet": "Innlandet",
    "møre og romsdal": "More og Romsdal",
    "nordland": "Nordland",
    "oslo": "Oslo",
    "rogaland": "Rogaland",
    "troms og finnmark": "Troms og Finnmark",
    "trøndelag": "Trondelag",
    "vestfold og telemark": "Vestfold og Telemark",
    "vestland": "Vestland",
    "viken": "Viken" 
}


def load_driver(url):
    op = Options()
    op.add_argument("--headless")
    driver = webdriver.Chrome(options=op)
    driver.get(url)
    return driver


def load_date(driver):
    elem = driver.find_element_by_class_name("fhi-date")
    date = elem.find_elements_by_tag_name("time")[-1].get_attribute("datetime")
    return date


def main():
    # Load current file
    df_source = pd.read_csv(OUTPUT_FILE)

    #  Get date
    driver = load_driver(DATA_URL)
    try:
        date = load_date(driver)
    except:
        raise Exception("Date not found!")

    # Load dose 1 data
    url = "https://www.fhi.no/api/chartdata/api/99112"
    dix = json.loads(requests.get(url).content)
    df_dose1 = pd.DataFrame(dix, columns=["region", "people_vaccinated"])
    # Load dose 2 data
    url = "https://www.fhi.no/api/chartdata/api/99111"
    dix = json.loads(requests.get(url).content)
    df_dose2 = pd.DataFrame(dix, columns=["region", "people_fully_vaccinated"])
    # Remove row
    df_dose1 = df_dose1.loc[~(df_dose2["region"] == "Fylke")]
    df_dose2 = df_dose2.loc[~(df_dose2["region"] == "Fylke")]
    # Merge
    df = df_dose1.merge(df_dose2, on="region", how="left")

    # Process region column
    df.loc[:, "region"] = df.loc[:, "region"].replace(REGION_RENAMING)

    # Add columns
    df.loc[:, "date"] = date
    df.loc[:, "location"] = COUNTRY
    df.loc[:, "total_vaccinations"] = df.loc[:, "people_fully_vaccinated"] + df.loc[:, "people_vaccinated"]

    # Add ISO codes
    df = merge_iso(df, country_iso=COUNTRY_ISO)

    # Concat
    df_source = df_source.loc[~(df_source.loc[:, "date"] == date)]
    df = pd.concat([df, df_source])

    # Export 
    df = df[["location", "region", "date", "location_iso", "region_iso",
             "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]
    df = keep_min_date(df)
    cols = ["total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]
    df[cols] = df[cols].astype("Int64").fillna(pd.NA)
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