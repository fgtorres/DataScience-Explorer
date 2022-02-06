import pandas

path_arq = "C:\\Users\\Felipe Torres\\OneDrive\\Hackathons\\TheBigHackathon\\datasets\\datasetSPOuvidoriaSaude.csv"

df = pandas.read_csv(path_arq, sep=";")
df.set_index('CNES')
print(df.head())

json = df.to_json()
print(json)