import pandas as pd

# Määrittele tiedoston nimi
tiedoston_nimi = "frisbeegolf_stats.csv"

# Lue tiedosto Pandas DataFrameen
data = pd.read_csv(Puolarmaari.csv)

# Tulosta ensimmäiset viisi riviä nähdäksesi, että tiedosto on ladattu oikein
print(data.head())