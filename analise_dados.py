import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path
import warnings

# Ignorar future warnings do seaborn
warnings.simplefilter(action='ignore', category=FutureWarning)

# Configurar caminhos relativos ao arquivo do script
base_dir = Path(__file__).resolve().parent
data_path = base_dir / "dados_formatados.csv"
output_dir = base_dir / "graficos"
os.makedirs(output_dir, exist_ok=True)

# 1. Carregar os dados
df = pd.read_csv(data_path)

# 2. Limpeza dos dados
def clean_numeric(val):
    if pd.isna(val):
        return np.nan
    if isinstance(val, str):
        val = val.replace(' Mbps', '').replace(' dBm', '').replace(' ms', '').strip()
    try:
        return float(val)
    except:
        return np.nan

df['Velocidade de downlink'] = df['Velocidade de downlink'].apply(clean_numeric)
df['velocidade de uplink'] = df['velocidade de uplink'].apply(clean_numeric)
df['latência'] = df['latência'].apply(clean_numeric)
df['jitter'] = df['jitter'].apply(clean_numeric)
df['sinal'] = df['sinal'].apply(clean_numeric)

# Dropar NaNs apenas nas colunas essenciais para os testes
df_clean = df.dropna(subset=['Velocidade de downlink', 'latência', 'sinal', 'banda', 'Localização'])

# Estilo global dos gráficos
sns.set_theme(style="whitegrid")

print("INICIANDO ANÁLISE ESTATÍSTICA\n" + "="*40 + "\n")

# --- TESTE 1: Intervalo de Confiança (Média ou Proporção) ---
# Média da Velocidade de Downlink
downlink_data = df_clean['Velocidade de downlink']
mean_dl = np.mean(downlink_data)
sem_dl = stats.sem(downlink_data)
ci_dl = stats.t.interval(confidence=0.95, df=len(downlink_data)-1, loc=mean_dl, scale=sem_dl)

print("1. INTERVALO DE CONFIANÇA (MÉDIA DE DOWNLINK)")
print(f"Média: {mean_dl:.2f} Mbps")
print(f"IC 95%: ({ci_dl[0]:.2f}, {ci_dl[1]:.2f})\n")

plt.figure(figsize=(8, 5))
sns.histplot(downlink_data, kde=True, color="skyblue")
plt.axvline(mean_dl, color='red', linestyle='dashed', linewidth=2, label=f'Média: {mean_dl:.1f} Mbps')
plt.axvline(ci_dl[0], color='green', linestyle='dotted', linewidth=2, label='IC 95% Inf')
plt.axvline(ci_dl[1], color='green', linestyle='dotted', linewidth=2, label='IC 95% Sup')
plt.title('Distribuição da Velocidade de Downlink com Intervalo de Confiança')
plt.xlabel('Velocidade de Downlink (Mbps)')
plt.ylabel('Frequência')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '01_downlink_ci.png'))
plt.close()


# --- TESTE 2: Teste de Hipótese com 1 Variável (Latência média > 30ms) ---
# H0: mu = 30 ms
# H1: mu > 30 ms
latency_data = df_clean['latência']
limite_ideal = 30.0
t_stat_1, p_val_1 = stats.ttest_1samp(latency_data, limite_ideal, alternative='greater')

print("2. TESTE DE HIPÓTESE (1 VARIÁVEL) - LATÊNCIA")
print(f"H0: Latência média = {limite_ideal} ms | H1: Latência média > {limite_ideal} ms")
print(f"Média Observada: {np.mean(latency_data):.2f} ms")
print(f"Estatística T: {t_stat_1:.2f}, P-valor: {p_val_1:.4f}")
print("Conclusão: " + ("Rejeitamos H0" if p_val_1 < 0.05 else "Falhamos em rejeitar H0") + "\n")

plt.figure(figsize=(8, 5))
sns.histplot(latency_data, kde=True, color="lightcoral", bins=20)
plt.axvline(np.mean(latency_data), color='darkred', linestyle='dashed', linewidth=2, label=f'Média Obs: {np.mean(latency_data):.1f} ms')
plt.axvline(limite_ideal, color='black', linestyle='solid', linewidth=2, label=f'Limite H0: {limite_ideal} ms')
plt.title('Distribuição da Latência vs Limite Ideal')
plt.xlabel('Latência (ms)')
plt.ylabel('Frequência')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '02_latencia_teste.png'))
plt.close()


# --- TESTE 3: Teste de Hipótese com 2 Variáveis (Downlink 2.4GHz vs 5GHz) ---
dl_24 = df_clean[df_clean['banda'] == '2.4 GHz']['Velocidade de downlink']
dl_5 = df_clean[df_clean['banda'] == '5 GHz']['Velocidade de downlink']
t_stat_2, p_val_2 = stats.ttest_ind(dl_24, dl_5, equal_var=False) # Welch's t-test

