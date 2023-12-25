# SPDB_project-spatial_prediction

## Objective
The main purpose of this project is to test and compare differents methods of spacial prediction that are available in Python.  
Scope of the project includes following methods of spacial prediction:
 - IDW (Inverse Distance Weighting)
 - Kriging
 - Linear regression

## Methods of comparison
Methods of spacial prediction will be compared based on:
 - Accuracy and robustness of calculated results
 - Time required to calculate the results in relation to amount of data being processed
 - Amount and complexity of preparatory procedures required before using methods
 - Quality and availability of materials explaining methods and their usage in Internet

## Data used
Methods are tested on data from following sources:
 - Poland DEM (Digital Elevation Model), downloaded from [https://mapy.geoportal.gov.pl/](https://mapy.geoportal.gov.pl/)
 - Generated data

## Project Organization
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts to download or generate data
        │
        ├── features       <- Scripts to turn raw data into features for modeling
        │
        ├── models         <- Scripts to train models and then use trained models to make
        │                     predictions
        │
        ├── util           <- Utility functions used in other scripts
        │
        └── visualization  <- Scripts to create exploratory and results oriented visualizations

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
