## Cartola-Pipeline

python scripts para modo offline e lambda-packages que estão sendo utilizados utilizados para visualizar as parciais do Ilegrão.

## Histórico de Desenvolvimento

A ideia sempre foi fugir de subir um servidor, e gerar uma página estática com as parciais.
no início eram apenas os scripts locais, como getParciaisLiga.py.
Com o tempo está tudo sendo migrado para o AWS lambda, por isso a pasta lambda-packages.
Há 2 lambda functions funcionais atualmente:
a primeira (updateEscalacoes) chamo manualmente 1 vez por rodada para atualizar o arquivo "escalacoes.json" no S3.
a segunda  (updateLiga) está rodando automaticamente a cada 15 minutos. O próximo passo é economizar e rodar apenas quando houver jogos em andamento, usando como base os horários das partidas do Brasileirão.

Esses scripts e packages estão sendo utilizados para a liga do Ilegrão, mas podem facilmente ser generalizados para uma liga qualquer.

Eis o endereço dessa página estática gerada:
https://s3-sa-east-1.amazonaws.com/ilegrao/index.html