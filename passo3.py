import pandas as pd
import matplotlib.pyplot as plt
from plyer import notification
import smtplib


dadosProdutos = pd.read_csv('vendas.csv')
print(dadosProdutos)

indice = dadosProdutos['TvP'].idxmax()

Produdo_com_maior = dadosProdutos.loc[indice,'produto']  
q = dadosProdutos.loc[indice,'quantidade'] 

p = dadosProdutos.loc[indice,'TvP']

print('\nProduto com maior Venda :',Produdo_com_maior,'com',p,'\n' )

notification.notify(
    title ='RELATORIO',
    message=f'o item mais vendido é {Produdo_com_maior}\n com {q} unidades vendidas. \n com um valor de R${p}',
    timeout=10
)

relatorio = pd.DataFrame({
    'Produto': [Produdo_com_maior],
    'Quantidade Vendida': [q],
    'Valor Total': [p]
})

# Salvando o relatório em um arquivo Excel
with pd.ExcelWriter('relatorio.xlsx', engine='openpyxl') as writer:
    # Criando uma aba para o resumo
    relatorio.to_excel(writer, sheet_name='Resumo', index=False)