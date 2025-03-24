import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog, messagebox

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
        ax.bar(top_3_lucrativos['produto'], top_3_lucrativos['lucro_total'], color='blue')
        ax.set_title('Top 3 Produtos Mais Lucrativos')
        ax.set_xlabel('Produtos')
        ax.set_ylabel('Lucro Total')

        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()