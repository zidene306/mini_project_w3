import pandas as pd
import pymysql
import os
from dotenv import load_dotenv
from config import unit_map,category_map

def clean_country(df_origin):
    df=df_origin.copy();
    
    # remove duplicate country data
    df = df[
    ~df['country'].str.contains(
        r'\(EI\)|\(EIA\)|\(Ember\)|\(Shift\)',
        regex=True,
        na=False
        )
    ]
    # classify country
    df.loc[df['country'] == 'World', 'entity_type'] = 'world'

    regions = [
    'Asia',
    'Europe',
    'Africa',
    'North America',
    'South America',
    'Oceania'
    ]
    df.loc[df['country'].isin(regions), 'entity_type'] = 'region'

    df.loc[
    df['iso_code'].notna() &
    df['entity_type'].isna(),
    'entity_type'
    ] = 'country'

    exclude = [
    'OECD',
    'OPEC',
    'G20',
    'G7',
    'High-income countries',
    'Low-income countries',
    'Upper-middle-income countries',
    'Lower-middle-income countries'
    ]
    df = df[~df['country'].isin(exclude)]

    df.loc[df['country'] == 'Kosovo', 'entity_type'] = 'country'
    df.loc[
    df['country'] == 'European Union (27)',
    'entity_type'
    ] = 'region'
    df.loc[
    df['country'] == 'Serbia and Montenegro',
    'entity_type'
    ] = 'country'

    df=df.sort_values(by="country").reset_index(drop=True)

    return df

# ==================================================
# import csv, extract
# ==================================================
df=pd.read_csv("renewable_energy_share_2000_2025.csv")

# ==================================================
# transform
# ==================================================
# clean data
df = clean_country(df)

# entity
df_entity = (
    df[
        [
            'country',
            'iso_code',
            'entity_type'
        ]
    ]
    .drop_duplicates()
    .sort_values('country')
    .reset_index(drop=True)
)
df_entity['entity_id'] = df_entity.index + 1
df_entity = df_entity.rename(
    columns={
        'country': 'entity_name'
    }
)
df_entity = df_entity[
    [
        'entity_id',
        'entity_name',
        'iso_code',
        'entity_type'
    ]
]

# year
df_year = (
    df[['year']]
    .drop_duplicates()
    .sort_values('year')
    .reset_index(drop=True)
)
df_year['decade'] = (
    (df_year['year'] // 10) * 10
).astype(str) + 's'
df_year['year_id'] = df_year.index + 1
df_year = df_year[
    ['year_id', 'year', 'decade']
]

# --------------------------------
# Build Indicator Dimension Table
# --------------------------------
# Non-indicator columns
non_indicator_cols = [
    'country',
    'year',
    'iso_code',
    'entity_type'
]

# Extract indicator columns
indicator_cols = [
    col for col in df.columns
    if col not in non_indicator_cols
]

# Create indicator dataframe
df_indicator = pd.DataFrame({
    'indicator_name': indicator_cols
})

# Generate surrogate key
df_indicator['indicator_id'] = (
    df_indicator.index + 1
)

df_indicator['unit'] = (
    df_indicator['indicator_name']
    .map(unit_map)
)

df_indicator['category'] = (
    df_indicator['indicator_name']
    .map(category_map)
)

# Reorder columns
df_indicator = df_indicator[
    [
        'indicator_id',
        'indicator_name',
        'unit',
        'category'
    ]
]

# fact_energy
df_fact

# ==================================================
# write data to mysql, load
# ==================================================
# database connection
load_dotenv()

engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}"
)
