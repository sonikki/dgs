import pandas as pd
from tabulate import tabulate

# Lue tiedosto Pandas DataFrameen
df = pd.read_csv("scorecards.csv")

# Luo lista eri ratojen nimistä
ratat = df['CourseName'].unique()

# Tulosta käyttäjälle saatavilla olevat radat
print("Saatavilla olevat radat:")
for i, rata in enumerate(ratat, start=1):
    print(f"{i}. {rata}")

# Kysy käyttäjältä valittavaa radan numeroa
valittu_rata_numero = int(input("Valitse radan numero: ")) - 1

# Valitse haluttu rata
valittu_rata = ratat[valittu_rata_numero]
rata_data = df[df['CourseName'] == valittu_rata]

# Lajittele suoritukset +/- sarakkeen mukaan ja ota top 10
top_10 = rata_data.sort_values(by='+/-').head(10)

# Näytä kaikkien pelaajien top 10 tulokset konsolissa
print("Kaikkien pelaajien top 10 tulokset:")
print(tabulate(top_10[['PlayerName', 'CourseName', 'Kaikki', '+/-']], headers='keys', tablefmt='grid', showindex=False))

# Luo lista pelaajien nimistä
pelaajat = df['PlayerName'].unique()

# Tulosta pelaajien nimet
print("Saatavilla olevat pelaajat:")
for i, pelaaja in enumerate(pelaajat, start=1):
    print(f"{i}. {pelaaja}")

# Kysy käyttäjältä pelaajan numeroa
valittu_pelaaja_numero = int(input("Valitse pelaajan numero: ")) - 1

# Valitse haluttu pelaaja
valittu_pelaaja = pelaajat[valittu_pelaaja_numero]

# Näytä valitun pelaajan top 10 tulokset konsolissa
valitun_pelaajan_tulokset = rata_data[rata_data['PlayerName'] == valittu_pelaaja].sort_values(by='+/-').head(10)
print(f"\n{valittu_pelaaja}'n top 10 tulokset:")
print(tabulate(valitun_pelaajan_tulokset[['PlayerName', 'CourseName', 'Kaikki', '+/-']], headers='keys', tablefmt='grid', showindex=False))
