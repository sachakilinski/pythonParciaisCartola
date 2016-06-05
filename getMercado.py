import requests

mercadodata = requests.get('https://api.cartolafc.globo.com/atletas/mercado')

partidasdata = requests.get('https://api.cartolafc.globo.com/partidas')
rodada = partidasdata.json()["rodada"]
mercadofilepath = "data/2016/mercado/mercado_rodada_" + str(rodada) + ".json"

with open(mercadofilepath, 'w') as f:
    f.write(mercadodata.text.encode("UTF-8"))





