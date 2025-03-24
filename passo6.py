import pandas as pd
import matplotlib.pyplot as plt
from plyer import notification
import smtplib
import schedule
import time


def rodar_script():

    dadosProdutos = pd.read_csv('vendas.csv')
    print(dadosProdutos)

    dadosProdutos["total_vendido"] = dadosProdutos["quantidade"] * dadosProdutos["preco"]
    total_produto = dadosProdutos.groupby('produto')['total_vendido'].sum()

    produtoVendidomais = total_produto.idxmax()

    total_vendido = total_produto.max()

    relatorio = {
    'Produto mais vendido': produtoVendidomais,
    'total do produto mais vendido': total_vendido
    }
    print(f"Relatorio\n Produto mais vendido: {relatorio['Produto mais vendido']}\n{relatorio['total do produto mais vendido']}")


    
#parte 6 é a parte que impoorta
    schedule.every().day.at("20:45").do(rodar_script)

# Loop para manter o agendamento funcionando
while True:
    schedule.run_pending()
    time.sleep(5)

rodar_script()