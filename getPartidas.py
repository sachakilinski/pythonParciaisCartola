import requests

partidasdata = requests.get('https://api.cartolafc.globo.com/partidas')
rodada = partidasdata.json()["rodada"]

ligafilepath = "data/2016/partidas/partidas_rodada_" + str(rodada) + ".json"

with open(ligafilepath, 'w') as f:
    f.write(partidasdata.text.encode("UTF-8"))





