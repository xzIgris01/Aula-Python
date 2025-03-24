import time
import pandas as pd
import matplotlib.pyplot as plt
from plyer import notification
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import email.message
import schedule


def rodar_script():

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

 def envia_email():

    corpo_email = """
    
 Olá, boa noite

 Segue o email com o relatório em anexo.

    """
    
    # Usando MIMEMultipart para suportar anexo
    msg = MIMEMultipart()
    msg['Subject'] = 'Relatório de Vendas'
    msg['From'] = 'scriptvinipython@gmail.com'
    msg['To'] = 'pythonexercicio1907@gmail.com'
    password = 'tvwmwczxeyxxgrsh'

    # Adicionando o corpo do e-mail
    msg.attach(MIMEText(corpo_email, 'plain'))

    # Anexando o arquivo
    with open('relatorio.xlsx', 'rb') as arquivo:
        anexo = MIMEBase('application', 'octet-stream')
        anexo.set_payload(arquivo.read())
        encoders.encode_base64(anexo)
        anexo.add_header('Content-Disposition', 'attachment', filename='relatorio.xlsx')
        msg.attach(anexo)

    # Enviando o e-mail
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(msg['From'], password)
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        s.quit()

        print('Email enviado com sucesso!')

    except Exception as e:
        print(f'Falha ao enviar email: {e}')


# Chamando a função para enviar o e-mail
 envia_email()


# Agendando o script para rodar todo dia às 9h
 schedule.every().day.at("21:11").do(rodar_script)

# Loop para manter o agendamento funcionando
while True:
    schedule.run_pending()
    time.sleep(5)  # Verifica se é hora de rodar o script a cada 60 segundos

rodar_script()