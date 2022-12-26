import pandas as pd
from typing import List, Dict



def get_percentage(value, total_number):

    percentage = (100/total_number)*value
    return round(percentage,0)

def make_percentage(list_of_numeric_values):

    total_number = sum(list_of_numeric_values)

    list_of_numeric_values = [get_percentage(value, total_number) for value in list_of_numeric_values]

    return list_of_numeric_values



def create_x_y_for_bar_plot(results: List[Dict], x:str):

    results = pd.DataFrame(results)
    
    if x == "country_dialect":
        results["country_dialect"] = results["country"]+"_"+results["dialect"]
    
    results_grouped = results[['primary_key',x]].groupby(x, as_index=False).count().sort_values('primary_key', ascending=False)
    x_values = results_grouped[x].tolist()
    y_values = results_grouped['primary_key'].tolist()
    colors = ['blue' for x in x_values]

    x_y_values = {'x_values': x_values, 'y_values': y_values, 'colors': colors}

    return x_y_values


def find_placename_of_coordinate(dataframe, coordinates_place_name):
    return dataframe[dataframe.coordinates_place_name==coordinates_place_name].place_name.tolist()[0]

def process_data_for_map(results: pd.core.frame.DataFrame):
    if type(results)==list:
        results = pd.DataFrame(results)
    # TODO: Check cases where we do not have coordinates
    results = results[results.coordinates_place_name.str.contains(',')]
    results_grouped = results[['coordinates_place_name', 'Form', 'place_name']].groupby('coordinates_place_name', as_index=False).count()
    results_grouped['id'] = results_grouped["coordinates_place_name"].apply(lambda x: str(x))
    results_grouped['place_name'] = results_grouped["coordinates_place_name"].apply(lambda x: "Place: "+find_placename_of_coordinate(results,str(x)))
    results_grouped['coordinates_place_name'] = results_grouped.coordinates_place_name.apply(lambda x: {'lat': float(x.split(',')[0].strip()), 'lon': float(x.split(',')[1].strip())})
    results_grouped.rename(columns={'Form':'count','place_name':'place_name'}, inplace=True)
    results_grouped['count'] = results_grouped["count"].apply(lambda x: str(x)+" cases")
    results_grouped = results_grouped.to_dict(orient="records")

    return results_grouped
    