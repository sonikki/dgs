from flask import Flask, render_template, request, jsonify
import pandas as pd
from tabulate import tabulate
import os

app = Flask(__name__)

# Lue CSV-tiedosto DataFrameen (Tämä poistetaan, koska tiedosto ladataan käyttäjältä)
df = None  # Alustetaan DataFrame tyhjäksi

radat = []
pelaajat = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_top_scores', methods=['POST'])
def get_top_scores():
    data = request.get_json()
    rata_index = int(data['rata_index'])
    pelaaja_index = int(data['pelaaja_index'])

    valittu_rata = radat[rata_index]
    valittu_pelaaja = pelaajat[pelaaja_index]

    rata_data = df[df['CourseName'] == valittu_rata]
    top_10_koko_rata = tabulate(rata_data.sort_values(by='+/-').head(10)[['PlayerName', 'CourseName', 'Kaikki', '+/-']], headers='keys', tablefmt='html', showindex=False).strip()
    valitun_pelaajan_tulokset = rata_data[rata_data['PlayerName'] == valittu_pelaaja].sort_values(by='+/-').head(10)
    top_10_pelaaja = tabulate(valitun_pelaajan_tulokset[['PlayerName', 'CourseName', 'Kaikki', '+/-']], headers='keys', tablefmt='html', showindex=False).strip()

    response_data = {
        'top_10_koko_rata': top_10_koko_rata,
        'top_10_pelaaja': top_10_pelaaja
    }

    return jsonify(response_data)

@app.route('/hae_radat')
def hae_radat():
    if df is not None:
        unique_radat = df['CourseName'].unique()
        return jsonify(list(unique_radat))
    return jsonify([])

@app.route('/hae_pelaajat')
def hae_pelaajat():
    if df is not None:
        unique_pelaajat = df['PlayerName'].unique()
        return jsonify(list(unique_pelaajat))
    return jsonify([])

@app.route('/hae_tulokset', methods=['POST'])
def hae_tulokset():
    data = request.get_json()
    rata = data['rata']
    pelaaja = data['pelaaja']

    print(f'Saatu rata: {rata}')
    print(f'Saatu pelaaja: {pelaaja}')

    if df is not None:
        # Hae tulokset tietokannasta käyttäen rata- ja pelaajatietoja
        tulokset = df.loc[(df['CourseName'] == rata) & (df['PlayerName'] == pelaaja)]
        print(f'Löydetty {len(tulokset)} tulosta')  # Tulosten määrä

        # Muunna tulokset JSON-muotoon
        tulokset_json = tulokset.to_dict(orient='records')

        return jsonify(tulokset_json)

    return jsonify([])

@app.route('/upload_file', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']

    if uploaded_file:
        # Save the uploaded file to a specific folder
        file_path = os.path.join("uploads", uploaded_file.filename)
        uploaded_file.save(file_path)

        # Read the uploaded file into the DataFrame
        global df
        df = pd.read_csv(file_path)

        # Update radat and pelaajat from the new DataFrame
        global radat
        radat = df['CourseName'].unique()

        global pelaajat
        pelaajat = df['PlayerName'].unique()

        # Return a response message
        response_data = {
            'message': 'Tiedoston lataus onnistui',
        }

        return jsonify(response_data)

    return jsonify({'message': 'Tiedoston lataaminen epäonnistui'})


if __name__ == '__main__':
    app.run(debug=True)
