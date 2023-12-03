from google.oauth2 import service_account
from google_json import google_json
import pandas as pd
import gspread
import json
import os

google_json_dump = json.dumps(google_json)
service_account_info = json.loads(google_json_dump)
credentials = service_account.Credentials.from_service_account_info(service_account_info)
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds_with_scope = credentials.with_scopes(scope)
client = gspread.authorize(creds_with_scope)
spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1fqORjfBLPrPN82CcBEYj-YqQ2lfppaCgDUv1I4W84SU/edit#gid=0')
worksheet = spreadsheet.get_worksheet(0)
records_data = worksheet.get_all_records()
records_df = pd.DataFrame.from_dict(records_data)
sim_row = records_df[(records_df == "sim")]
records_df
itens = {}
numRegistrosTotal = 0
for i, row in enumerate(records_df):
    posicoes = {}
    dict = records_df[row].to_dict()
    for j in dict:
        if dict[j] == "sim":
            posicoes.update({j: i})
            itens.update({str(row) : posicoes})
            numRegistrosTotal+=1
print(itens)
print("Número total de registros: "+str(numRegistrosTotal))
suportes = {}
confianças = {}
for index, i in enumerate(itens):
    list = {}
    suporte = 0
    for j in itens[i].keys():
        for index2, k in enumerate(itens):
            ocorrencias = 0
            if index2!=index:
                for l in itens[k].keys():
                    if j == l:
                        ocorrencias +=1
                        if k in list:
                            list.update({k:list.get(k)+ocorrencias})
                        else:
                            list.update({k:ocorrencias})
                suporte = list.get(k, 0)/10
                confiança = list.get(k, 0)/len(itens[i].keys())
                atual = suportes.get(str(i)+"-"+str(k), "nulo")
                if atual == "nulo" and suporte == 0.0:
                    suportes.update({str(i)+"-"+str(k): 0})
                    confianças.update({str(i)+"-"+str(k): 0})
                elif atual == "nulo" and suporte !=0.0:
                    suportes.update({str(i)+"-"+str(k): suporte})
                    confianças.update({str(i)+"-"+str(k): confiança})
                elif atual<=suporte:
                    suportes.update({str(i)+"-"+str(k): suporte})
                    confianças.update({str(i)+"-"+str(k): confiança})
print("-----------SUPORTE-----------")
for i, j in suportes.items():
    if j>0:
        print(i, j)
print("-----------CONFIANÇA-----------")
for i, j in confianças.items():
    if j>0:
        print(i, j)