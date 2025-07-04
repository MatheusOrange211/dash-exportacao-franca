import pandas as pd
import streamlit as st


def clean_dataset(df: pd.DataFrame):
    """
    Realiza a limpeza dos dados, removendo linhas em branco. Retorna um pd.Dataframe()
    """
    try:
        if isinstance(df,pd.DataFrame):
            df = df.dropna() #remover linhas em branco
            df = df[df['Economic Block'] !='Europe']
            return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()


def format_value_dynamic(value):
    """
    Formata um valor numérico para K (milhares), M (milhões) ou B (bilhões)
    com 2 casas decimais, dependendo da sua magnitude.
    """
    if abs(value) >= 1e9:  # Bilhões
        return f"${value / 1e9:.2f}B"
    elif abs(value) >= 1e6: # Milhões
        return f"${value / 1e6:.2f}M"
    elif abs(value) >= 1e3: # Milhares
        return f"${value / 1e3:.2f}K"
    else: # Valores menores que mil
        return f"${value:.2f}"


def list_options_by_dataframe(df:pd.DataFrame,col:str):
    """
    Passe o dataframe e o nome da coluna da qual você deseja que retorne uma tupla de opções. Serve para caixas de seleções
    """
    try:
        if isinstance(df, pd.DataFrame):
            if col in df.columns:
                options = tuple(df[col].unique())
                return options
            else:
                print(f"Erro: A coluna '{col}' não existe no DataFrame.")
                return () # Retorna uma tupla vazia se a coluna não for encontrada
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()


def dataset_report(df: pd.DataFrame):
    """
    Esta função gera um print personalizado que rtorna as principais informações do arquivo usado para análises  
    """
    print("--- Dataset Report ---")
    print(f"Número de Linhas: {df.shape[0]}")
    print(f"Número de Colunas: {df.shape[1]}\n")

    # Missing Values
    missing_total = df.isnull().sum().sum()
    print(f"Total de Células Vazias: {missing_total}\n")

    if missing_total > 0:
        # Columns with missing values
        missing_cols = df.isnull().sum()
        missing_cols = missing_cols[missing_cols > 0].sort_values(ascending=False)
        if not missing_cols.empty:
            print("Colunas com Valores Vazios:")
            for col, count in missing_cols.items():
                print(f"  - {col}: {count} valores vazios ({count/df.shape[0]:.2%})")
            print("")

        # Rows with missing values
        rows_with_missing = df[df.isnull().any(axis=1)]
        if not rows_with_missing.empty:
            print(f"Linhas com Valores Vazios: {rows_with_missing.shape[0]}")            
    else:
        print("Não há valores vazios no dataset.\n")


    # Data Types
    print("Tipos de Dados por Coluna:")
    for col, dtype in df.dtypes.items():
        print(f"  - {col}: {dtype}")
    print("")

    # Memory Usage
    mem_usage = df.memory_usage(deep=True).sum()
    print(f"Tamanho do Dataset (Uso de Memória): {mem_usage / (1024**2):.2f} MB")
    print("--------------------")


def columns_selected_by_options(df: pd.DataFrame, cidades_selecionadas: list, estados_selecionados: list, anos_selecionados: list):
    """
    Filtra o DataFrame com base nas seleções de cidade, estado e ano.
    Se uma lista de seleção estiver vazia, nenhum filtro é aplicado para aquela categoria.
    """
    df_filtrado = df.copy()

    if cidades_selecionadas:
        df_filtrado = df_filtrado[df_filtrado['City_State'].isin(cidades_selecionadas)]

    if estados_selecionados:
        df_filtrado = df_filtrado[df_filtrado['State'].isin(estados_selecionados)]

    if anos_selecionados:
        df_filtrado = df_filtrado[df_filtrado['Year'].isin(anos_selecionados)]

    return df_filtrado
