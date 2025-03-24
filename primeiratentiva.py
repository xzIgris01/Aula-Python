import pandas as pd
from plyer import notification
import openpyxl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import matplotlib.pyplot as plt
import schedule
import time
import sqlite3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- 1. Leitura e análise de CSV ---
def analisar_vendas():
    try:
        df = pd.read_csv('vendas.csv')
        total_por_produto = df.groupby('produto')['quantidade'].sum()
        produto_mais_vendido = total_por_produto.idxmax()
        total_geral = df['quantidade'].sum()
        print(f"Produto mais vendido: {produto_mais_vendido}")
        print(f"Total geral: {total_geral}")

        # --- 2. Enviar notificação ---
        notification.notify(
            title='Resumo de Vendas',
            message=f'Produto mais vendido: {produto_mais_vendido}\nTotal geral: {total_geral}',
            app_name='Análise de Vendas',
            timeout=10
        )

        # --- 3. Relatório em Excel ---
        resumo = df.groupby('produto')['quantidade'].sum().reset_index()
        resumo.to_excel('relatorio.xlsx', sheet_name='Resumo', index=False)

        # --- 5. Gráficos ---
        plt.bar(resumo['produto'], resumo['quantidade'])
        plt.savefig('grafico.jpg')
        plt.close()

        # --- 7. Análise de KPIs ---
        df['total'] = df['quantidade'] * df['preco']
        ticket_medio = df['Total'].mean()
        print(f"Ticket médio: {ticket_medio}")

        # --- 9. Atualização do banco de dados SQLite ---
        conn = sqlite3.connect('vendas.db')
        df.to_sql('vendas', conn, if_exists='replace', index=False)
        conn.close()

        return df
    except FileNotFoundError:
        print("Arquivo vendas.csv não encontrado.")
        return None

# --- 4. Enviar e-mail ---
def enviar_email(df):
    if df is None:
        return
    remetente = 'seu_email@gmail.com'
    senha = 'sua_senha'
    destinatario = 'destinatario@email.com'
    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = 'Relatório de Vendas'
    corpo = MIMEText('Segue o relatório de vendas em anexo.')
    mensagem.attach(corpo)
    with open('relatorio.xlsx', 'rb') as arquivo:
        anexo = MIMEApplication(arquivo.read(), _subtype='xlsx')
        anexo.add_header('Content-Disposition', 'attachment', filename='relatorio.xlsx')
        mensagem.attach(anexo)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
        servidor.login(remetente, senha)
        servidor.send_message(mensagem)
    print("E-mail enviado com sucesso!")

# --- 6. Agendar execução ---
def agendar_tarefa():
    schedule.every().day.at("09:00").do(executar_tarefas)
    while True:
        schedule.run_pending()
        time.sleep(1)

def executar_tarefas():
    df = analisar_vendas()
    enviar_email(df)

# --- 10. Monitorar pasta ---
class ManipuladorDeArquivos(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return None
        elif event.src_path.endswith('.csv'):
            print(f"Novo arquivo detectado: {event.src_path}")
            analisar_vendas()

def monitorar_pasta():
    observer = Observer()
    observer.schedule(ManipuladorDeArquivos(), path='pasta_monitorada')
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# --- 8. Dashboard Tkinter ---
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def carregar_csv_e_exibir_resumo():
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
    if arquivo:
        df = pd.read_csv(arquivo)
        resumo = df.describe()
        texto_resumo.delete(1.0, tk.END)
        texto_resumo.insert(tk.END, str(resumo))

        figura = plt.Figure(figsize=(5, 4), dpi=100)
        grafico = figura.add_subplot(111)
        df['Produto'].value_counts().plot(kind='bar', ax=grafico)

        canvas = FigureCanvasTkAgg(figura, master=janela)
        canvas.draw()
        canvas.get_tk_widget().pack()

janela = tk.Tk()
janela.title("Dashboard de Vendas")
botao_carregar = tk.Button(janela, text="Carregar CSV", command=carregar_csv_e_exibir_resumo)
botao_carregar.pack()
texto_resumo = tk.Text(janela)
texto_resumo.pack()

# --- Execução ---
# executar_tarefas() # Executa a análise e envia o email uma vez.
# agendar_tarefa() # Agenda a execução diária.
# monitorar_pasta() # Monitora a pasta por novos arquivos.
# janela.mainloop() # inicia a interface Tkinter
