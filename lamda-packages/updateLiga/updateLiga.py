from __future__ import print_function

import json
import boto3
import requests
import copy
import datetime
from jinja2 import Environment
from jinja2_s3loader import S3loader
import os

print('Loading function')

bucket = "cartola-pipeline"
s3 = boto3.client('s3')
escalacoesdata = json.loads(s3.get_object(Bucket=bucket, Key="escalacoes.json")["Body"].read())
j2 = Environment(loader=S3loader(bucket))
template = j2.get_template("template.html")

def getSomaParcial(time):
    newtime = copy.deepcopy(time)
    newtime.update({"parcial" : 0})
    for atleta in newtime["atletas"]:
        try:
            newtime["parcial"] += atleta["pontos"]
        except KeyError:
            pass
    return newtime

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

def lambda_handler(event, context):
    try:
        parciaisdata = requests.get('https://api.cartolafc.globo.com/atletas/pontuados')

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

        timesatletasparciais = map(updateAtletas, escalacoesdata)

        timessoma= map(getSomaParcial, timesatletasparciais)

        data = [(t["cartola"], t["nome"], t["parcial"], getApelidos(t), getPontosTime(t)) for t in sorted(timessoma, key=lambda x: x["parcial"], reverse=True)]

        now= (datetime.datetime.now() - datetime.timedelta(hours=3)).strftime("%d/%m %H:%M")

        s3.put_object(Bucket="ilegrao", Key="index.html", Body=template.render(data=data, timestamp=now), ContentType='text/html', ACL='public-read')

        return "exported parciais to s3"

    except Exception as e:
        print(e)
        raise e