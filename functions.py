import pandas as pd
import pymysql
import os
from dotenv import load_dotenv
# from sqlalchemy import create_engine

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

    return df


