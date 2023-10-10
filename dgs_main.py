import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
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

# Tallenna taulukko PDF-tiedostona
doc = SimpleDocTemplate('top10.pdf', pagesize=letter)
elements = []

# Muotoile taulukko
data = [['Pelaaja(t)', 'Rata', 'Par', '+/-']] + top_10[['PlayerName', 'CourseName', 'Kaikki', '+/-']].values.tolist()
t = Table(data)

# Muotoilu taulukolle
style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), (0.9, 0.9, 0.9)),
    ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), (1, 1, 1)),
    ('GRID', (0, 0), (-1, -1), 0.5, (0, 0, 0)),
])

t.setStyle(style)
elements.append(t)
doc.build(elements)

# Näytä taulukko konsolissa
print(tabulate(top_10[['PlayerName', 'CourseName', 'Kaikki', '+/-']], headers='keys', tablefmt='grid', showindex=False))

