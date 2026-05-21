import pandas as pd
import pycountry_convert as pc
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine #
from dotenv import load_dotenv
from getpass import getpass #to import pwd hidden
import os
import mysql.connector

####################################################################
# Obtain the df of Europe: filter only Europ; keep other data same #
####################################################################

def get_continent_name(country_name):
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        return pc.convert_continent_code_to_continent_name(continent_code)
    except:
        return "Unknown"



def get_df_europe(df):
    df1 = df.copy()
    #clean the country column
    df1["country"] = df1.country.apply(lambda x: x.strip().capitalize())
    df1["continent"] = df1.country.apply(get_continent_name)
    condition = df1.continent == "Europe"
    df1 = df1[condition].reset_index()
    return df1
#=============================================================================
df2 = get_df_europe(df) #this is the Europe dataframe
#=============================================================================
###############################################################
#Renewable transition over time
###############################################################
def renew_energy_transition(df2, top_n = 5):
    """
    input: df1 = df2
    show the transition of europe coutries to renewable energy
    output line plot
    """
    df1= df2.copy()
    plt.figure(figsize=(12,6))
    
    col_to_find = ["country", "year", "energy"]
    
    top_n_countries = df1.groupby("country")["renewables_share_energy"].mean().nlargest(top_n).reset_index()
    #keep only topn_n countries in df to visualize
    condition = df1["country"].isin(top_n_countries["country"])
    df1 = df1[condition]
    country_plot = sns.lineplot(data = df1, x= "year", y = "renewables_share_energy", hue = "country", palette = "tab10")
    #plot settings
    plt.title("How fast is the energy transition going in Europe?")
    plt.legend(loc="upper left")
    plt.show()

    return country_plot

##############################################################################
# most dependent countries on fossil energy
##############################################################################
def fossil_dep_countries(df2, top_n= 5):
    """
    input: df2=  df_europe
    show the most dependent on fossil energy countries
    output line plot
    """
    df1= df2.copy()
    plt.figure(figsize=(12,6))
    
    col_to_find = ["country", "year", "energy"]
    
    top_n_countries = df1.groupby("country")["fossil_share_energy"].mean().nlargest(top_n).reset_index()
    #keep only topn_n countries in df to visualize
    condition = df1["country"].isin(top_n_countries["country"])
    df1 = df1[condition]
    country_plot = sns.lineplot(data = df1, x= "year", y = "fossil_share_energy", hue = "country", palette = "tab10")
    #plot settings
    plt.title("Most fossil-dependant EU countries")
    plt.legend(loc="upper right")
    plt.show()

    return country_plot

##############################################################################
# Create the parent tables: location table & year table
##############################################################################

def location_table(df2):
    
    """
    input: europe DF
    keeps only columns: country + continent & remove duplicates
    outputs location_table csv file
    """
    df1= df2.copy()
    
    location_table = (
    df1[["country", "continent"]]
    .drop_duplicates(keep = "first")
    .reset_index(drop = True)
    )
    location_table.insert(0, "location_id", location_table.index + 1)

    return location_table
    
def year_table(df2):
    """
    input: europe DF
    keeps only one column: year
    outputs location_table csv file
    """
    df1 = df2.copy()
    
    year_table =(
        df1[["year"]]
        .drop_duplicates(keep = "first")
        .reset_index(drop = True)
    ) 
    year_table.insert(0, "year_id", year_table.index + 1)
    
    return year_table

##############################################################################
# Merge the 2 parent tables to the original df_europe and keep: output df2
##############################################################################
def merge_country_year(df2):
    df1 = df2.copy()
    df1 = (df1
          .merge(location_table(df1), on = ["country", "continent"])
          .merge(year_table(df1), on = "year")
          )
    return df1

##############################################################################
# Create the kid tables: statistics and population
##############################################################################
def stats_table(df_main):
    """
    input: europe main (country id + year id)
    keeps only one column: statistics
    outputs location_table csv file
    """
    df1 = df_main.copy()
    
    stats_table =(
         df1[[
             "location_id",
             "year_id",
             "renewables_share_energy",
             "fossil_share_energy",
             "renewables_share_elec"
            ]].copy()
    )
    #generate stat_id
    stats_table['stat_id'] = range(
        1, len(stats_table["location_id"]) +1
    )
     
    return stats_table

