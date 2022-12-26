from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from ast import literal_eval
from flask_session import Session
import json

from static.python.queries import DatabaseSearcher
from static.python.utils import create_x_y_for_bar_plot, process_data_for_map


app = Flask(__name__)
app.secret_key = "super secret key"

# https://flask-session.readthedocs.io/en/latest/
# https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)



dbs = DatabaseSearcher()
    

@app.route('/', methods=['GET', 'POST'])
def main_page():

    if request.is_json:

        all_inputs = request.get_json()        
            
        results = dbs.get_query_results(all_inputs)
        
        x_y_values_dialect = create_x_y_for_bar_plot(results, 'dialect')
        x_y_values_country = create_x_y_for_bar_plot(results, 'country')
        x_y_values_country_dialect = create_x_y_for_bar_plot(results, 'country_dialect')
        data_for_map = process_data_for_map(results)

        return_json = dict()

        return_json['results']=results
        return_json['x_y_values_dialect_bar_chart']=x_y_values_dialect
        return_json['x_y_values_country_bar_chart']=x_y_values_country
        return_json['x_y_values_country_dialect']=x_y_values_country_dialect
        return_json['data_for_map'] = data_for_map

        return_json = jsonify(return_json)
        
        return return_json

  
    else:
        print('Is None.')
        print("Not json")
    
        return render_template('main_page.html')


        


if __name__ == "__main__":
    app.run(debug=True)
    #app.run(debug=True, host='0.0.0.0')


  