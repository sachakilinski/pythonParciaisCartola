from __future__ import print_function

import json
import urllib
import boto3
import requests

print('Loading function')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = "cartola-pipeline"
    key = "pontuados.json"
    try:
        parciaisdata = requests.get('https://api.cartolafc.globo.com/atletas/pontuados')
        parciais_sorted = sorted(parciaisdata.json()["atletas"].values(), key=lambda x: x["pontuacao"], reverse=True)
        print([ {s["apelido"] : s["pontuacao"]}  for s in parciais_sorted])
        response = s3.put_object(Body=json.dumps(parciais_sorted), Bucket=bucket, Key=key, Metadata={'Content-Type':'application/json'})
        return response
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e