def population_table(df_main):
    """
    input: df_main
    keeps only one column: statistics
    outputs location_table csv file
    """
    df1 = df_main.copy()
    
    population_table =(
         df1[[
             "location_id",
             "year_id",
             "population",
             "gdp"
             ]].copy()
    )
    #generate stat_id
    population_table['pop_id'] = range(
        1, len(population_table["location_id"]) +1
    )
     
    return population_table

##############################################################################
# EXPORTING dataframes into csv failes
##############################################################################

def export_csv(df2):
    output_dir = r"C:\Users\ziden\Desktop\Trainings\IRONHACK\Week3\mini_project_w3\exported_csv"
    #df_europe.to_csv("renewable_energy_dataset_cleaned.csv", index=False, encoding= "utf-8", sep = ";")
    #1. export location table
    loc_table = location_table(df2)
    loc_table.to_csv(f"{output_dir}/location_table_csv.csv", index=False, encoding= "utf-8", sep = ";")
    print("=========================================================================")
    print("File 'location_table_csv' exported successfully")
   
    #2. export year table
    yr_table = year_table(df2)
    yr_table.to_csv(f"{output_dir}/year_table_csv.csv", index=False, encoding= "utf-8", sep = ";")
    print("=========================================================================")
    print("File 'year_table_csv' exported successfully")
    
    #3. generatin main table:
    df_main = merge_country_year(df2)
    #df_main.to_csv("df_main_csv", index=False, encoding= "utf-8", sep = ";")
    
    #4. export statistics table
    stat_table = stats_table(df_main)
    stat_table.to_csv(f"{output_dir}/stats_table_csv.csv", index=False, encoding= "utf-8", sep = ";")
    print("=========================================================================")
    print("File 'stats_table_csv' exported successfully")
    
    #5. export population table
    pop_table = population_table(df_main)
    pop_table.to_csv(f"{output_dir}/population_table_csv.csv", index=False, encoding= "utf-8", sep = ";")
    print("=========================================================================")
    print("File 'population_table_csv' exported successfully")

##############################################################################
# AREA PLOT: TRANSITION FROM FOSSIL TO RENEWABLE ENERGIES
##############################################################################

#1. get data directly from SQL:
#df1 = pd.read_csv(r"Desktop/Trainings/IRONHACK/Week3/mini_project_w3/exported_csv/renew_fossil_av_area_plot.csv")

def read_sql_area_chart():
    # Create database engine
    engine = create_engine('mysql+pymysql://root:passwd@localhost:3306/proj_w3')
   
    query = """
        SELECT
    	st.year_id, y.year,
    	AVG(renewables_share_energy) as renew_av,
        AVG(fossil_share_energy) as fossil_av
        FROM energy_statistics as st
        LEFT JOIN year_table as y
        ON st.year_id = y.year_id
        GROUP BY st.year_id
        ORDER BY st.year_id;
        """
    # Fixed: using 'engine' instead of 'conn'
    df1 = pd.read_sql(query, engine)
    return df1


    
#1. Drawing areaplot:
def renew_fossil_area_plot():
    #get the df from sql
    df1 = read_sql_area_chart()
    my_plot = df1.plot.area(
        x = "year",
        y = ["renew_av", "fossil_av"],
        figsize=(12,6),
        alpha=0.85
    )

    ##Europe target line: 
    # Target line
    plt.axhline(
    y=42.5,
    color="red",
    linestyle="--",
    linewidth=2,
    label="EU 2030 Target"
    )
    #plot legend:
    plt.title("Global Energy Transition Over Time")
    plt.xlabel("Year")
    plt.ylabel("Average Energy Share (%)")
    plt.legend(
    ["Renewable Energy", "Fossil Energy"],
    title="Energy Sources",
    fontsize=12,
    title_fontsize=13,
    loc="center left",
    bbox_to_anchor=(1, 0.5),
    frameon=True
    )
    plt.show()
renew_fossil_area_plot()  
