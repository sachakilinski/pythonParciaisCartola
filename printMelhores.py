import requests

parciaisdata = requests.get('https://api.cartolafc.globo.com/atletas/pontuados')

sorted = sorted(parciaisdata.json()["atletas"].values(), key=lambda x: x["pontuacao"], reverse=True)

print [ {s["apelido"] : s["pontuacao"]}  for s in sorted]







