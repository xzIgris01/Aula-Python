import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

vendas = pd.read_csv('vendas.csv')

quantidade_vendida = vendas.groupby('produto')['quantidade'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x='produto', y='quantidade', data=quantidade_vendida, palette='viridis')

plt.title('Quantidade Vendida por Produto', fontsize=16)
plt.xlabel('Produto', fontsize=12)
plt.ylabel('Quantidade Vendida', fontsize=12)

plt.tight_layout()
plt.savefig('grafico.png')

plt.show()

print('Gráfico gerado e salvo como "grafico.png".')