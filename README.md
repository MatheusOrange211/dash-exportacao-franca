﻿# Dashboard de Exportação para a França 🎲
# 🥐🥐 Dashboard de Análise de Exportações para a França 🥐🥐

Este projeto apresenta um dashboard interativo desenvolvido com **Streamlit** para visualização e análise de dados de exportações brasileiras com destino à França. O objetivo é fornecer insights rápidos sobre padrões de exportação, valores FOB, pesos líquidos e a evolução ao longo dos anos, permitindo filtrar por cidade, estado e ano.

---

## 🚀 Funcionalidades Principais

O dashboard oferece as seguintes análises e visualizações:

* **Visão Geral das Exportações:**
    * Gráfico de barras mostrando o valor total exportado (US$ FOB) para a França ao longo dos anos.
    * Filtros interativos por Cidade, Estado (UF) e Ano para granularidade da análise.
    * Exemplo: Total exportado para a França em US$ ao longo dos anos (2016-2020).

* **Análise por Cidade e Descrição (SH2 Description):**
    * Heatmap que correlaciona o valor US$ FOB exportado por cidade e a descrição do produto (SH2 Description), permitindo identificar quais produtos são mais exportados de determinadas cidades.
    * Exemplo: Análise de "Fish and crustaceans, molluscs" vs "Coffee, tea, maté and spices" por "Alfenas" e "Águas Mornas".

* **Distribuição de Valores US$ FOB:**
    * Histograma que mostra a frequência da distribuição dos valores US$ FOB das exportações, com indicação das médias.
    * Boxplot do Peso Líquido (Net Weight) com outliers removidos e em escala logarítmica, para entender a distribuição dos pesos das mercadorias exportadas.

* **Ranking de Produtos Exportados (SH4 Description):**
    * Tabela de ranking dos produtos mais exportados (SH4 Description) com base no valor US$ FOB, permitindo visualizar os principais itens em destaque.
    * Controle deslizante para ajustar a quantidade de produtos a serem exibidos no ranking.

* **Resumo Estatístico do DataFrame:**
    * Tabela com estatísticas descritivas (contagem, média, desvio padrão, mínimo, quartis e máximo) para as colunas numéricas do dataset, fornecendo um panorama estatístico dos dados filtrados.
    * Útil para uma visão rápida sobre a magnitude e variabilidade dos dados.

---

## 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem de programação principal.
* **Streamlit:** Framework para criação de aplicações web interativas e dashboards.
* **Pandas:** Manipulação e análise de dados.
* **Plotly / Matplotlib / Seaborn (ou similar):** Para criação dos gráficos e visualizações.
* **Git LFS:** Utilizado para gerenciar a base de dados de exportação de 70MB de forma eficiente no repositório.

---

## ⚙️ Como Rodar o Projeto Localmente

Siga os passos abaixo para configurar e executar o dashboard em sua máquina:

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git](https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git)
    cd SEU-REPOSITORIO
    ```
    * **Lembre-se de substituir `SEU-USUARIO` e `SEU-REPOSITORIO` pelos seus dados reais.**

2.  **Instale o Git LFS (se ainda não tiver):**
    Se você planeja lidar com a base de dados grande, certifique-se de ter o Git LFS instalado.
    [Instruções de instalação do Git LFS](https://git-lfs.com/)
    Após instalar, execute:
    ```bash
    git lfs install
    ```
    Isso garantirá que a base de dados de 70MB seja baixada corretamente.

3.  **Crie e Ative um Ambiente Virtual (Recomendado):**
    É uma boa prática criar um ambiente virtual para gerenciar as dependências do projeto.
    ```bash
    python -m venv venv
    # No Windows
    .\venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

4.  **Instale as Dependências:**
    Assumindo que você tem um arquivo `requirements.txt` com todas as dependências:
    ```bash
    pip install -r requirements.txt
    ```
    (Se você não tiver, crie um com `pip freeze > requirements.txt` após instalar Streamlit, pandas, plotly, etc.)

5.  **Execute o Dashboard:**
    ```bash
    streamlit run app.py
    ```
    O dashboard será aberto automaticamente no seu navegador padrão.

---

## 📂 Estrutura do Projeto

* `app.py`: O arquivo principal do Streamlit que contém a lógica do dashboard e a interface do usuário.
* `data_loader.py`: Script responsável por carregar e pré-processar a base de dados.
* `data_processor.py`: Script que contém funções para o processamento e transformação dos dados para as visualizações.
* `data/`: Pasta contendo a base de dados original (`exportacoes_franca.csv` - gerenciado via Git LFS).
* `heatmap_cidade_items_por_valor_refactored.json`: (Se for um arquivo gerado) Pode ser um arquivo de cache ou pré-processamento para o heatmap.
* `.gitattributes`: Arquivo de configuração do Git LFS.
* `README.md`: Este arquivo.

---

## 🤝 Contribuições

Contribuições são bem-vindas! Se você tiver sugestões, melhorias ou encontrar algum problema, sinta-se à vontade para abrir uma issue ou enviar um Pull Request.

---

