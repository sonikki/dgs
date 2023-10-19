from flask import Flask, render_template, request, jsonify
import pandas as pd
from tabulate import tabulate


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
    """
    Returns the top 10 scores for a given course and player, as well as the top 10 scores for the entire course.

    Args:
        None

    Returns:
        A JSON object containing the top 10 scores for the given course and player, as well as the top 10 scores for the entire course.
    """
    data = request.get_json()
    rata_index = int(data['rata_index'])
    pelaaja_index = int(data['pelaaja_index'])

    if rata_index >= len(radat):
        return jsonify({'error': 'Invalid rata_index'})

    if df is not None:
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

    return jsonify([])

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
    global df  # Use the global keyword to access the global df variable

    file = request.files['file']

    if file:
        try:
            # Load the file into a Pandas DataFrame
            df = pd.read_csv(file)

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
        except Exception as e:
            return jsonify({'message': f'Tiedoston lataaminen epäonnistui: {str(e)}'})

    return jsonify({'message': 'Tiedoston lataaminen epäonnistui'})


@app.route('/get_courses_for_player', methods=['POST'])
def get_courses_for_player():
    data = request.get_json()
    pelaaja = data['pelaaja']

    if df is not None:
        # Filter the DataFrame to get the courses for the selected player
        pelaajan_radat = df.loc[df['PlayerName'] == pelaaja]['CourseName'].unique()

        return jsonify(list(pelaajan_radat))

    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)