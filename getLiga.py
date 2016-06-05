import json

import requests

token = "paste your token here"
ligadata1 = requests.get('https://api.cartolafc.globo.com/auth/liga/ilegrao-2016', headers = { 'X-GLB-Token': token}).json()
ligadata2 = requests.get('https://api.cartolafc.globo.com/auth/liga/ilegrao-2016?page=2', headers = { 'X-GLB-Token': token}).json()
ligadata3 = requests.get('https://api.cartolafc.globo.com/auth/liga/ilegrao-2016?page=3', headers = { 'X-GLB-Token': token}).json()

ligadata1["times"] += ligadata2["times"]
ligadata1["times"] += ligadata3["times"]

ligadata =  json.dumps(ligadata1)

partidasdata = requests.get('https://api.cartolafc.globo.com/partidas')
rodada = partidasdata.json()["rodada"]

ligafilepath = "data/2016/liga/liga_rodada_" + str(rodada) + ".json"

with open(ligafilepath, 'w') as f:
    f.write(ligadata.encode("UTF-8"))





