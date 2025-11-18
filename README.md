# Windy Pops
A notification tool for wind and watersports conditions


## Usage:
Locally:

Using `uv`:
```bash
uv sync
source .venv/bin/activate
```

```bash
uv run python -m windy_pops.main
```





```bash
PYTHONPATH=/home/std3ldn/Documents/study/windy-pops/src python -m windy_pops.windy_pops
```
cron job, e.g. to run every 12 hours:
```bash
* */3 * * * PYTHONPATH=/home/std3ldn/Documents/study/windy-pops/src /home/std3ldn/Documents/study/windy-pops/.venv/bin/python -m windy_pops
```
or every day at 5am:
```bash
0 5 * * * PYTHONPATH=/home/std3ldn/Documents/study/windy-pops/src /home/std3ldn/Documents/study/windy-pops/.venv/bin/python -m windy_pops
```
Edit the cron job with:
```bash
crontab -e
```

For dev and testing, you can use saved data to avoid hitting the API too often.
```
    # gather data from file, cache, or api
    #data_loader = DataLoader.from_file(DATA_DIR / Path("2025-sample-data.json"))
    #data_loader = DataLoader.from_file(DATA_DIR / Path("2024-10-07-09-50-54.json"))
    #data_loader = DataLoader.from_latest_cache()
    #data_loader = Metoffice_dataloader()
    #data_loader.cache()
```




### Forecast sources:
#looked at legacy Datapoint format - to be deprecated March 2025:

https://www.metoffice.gov.uk/services/data/datapoint/api-reference

https://www.metoffice.gov.uk/binaries/content/assets/metofficegovuk/pdf/data/datapoint_api_reference.pdf

will be replaced this year(?) by:
https://www.metoffice.gov.uk/services/data/met-office-weather-datahub

Free if sticking to Global Spot forecasts only: https://datahub.metoffice.gov.uk/docs/f/category/site-specific/type/site-specific/api-documentation

So, using new Datahub format: Global Spot forecast:
- docs: https://datahub.metoffice.gov.uk/docs/f/category/site-specific/type/site-specific/api-documentation#get-/point/three-hourly
- shoreham_beach = {"lat": "50.827274", "long": "-0.271525"}
- definitions: https://www.metoffice.gov.uk/binaries/content/assets/metofficegovuk/pdf/data/global-spot-data-3-hourly.pdf

For Sferics: _Sferics data is normally generated during the whole of the sferics data file time
duration. Consequently, a window of sferics observations that is 3 hours either side of
the Cb file’s time is used._
file:///home/std3ldn/Downloads/FRTR_315_2000P.pdf Numerical Weather Prediction
Evaluation of numerical model parameters used in the prediction of
embedded cumulonimbus,  Forecasting Research Technical Report No. 315
Adrian Pickersgill, MET Office
Also: https://www.metoffice.gov.uk/binaries/content/assets/metofficegovuk/pdf/research/library-and-archive/library/publications/factsheets/factsheet_2-thunderstorms_2023.pdf

Southern Water sewage:

https://www.southernwater.co.uk/our-region/clean-rivers-and-seas-task-force/beachbuoy/

Other sewage providers:

- https://paddleuk.org.uk/water-firms-release-new-storm-overflow-maps/

- https://www.sas.org.uk/water-quality/sewage-pollution-alerts/safer-seas-rivers-service/

live map to pull api from dev tools? https://www.sas.org.uk/water-quality/sewage-pollution-alerts/

add surfers against sewage check?

- no single API but some sources cited: https://www.sas.org.uk/water-quality/sewage-pollution-alerts/safer-seas-rivers-service/

    - The Safer Seas and Rivers Service uses real-time data from a combination of sources.

    - Water companies in England and Wales voluntarily provide us with real-time sewage alerts from sensors located on their Combined Sewer Overflows (CSO), which then automatically send alerts to the Safer Seas and Rivers Service.

    - In addition to the sewage alert, during the bathing season, Pollution Risk Forecasts (PRFs) are issued by the four regulators in the UK.

### Could be useful:

https://realpython.com/build-a-python-weather-app-cli/

OSM maps?:
https://overpass-turbo.eu/

Forecast maps are available on metoffice:
https://datahub.metoffice.gov.uk/docs/f/category/map-images/overview

## To Do:

suggest wing / kite / prone / bike / run session times
(could also suggest kit, i.e. wing/kite size)
river & tide conditions for foil bungee practise

could utilise the cached data to look at changing conditions over time?



## Python notes:

In pycharm ctrl + alt + L pretty formats json

For prettifying tabulated output:
https://pypi.org/project/tabulate/

For sorting out contiguous periods of safe data:
itertools groupby, ~8:20 https://www.youtube.com/watch?v=1p7xa_BHYDs
https://realpython.com/python-itertools/
https://pymotw.com/3/itertools/index.html

string formatting for printing out a table of the scores:
https://docs.python.org/3/library/string.html#formatspec

filenames, paths and file system:
- https://realpython.com/python-pathlib/
- https://docs.python.org/3/library/glob.html
- https://realpython.com/python-datetime/


Current WIP:

uv?

cronjob to send results somewhere?

Datetime stuff
Based on the provided context and code excerpts, here is a summary of where the project could benefit from refactoring to apply DRY (Don't Repeat Yourself) principles:

1. Date and Time Parsing/Formatting


There are multiple places where date and time parsing, formatting, and conversion are handled (e.g., parsing ISO strings, converting to datetime.date, etc.).
Refactor by creating utility functions or a module for all date/time parsing and formatting logic to avoid repetition and centralize changes.
2. Validation and Error Handling


Field validation (e.g., checking date and time ranges) is repeated in several constructors and methods.
Move validation logic into shared helper functions or base classes.
3. String Representation Methods


Methods like __repr__, __str__, and isoformat have similar formatting logic across classes.
Abstract common string formatting logic into reusable functions.
4. Timezone Handling


Timezone offset and name retrieval logic is repeated in both time and datetime classes.
Extract timezone-related logic into a mixin or utility module.
5. Arithmetic and Comparison Operations


Arithmetic and comparison methods for date, time, datetime, and timedelta share similar patterns.
Consider using mixins or base classes to implement shared operator logic.
6. Pickle/Serialization Support


Pickle support methods (__reduce__, __setstate__, etc.) are implemented similarly in multiple classes.
Refactor to use shared serialization helpers.
7. Documentation and Comments


Some docstrings and comments are repeated or very similar.
Consolidate documentation where possible and reference shared behavior.
General Recommendation:
Identify repeated code blocks and logic, especially in constructors, string formatting, validation, and arithmetic operations. Move these into shared utility functions, mixins, or base classes to improve maintainability and reduce duplication. This will make the codebase easier to update and less error-prone.