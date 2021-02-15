# Subnational COVID-19 vaccination data 
### [**API**](https://sociepy.org/covid19-vaccination-subnational/data/api/v1) | [**Download data**](data/vaccinations.csv) | [**GitHub**](https://github.com/sociepy/covid19-vaccination-subnational)

![refresh](https://github.com/sociepy/covid19-vaccination-subnational/workflows/refresh/badge.svg?branch=main)
![GitHub last commit](https://img.shields.io/github/last-commit/sociepy/covid19-vaccination-subnational)
[![Website link!](https://img.shields.io/badge/website-link-1abc9c.svg)](https://sociepy.org/covid19-vaccination-subnational/)
[![API link!](https://img.shields.io/badge/API-link-1abc9c.svg)](https://sociepy.org/covid19-vaccination-subnational/data/api/v1)



COVID-19 vaccination data at subnational level. To ensure its officiality, the source data is carefully verified.

All country data can be found in a [single
csv file](https://raw.githubusercontent.com/sociepy/covid19-vaccination-subnational/main/data/vaccinations.csv). If you
are interested in indiviual country data, you may want to check [countries](data/countries) folder.

Additionally, we provide a static API endpoint, which contains the data per country as JSONs. For more details check [here](https://sociepy.org/covid19-vaccination-subnational/data/api/v1).


### Thanks to
This project is inspired by wonderful project [owid/covid-19-data](https://github.com/owid/covid-19-data), adopting
some of its structure, and is open to integration if deemed appropriate.
In addition, thanks to all of the people involved in the different [source data](#data-sources) initiatives. 

## Content
* [Data sources](#data-sources)
* [Data format](#data-format)
* [JSON Endpoint API](data/api/v1/README.md)
* [Contribute](#contribute)
* [Documentation](docs/CODE.md) (WIP 🚧)
* [License](#license)


## Data sources
This project wouldn't be possible without the great resources available online.

{data_sources}

## Data format
The data pretends to resemble the API proposed by [owid/covid-19-data](https://github.com/owid/covid-19-data). Find
below the field description, mainly provided by [OWID](https://github.com/owid/covid-19-data/blob/master/public/data/vaccinations/README.md).

| Field 	| Description 	|
|-	|-	|
| `location` 	| Name of the country. 	|
| `region` 	| Name of the subnational region of the country. 	|
| `date` 	| Date of the observation. 	|
| `location_iso` 	| ISO 3166-1 country codes (XX) 	|
| `region_iso` 	| ISO 3166-2 region codes (XX-YY or XX-YYY). 	|
| `total_vaccinations` 	| Total number of doses administered. This is counted as a single dose, and may not equal the total number of people vaccinated, depending on the specific dose regime (e.g. people receive multiple doses). If a person receives one dose of the vaccine, this metric goes up by 1. If they receive a second dose, it goes up by 1 again. 	|
| `people_vaccinated` 	| Total number of people who received at least one vaccine dose. If a person receives the first dose of a 2-dose vaccine, this metric goes up by 1. If they receive the second dose, the metric stays the same. 	|
|  `people_fully_vaccinated`    | Total number of people who received all doses prescribed by the vaccination protocol. If a person receives the first dose of a 2-dose vaccine, this metric stays the same. If they receive the second dose, the metric goes up by 1.  |
| `total_vaccinations_per_100` 	| `total_vaccinations` per 100 habitants. |
| `people_vaccinated_per_100` 	| `people_vaccinated` per 100 habitants.	|
|  `people_fully_vaccinated_per_100` 	| `people_fully_vaccinated` per 100 habitants. 	|

Note: for `people_vaccinated` and `people_fully_vaccinated` we are dependent on the necessary data being made available,
so we may not be able to make these metrics available for some countries.

## Contribute
The updates are done using [update_all.sh](scripts/update_all.sh) script. For more details on the scripts being used,
check [here](scripts/README.md).


### Set up environment
Install the package:

```
$ pip install -e .
```

### Execute update

```
$ bash scripts/update_all.sh
```

### Add new countries
If you know of any reference publishing vaccination regional data for other countries, your contribution is very much
appreciated! It is extremely helpfull if you could [report this in the issues](https://github.com/sociepy/covid19-vaccination-subnational/issues/new). Also, if you feel like automating it by
yourself (that'd be awesome!), please fork this repository and issue a pull request
with your changes.

The country scraping logic lives within the package module, specifically in
[covid_updater.scraping](src/covid_updater/scraping/). More details to be added [here](docs/CODE.md) soon.

### Bugs
We do our best to ensure that the data is reliable. However, as the project grows and source website change their
format, some bugs might appear. If you detect any, please [report this in the issues section](https://github.com/sociepy/covid19-vaccination-subnational/issues/new).

## Documentation
See [documentation](docs/CODE.md) (WIP 🚧)

## License
See [LICENSE](LICENSE).

> This site or product includes IP2Location™ ISO 3166-2 Subdivision Code which available from
> https://www.ip2location.com.
