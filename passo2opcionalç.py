import pandas as pd
import openpyxl

dados = pd.read_csv("vendas.csv")

with pd.ExcelWriter("relatorio.xlsx" , engine="openpyxl") as writer:
    dados.to_excel(writer, sheet_name="Resumo" , index=False)