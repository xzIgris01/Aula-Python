import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog, messagebox
from plyer import notification
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import schedule
import time
import threading

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard de Vendas")
        
        self.load_button = tk.Button(root, text="Carregar CSV", command=self.load_csv)
        self.load_button.pack(pady=20)

        self.summary_text = tk.Text(root, height=10, width=50)
        self.summary_text.pack(pady=20)

        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(pady=20)

        # Iniciar o agendamento em uma thread separada
        self.schedule_thread = threading.Thread(target=self.run_schedule, daemon=True)
        self.schedule_thread.start()

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.dadosProdutos = pd.read_csv(file_path)
                self.show_summary()
                self.plot_data()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar o arquivo: {e}")

    def show_summary(self):
        self.summary_text.delete(1.0, tk.END)  # Limpa o texto anterior
        ticket_medio = self.dadosProdutos['TvP'].sum() / self.dadosProdutos['quantidade'].sum()
        self.summary_text.insert(tk.END, f'Ticket Médio: R${ticket_medio:.2f}\n')

        # Produtos com Baixa Margem de Lucro
        self.dadosProdutos['margem_lucro'] = (self.dadosProdutos['TvP'] - self.dadosProdutos['custo']) / self.dadosProdutos['TvP']
        produtos_baixa_margem = self.dadosProdutos[self.dadosProdutos['margem_lucro'] < 0.20]
        self.summary_text.insert(tk.END, 'Produtos com Baixa Margem de Lucro:\n')
        self.summary_text.insert(tk.END, produtos_baixa_margem['produto'].to_string(index=False) + '\n')

        # Top 3 Produtos Mais Lucrativos
        self.dadosProdutos['lucro_total'] = (self.dadosProdutos['TvP'] - self.dadosProdutos['custo']) * self.dadosProdutos['quantidade']
        top_3_lucrativos = self.dadosProdutos.nlargest(3, 'lucro_total')
        self.summary_text.insert(tk.END, 'Top 3 Produtos Mais Lucrativos:\n')
        self.summary_text.insert(tk.END, top_3_lucrativos[['produto', 'lucro_total']].to_string(index=False) + '\n')

    def plot_data(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Gráfico de barras dos produtos mais lucrativos
        top_3_lucrativos = self.dadosProdutos.nlargest(3, 'lucro_total')
        ax.bar(top_3_lucrativos['produto'], top_3_lucrativos['lucro_total'], color=['blue', 'green', 'red'])
        ax.set_title('Top 3 Produtos Mais Lucrativos')
        ax.set_xlabel('Produtos')
        ax.set_ylabel('Lucro Total')

        self.canvas.draw()

    def rodar_script(self):
        # Cálculo do Ticket Médio
        ticket_medio = self.dadosProdutos['TvP'].sum() / self.dadosProdutos['quantidade'].sum()
        print(f'\nTicket Médio: R${ticket_medio:.2f}\n')

        # Produtos com Baixa Margem de Lucro
        self.dadosProdutos['margem_lucro'] = (self.dadosProdutos['TvP'] - self.dadosProdutos['custo']) / self.dadosProdutos['TvP']
        produtos_baixa_margem = self.dadosProdutos[self.dadosProdutos['margem_lucro'] < 0.20]
        print('Produtos com Baixa Margem de Lucro:\n', produtos_baixa_margem['produto'])

        # Top 3 Produtos Mais Lucrativos
        self.dadosProdutos['lucro_total'] = (self.dadosProdutos['TvP'] - self.dadosProdutos['custo']) * self.dadosProdutos['quantidade']
        top_3_lucrativos = self.dadosProdutos.nlargest(3, 'lucro_total')
        print('\nTop 3 Produtos Mais Lucrativos:\n', top_3_lucrativos[['produto', 'lucro_total']])

        # Produto mais vendido
        indice = self.dadosProdutos['TvP'].idxmax()
        produto_com_maior = self.dadosProdutos.loc[indice, 'produto']
        q = self.dadosProdutos.loc[indice, 'quantidade']
        p = self.dadosProdutos.loc[indice, 'TvP']

        print('\nProduto com maior Venda:', produto_com_maior, 'com', q, 'unidades vendidas e um valor de R$', p)

        notification.notify(
            title='RELATÓRIO',
            message=f'O item mais vendido é {produto_com_maior}\n com {q} unidades vendidas. \n com um valor de R${p}',
            timeout=10
        )

        relatorio = pd.DataFrame({
            'Produto': [produto_com_maior],
            'Quantidade Vendida': [q],
            'Valor Total': [p]
        })

        with pd.ExcelWriter('relatorio.xlsx', engine='openpyxl') as writer:
            relatorio.to_excel(writer, sheet_name='Resumo', index=False)

        self.envia_email()

    def envia_email(self):
        corpo_email = """
        Olá, boa noite

        Segue o email com o relatório em anexo.
        """

        msg = MIMEMultipart()
        msg['Subject'] = 'Relatório de Vendas'
        msg['From'] = 'scriptvinipython@gmail.com'
        msg['To'] = 'pythonexercicio1907@gmail.com'
        password = 'tvwmwczxeyxxgrsh'  # Substitua pela sua senha

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

    def run_schedule(self):
        schedule.every().day.at("18:51").do(self.rodar_script)

        while True:
            schedule.run_pending()
            time.sleep(5)

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()