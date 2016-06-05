
import json

import boto3

import requests

import copy


print('Loading function')

s3 = boto3.client('s3')
bucket = "cartola-pipeline"
ligadata = json.loads(s3.get_object(Bucket=bucket, Key="liga.json")["Body"].read())
key = "escalacoes.json"

def getTimeAtletas(slug):
    print(slug)
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

def lambda_handler(event, context):
    try:
        times = [{"cartola": t["nome_cartola"], "slug": t["slug"], "nome": t["nome"]} for t in ligadata["times"]]
        timesatletas = getAtletas(times)
        s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(timesatletas))
        return "updated escalacoes"
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e