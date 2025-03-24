import pandas as pd
import matplotlib.pyplot as plt
from plyer import notification
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import schedule
import time

def rodar_script():
    dadosProdutos = pd.read_csv('vendas.csv')

    # Cálculo do Ticket Médio
    ticket_medio = dadosProdutos['TvP'].sum() / dadosProdutos['quantidade'].sum()
    print(f'\nTicket Médio: R${ticket_medio:.2f}\n')

    # Produtos com Baixa Margem de Lucro
    dadosProdutos['margem_lucro'] = (dadosProdutos['TvP'] - dadosProdutos['custo']) / dadosProdutos['TvP']
    produtos_baixa_margem = dadosProdutos[dadosProdutos['margem_lucro'] < 0.20] # Margem de lucro menor que 20%
    print('Produtos com Baixa Margem de Lucro:\n', produtos_baixa_margem['produto'])

    # Top 3 Produtos Mais Lucrativos
    dadosProdutos['lucro_total'] = (dadosProdutos['TvP'] - dadosProdutos['custo']) * dadosProdutos['quantidade']
    top_3_lucrativos = dadosProdutos.nlargest(3, 'lucro_total')
    print('\nTop 3 Produtos Mais Lucrativos:\n', top_3_lucrativos[['produto', 'lucro_total']])

    # Restante do seu código (produto mais vendido, relatório, e-mail)
    indice = dadosProdutos['TvP'].idxmax()
    Produdo_com_maior = dadosProdutos.loc[indice, 'produto']
    q = dadosProdutos.loc[indice, 'quantidade']
    p = dadosProdutos.loc[indice, 'TvP']

    print('\nProduto com maior Venda :', Produdo_com_maior, 'com', p, '\n')

    notification.notify(
        title='RELATORIO',
        message=f'o item mais vendido É{Produdo_com_maior}\n com {q} unidadades vendidadas. \n com um valor de R${p}',
        timeout=10
    )

    relatorio = pd.DataFrame({
        'Produto': [Produdo_com_maior],
        'Quantidade Vendida': [q],
        'Valor Total': [p]
    })

    with pd.ExcelWriter('relatorio.xlsx', engine='openpyxl') as writer:
        relatorio.to_excel(writer, sheet_name='Resumo', index=False)

    def envia_email():
        corpo_email = """
        Olá, boa noite

        Segue o email com o relatório em anexo.
        """

        msg = MIMEMultipart()
        msg['Subject'] = 'Relatório de Vendas'
        msg['From'] = 'scriptvinipython@gmail.com'
        msg['To'] = 'pythonexercicio1907@gmail.com'
        password = 'tvwmwczxeyxxgrsh'

        msg.attach(MIMEText(corpo_email, 'plain'))

        with open('relatorio.xlsx', 'rb') as arquivo:
            anexo = MIMEBase('application', 'octet-stream')
            anexo.set_payload(arquivo.read())
            encoders.encode_base64(anexo)
            anexo.add_header('Content-Disposition', 'attachment', filename='relatorio.xlsx')
            msg.attach(anexo)

        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(msg['From'], password)
            s.sendmail(msg['From'], msg['To'], msg.as_string())
            s.quit()
            print('Email enviado com sucesso!')
        except Exception as e:
            print(f'Falha ao enviar email: {e}')

    envia_email()

# Agendando o script para rodar todo dia às 9h
schedule.every().day.at("18:51").do(rodar_script)

# Loop para manter o agendamento funcionando
while True:
    schedule.run_pending()
    time.sleep(5)

rodar_script()