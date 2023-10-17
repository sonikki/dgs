from flask import Flask, render_template, request, jsonify
import pandas as pd
from tabulate import tabulate

app = Flask(__name__)

# Lue CSV-tiedosto DataFrameen
df = pd.read_csv("scorecards.csv")
ratat = df['CourseName'].unique()
pelaajat = df['PlayerName'].unique()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_top_scores', methods=['POST'])
def get_top_scores():
    data = request.get_json()
    rata_index = int(data['rata_index'])
    pelaaja_index = int(data['pelaaja_index'])

    valittu_rata = ratat[rata_index]
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
    return jsonify(ratat.tolist())

@app.route('/hae_pelaajat')
def hae_pelaajat():
    return jsonify(pelaajat.tolist())

@app.route('/hae_tulokset', methods=['POST'])
def hae_tulokset():
    data = request.get_json()
    rata = data['rata']
    pelaaja = data['pelaaja']

    print(f'Saatu rata: {rata}')
    print(f'Saatu pelaaja: {pelaaja}')

    # Hae tulokset tietokannasta käyttäen rata- ja pelaajatietoja
    # Esimerkki: Oletetaan, että sinulla on DataFrame 'df', ja haet tulokset sen perusteella
    tulokset = df.loc[(df['CourseName'] == rata) & (df['PlayerName'] == pelaaja)]
    print(f'Löydetty {len(tulokset)} tulosta')  # Tulosten määrä

    # Muunna tulokset JSON-muotoon
    tulokset_json = tulokset.to_dict(orient='records')

    return jsonify(tulokset_json)

if __name__ == '__main__':
    app.run(debug=True)
