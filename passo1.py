import pandas as pd
import time
from plyer import notification

#parte 1
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


    