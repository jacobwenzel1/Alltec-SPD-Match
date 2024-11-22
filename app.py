from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd

app = Flask(__name__)

app.secret_key = '123456789'

# Load SPD data from the CSV file
spd_data = pd.read_csv('SPD_CSV_DATA.csv')

# Clean column names by stripping leading/trailing spaces and special characters
spd_data.columns = spd_data.columns.str.strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match():
    # Get user input for kA Rating, MCOV, Service Voltage, and Voltage Config
    ka_rating = request.form.get('ka_rating')
    mcov = request.form.get('mcov')
    service_voltage = request.form.get('service_voltage')
    voltage_config = request.form.get('voltage_config')
    
    # Convert the relevant columns to strings, in case they're not already
    spd_data['kA Raiting'] = spd_data['kA Raiting'].astype(str)
    spd_data['MCOV (Vac)'] = spd_data['MCOV (Vac)'].astype(str)
    spd_data['Service Voltage (V)'] = spd_data['Service Voltage (V)'].astype(str)
    spd_data['Voltage Config'] = spd_data['Voltage Config'].astype(str)

    # Match by kA Rating, MCOV (Vac), Service Voltage, and Voltage Config
    matched_spd = spd_data[
        (spd_data['kA Raiting'].str.contains(ka_rating, case=False, na=False)) &
        (spd_data['MCOV (Vac)'].str.contains(mcov, case=False, na=False)) &
        (spd_data['Service Voltage (V)'].str.contains(service_voltage, case=False, na=False)) &
        (spd_data['Voltage Config'].str.contains(voltage_config, case=False, na=False))
    ]
    
    # Check if the matched data is empty
    if matched_spd.empty:
        matched_spd = None  # Set to None to show no matches in the template
    
    return render_template('results.html', matched_spd=matched_spd)

if __name__ == '__main__':
    app.run(debug=True)
