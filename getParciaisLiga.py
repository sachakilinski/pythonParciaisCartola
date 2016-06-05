import json
import copy
import os
import datetime

import requests
from jinja2 import Environment, FileSystemLoader


THIS_DIR = os.path.dirname(os.path.abspath(__file__))


parciaisdata = requests.get('https://api.cartolafc.globo.com/atletas/pontuados')
with open('data/2016/escalacoes/escalacoes_rodada_6.json', 'r') as f:
    escalacoesdata = json.load(f)

def getParcial(atleta):
    newatleta = copy.deepcopy(atleta)
    try:
        newatleta["pontos"] = parciaisdata.json()["atletas"]["%s" %atleta["id"]]["pontuacao"]
    except KeyError:
        pass
    return newatleta

def updateAtletas(time):
    newtime = copy.deepcopy(time)
    newtime.update({"atletas" : map(getParcial, time["atletas"]) })
    return newtime

def getSomaParcial(time):
    newtime = copy.deepcopy(time)
    newtime.update({"parcial" : 0})
    for atleta in newtime["atletas"]:
        try:
            newtime["parcial"] += atleta["pontos"]
        except KeyError:
            pass
    return newtime


timesatletasparciais = map(updateAtletas, escalacoesdata)

timessoma= map(getSomaParcial, timesatletasparciais)

def getApelidos(time):
    return map(lambda x: x["apelido"], time["atletas"])

def getPontosTime(time):
    return map(getPontos, time["atletas"])

def getPontos(atleta):
    try:
        result = atleta["pontos"]
    except KeyError:
        result = "N"
    return result

now= (datetime.datetime.now() - datetime.timedelta(hours=0)).strftime("%d/%m %H:%M")

data = [(t["cartola"], t["nome"], t["parcial"], getApelidos(t), getPontosTime(t)) for t in sorted(timessoma, key=lambda x: x["parcial"], reverse=True)]

parciaishtml= Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True).get_template("template.html").render(data=data, timestamp=now)


with open("parciais.html", 'w') as f:
    f.write(parciaishtml.encode("UTF-8"))
















