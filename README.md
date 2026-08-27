# Análise de Dados da Rede Wi-Fi (UFCA)

Este projeto contém um script Python (`analise_dados.py`) desenvolvido para um **trabalho de introdução à análise de dados**. O objetivo principal do script é realizar a limpeza de dados coletados sobre a rede Wi-Fi da universidade e aplicar testes estatísticos básicos para extrair insights sobre a qualidade da conexão (velocidade, latência, sinal, etc.).

## O que o código faz?

O script está dividido nas seguintes etapas principais:

### 1. Carregamento e Limpeza dos Dados
- O código lê um arquivo de dados local chamado `dados_formatados.csv`.
- **Limpeza:** Várias colunas contêm texto junto com os números (como " Mbps", " dBm", " ms"). O script possui uma função dedicada para remover esses textos e converter os valores para números (formato *float*), permitindo cálculos matemáticos.
- Valores nulos ou inválidos nas colunas essenciais são removidos (processo de *dropna*).

### 2. Análises Estatísticas
O script executa quatro testes estatísticos diferentes, fundamentais para a análise de dados:

1. **Intervalo de Confiança (Média de Downlink):**
   - Calcula a média da velocidade de download da rede.
   - Determina um intervalo de confiança de 95% para essa média, ou seja, a faixa de valores onde a verdadeira média da população tem 95% de chance de estar.

2. **Teste de Hipótese com 1 Variável (Latência):**
   - Verifica se a latência (atraso na rede) média é superior a um limite aceitável de 30 ms.
   - **H0 (Hipótese Nula):** A latência média é igual a 30 ms.
   - **H1 (Hipótese Alternativa):** A latência média é maior que 30 ms.

3. **Teste de Hipótese com 2 Variáveis (Velocidade por Banda):**
   - Compara as velocidades de download entre as redes de **2.4 GHz** e **5 GHz**.
   - Usa o *Welch's t-test* para verificar se há uma diferença estatisticamente significativa na velocidade média entre as duas tecnologias.

4. **Teste Qui-Quadrado (Independência):**
   - Testa se existe dependência entre variáveis categóricas.
   - **Teste A:** Analisa a relação entre o Bloco (sala) e a Banda Wi-Fi utilizada (2.4 GHz ou 5 GHz).
   - **Teste B:** Analisa a relação entre a Localização específica e a Banda Wi-Fi.

### 3. Visualização de Dados (Gráficos)
Para cada análise, o código gera visualizações para facilitar a interpretação. Ao todo, são gerados e salvos **7 gráficos** em uma nova pasta chamada `graficos`:
- Histogramas com as distribuições e médias.
- *Boxplots* para comparar as velocidades entre as bandas.
- *Countplots* (gráficos de barras) e *Heatmaps* (mapas de calor) para visualizar a distribuição das redes por blocos e localizações.

## Pré-requisitos

Para rodar este script, você precisará ter o Python instalado junto com as seguintes bibliotecas de análise de dados:

```bash
pip install pandas numpy scipy matplotlib seaborn
```

## Como executar

1. Certifique-se de que o arquivo `dados_formatados.csv` está na mesma pasta que o script.
2. Execute o arquivo Python no seu terminal ou ambiente de desenvolvimento (IDE):

```bash
python analise_dados.py
```

3. Os resultados dos testes estatísticos serão impressos no terminal.
4. Os gráficos gerados estarão disponíveis na pasta `graficos`, que será criada automaticamente na mesma pasta do script.

## Integrantes da equipe

- [A](https://github.com/AndreLucas23)
- [K](https://github.com/Kayky-MM)
- [M](https://github.com/MarcusVentura14)
- [Rodrigo Pinheiro Alcantara](https://github.com/rodrigop07)