print("3. TESTE DE HIPÓTESE (2 VARIÁVEIS) - VELOCIDADE POR BANDA")
print("H0: Não há diferença na velocidade média entre 2.4 GHz e 5 GHz")
print(f"Média 2.4 GHz: {np.mean(dl_24):.2f} Mbps | Média 5 GHz: {np.mean(dl_5):.2f} Mbps")
print(f"Estatística T: {t_stat_2:.2f}, P-valor: {p_val_2:.4f}")
print("Conclusão: " + ("Rejeitamos H0 (Há diferença)" if p_val_2 < 0.05 else "Falhamos em rejeitar H0") + "\n")

plt.figure(figsize=(8, 5))
sns.boxplot(x='banda', y='Velocidade de downlink', data=df_clean, hue='banda', palette="Set2", legend=False)
plt.title('Comparação de Velocidade de Downlink: 2.4 GHz vs 5 GHz')
plt.xlabel('Banda')
plt.ylabel('Velocidade de Downlink (Mbps)')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '03_downlink_boxplot.png'))
plt.close()


# --- TESTE 4a: Teste Qui-Quadrado (Sala/Bloco vs Banda) ---
contingency_sala = pd.crosstab(df_clean['sala'], df_clean['banda'])
chi2_sala, p_val_sala, dof_sala, expected_sala = stats.chi2_contingency(contingency_sala)

print("4a. TESTE QUI-QUADRADO - SALA (BLOCO) vs BANDA")
print("H0: Bloco e Banda são independentes")
print(f"Tabela de contingência:\n{contingency_sala}\n")
print(f"Estatística Qui-Quadrado: {chi2_sala:.2f}, Graus de Liberdade: {dof_sala}, P-valor: {p_val_sala:.4f}")
print("Conclusão: " + ("Rejeitamos H0 (São dependentes)" if p_val_sala < 0.05 else "Falhamos em rejeitar H0 (São independentes)") + "\n")

# Gráfico 1: Countplot
plt.figure(figsize=(8, 5))
sns.countplot(x='sala', hue='banda', data=df_clean, palette="Set2")
plt.title('Distribuição de Redes por Bloco e Banda')
plt.xlabel('Bloco')
plt.ylabel('Quantidade de Medições')
plt.legend(title='Banda')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '04a_sala_banda_countplot.png'))
plt.close()

# Gráfico 2: Heatmap
plt.figure(figsize=(7, 5))
sns.heatmap(contingency_sala, annot=True, fmt='d', cmap='Blues', linewidths=.5, cbar_kws={'label': 'Quantidade de Medições'})
plt.title('Mapa de Calor: Distribuição de Redes (Bloco x Banda)')
plt.xlabel('Banda Wi-Fi')
plt.ylabel('Bloco da Universidade')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '04a_sala_banda_heatmap.png'))
plt.close()


# --- TESTE 4b: Teste Qui-Quadrado (Localização vs Banda) ---
contingency_loc = pd.crosstab(df_clean['Localização'], df_clean['banda'])
chi2_loc, p_val_loc, dof_loc, expected_loc = stats.chi2_contingency(contingency_loc)

# Verificar premissa: células com frequência esperada < 5
celulas_baixas = (expected_loc < 5).sum()
total_celulas = expected_loc.size

print("4b. TESTE QUI-QUADRADO - LOCALIZAÇÃO vs BANDA")
print("H0: Localização e Banda são independentes")
print(f"Estatística Qui-Quadrado: {chi2_loc:.2f}, Graus de Liberdade: {dof_loc}, P-valor: {p_val_loc:.4f}")
print(f"Aviso: {celulas_baixas}/{total_celulas} células com frequência esperada < 5 (premissa violada)")
print("Conclusão: " + ("Rejeitamos H0 (São dependentes)" if p_val_loc < 0.05 else "Falhamos em rejeitar H0 (São independentes)") + "\n")

# Gráfico 1: Countplot
plt.figure(figsize=(10, 15))
sns.countplot(y='Localização', hue='banda', data=df_clean, palette="Pastel1")
plt.title('Distribuição de Redes por Localização e Banda')
plt.ylabel('Localização Específica')
plt.xlabel('Quantidade de Medições')
plt.legend(title='Banda', bbox_to_anchor=(1.0, 1.0), loc='upper right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '04b_localizacao_banda_countplot.png'))
plt.close()

# Gráfico 2: Heatmap
plt.figure(figsize=(10, 15))
sns.heatmap(contingency_loc, annot=True, fmt='d', cmap='Blues', linewidths=.5, cbar_kws={'label': 'Quantidade de Medições'})
plt.title('Mapa de Calor: Distribuição de Redes (Localização x Banda)')
plt.xlabel('Banda Wi-Fi')
plt.ylabel('Localização Específica')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '04b_localizacao_banda_heatmap.png'))
plt.close()

print(f"Análise finalizada! Todos os 7 gráficos foram salvos com sucesso em:\n{output_dir}")