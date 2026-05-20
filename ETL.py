import pandas as pd
import pymysql
from dotenv import load_dotenv
from sqlalchemy import create_engine,text
import os
from config import unit_map,category_map
from functions import clean_country

# ==================================================
# import csv, extract
# ==================================================
df=pd.read_csv("renewable_energy_share_2000_2025.csv").copy()

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
df_year['decade'] = ((df_year['year'] // 10) * 10).astype(str) + 's'
df_year['year_id'] = df_year.index + 1
df_year = df_year[['year_id', 'year', 'decade']]
    
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
    
# --------------------------------
# Build fact_energy Table
# --------------------------------
df_fact = df.melt(
    id_vars=[
        'country',
        'year'
    ],
    value_vars=indicator_cols,
    var_name='indicator_name',
    value_name='value'
)
    
df_fact = df_fact.merge(
    df_entity[
        [
            'entity_id',
            'entity_name'
        ]
    ],
    left_on='country',
    right_on='entity_name',
    how='left'
)
    
df_fact = df_fact.merge(
    df_year[
        [
            'year_id',
            'year'
        ]
    ],
    on='year',
    how='left'
)
    
df_fact = df_fact.merge(
    df_indicator[
        [
            'indicator_id',
            'indicator_name'
        ]
    ],
    on='indicator_name',
    how='left'
)
    
df_fact = df_fact.reset_index(drop=True)
    
df_fact['fact_id'] = (
    df_fact.index + 1
)
    
df_fact = df_fact[
    [
        'fact_id',
        'entity_id',
        'year_id',
        'indicator_id',
        'value'
    ]
]


# ==================================================
# write data to mysql, load
# ==================================================

# database connection
load_dotenv()
    
engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}"
)
# print("connected!")

# ==================================================
# delete data
# ==================================================

with engine.connect() as conn:
# Delete child table first
    conn.execute(
        text("DELETE FROM fact_energy")
    )

    # Delete dimension tables
    conn.execute(
        text("DELETE FROM year")
    )

    conn.execute(
        text("DELETE FROM entity")
    )

    conn.execute(
        text("DELETE FROM indicator")
    )

    conn.commit()

# ==================================================
# Load Tables
# ==================================================
df_year.to_sql(
    'year',
    con=engine,
    if_exists='append',
    index=False
)

df_entity.to_sql(
    'entity',
    con=engine,
    if_exists='append',
    index=False
)

df_indicator.to_sql(
    'indicator',
    con=engine,
    if_exists='append',
    index=False
)

df_fact.to_sql(
    'fact_energy',
    con=engine,
    if_exists='append',
    index=False
)

print("data loaded!")
