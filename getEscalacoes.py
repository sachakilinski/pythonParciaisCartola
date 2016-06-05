import json
import copy
import os

import requests


THIS_DIR = os.path.dirname(os.path.abspath(__file__))


with open('data/2016/liga/liga_rodada_4.json', 'r') as f:
    ligadata = json.load(f)

def getTimeAtletas(slug):
    print slug
    time = requests.get('https://api.cartolafc.globo.com/time/%s' %slug).json()
    try:
        atletas = sorted(time["atletas"], key=lambda x: x["posicao_id"], reverse=False)
    except KeyError:
        atletas = []
    return [ { "id": a["atleta_id"], "apelido": a["apelido"], "clube_id": a["clube_id"], "posicao": a["posicao_id"]}  for a in atletas]

def getAtletas(times):
    newtimes = copy.deepcopy(times)
    for t in newtimes:
        t.update({"atletas": getTimeAtletas(t["slug"])})
    return  newtimes


times = [{"cartola": t["nome_cartola"], "slug": t["slug"], "nome": t["nome"]} for t in ligadata["times"]]

timesatletas = getAtletas(times)

partidasdata = requests.get('https://api.cartolafc.globo.com/partidas')
rodada = partidasdata.json()["rodada"]

filepath = "data/2016/escalacoes/escalacoes_rodada_" + str(rodada) + ".json"

with open(filepath, 'w') as f:
    f.write(json.dumps(timesatletas))
















