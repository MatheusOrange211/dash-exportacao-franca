import pandas as pd
import streamlit as st
import data_processor as data_proc

@st.cache_data # Cache para evitar recarregar dados a cada interação
def load_dataset(caminho_arquivo):
    """
    Carrega os dados de um arquivo CSV e converte a coluna 'Data' para datetime.
    """
    try:
        df = pd.read_csv(caminho_arquivo)
        if 'Data' in df.columns:
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce') # 'coerce' para lidar com erros
        df = data_proc.clean_dataset(df)
        df['State'] = df['City'].str.split(' - ').str[1]
        df['City_State'] = df['City'].copy()
        df['City'] = df['City'].str.split(' - ').str[0]
        return df
    except FileNotFoundError:
        st.error(f"Erro: Arquivo '{caminho_arquivo}' não encontrado. Verifique o caminho.")
        return pd.DataFrame() # Retorna DataFrame vazio em caso de erro
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

