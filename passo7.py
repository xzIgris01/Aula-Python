import pandas as pd
import matplotlib.pyplot as plt
from plyer import notification
import smtplib

def rodar_script():
    dadosProdutos = pd.read_csv('vendas.csv')

    # Cálculo do Ticket Médio
    ticket_medio = dadosProdutos['TvP'].sum() / dadosProdutos['quantidade'].sum()
    print(f'\nTicket Médio: R${ticket_medio:.2f}\n')
rodar_script()