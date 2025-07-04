import streamlit as st
import pandas as pd
import numpy as np
import data_loader as dl
import plotly.express as px
import plotly.graph_objects as go
import statsmodels as sm
import matplotlib.pyplot as plt

tab1, tab2, tab3 = st.tabs(["Geral", "Tabela SH4 Description", "Estatísticas"])

file_path = "C:\\project\\streamlit-bitcoin\\data\\exportacoes_franca.csv"

dataset = dl.load_dataset(file_path)


with st.sidebar:
    st.title("DashOrange 🍊")
    cidades_selecionadas = st.multiselect(
        "Faça uma Análise por Cidade:",
        dl.data_proc.list_options_by_dataframe(dataset,'City_State'),
        placeholder='Cidade',
        help="Selecione as cidade corretamente. Caso selecione uma cidade e queira também selecionar um Estado e forem de locais distintos, o filtro não funcionará",
        default=['Águas Mornas - SC','Alfenas - MG']
    )
    estados_selecionados = st.multiselect(
        "Faça uma Análise por Estado:",
        dl.data_proc.list_options_by_dataframe(dataset,'State'),
        help="Caso você tenha selecionado um Estado que não condiz com a cidade selecionada (caso queira analisar por cidade também), os gráficos não serão gerados",
        placeholder="UF",
    )
    anos_selecionados = st.multiselect(
        "Faça uma Análise por Ano:",
        dl.data_proc.list_options_by_dataframe(dataset,'Year'),
        placeholder='Ano',
        help="Selecione um ou mais anos para filtrar os dados. Se nenhum ano for selecionado, todos os anos serão exibidos.",
        default=list(dl.data_proc.list_options_by_dataframe(dataset,'Year'))
    )


df_filtrado = dl.data_proc.columns_selected_by_options(
    dataset,
    cidades_selecionadas,
    estados_selecionados,
    anos_selecionados
    )


with tab1:
    st.title("Dashboard de Exportação para a França 🎲")
    st.write("Na Barra ao lado, selecione as opções e comece a manipular os gráficos")
    # --- Geração do Gráfico ---
    if not df_filtrado.empty:
        exportacoes_ano = df_filtrado.groupby('Year')["US$ FOB"].sum().reset_index() # Reset index para ter 'Year' como coluna

        # Verifica se há dados para plotar após o groupby
        if not exportacoes_ano.empty:
            fig = px.bar(exportacoes_ano,
                         x='Year', # Usar o nome da coluna 'Year'
                         y='US$ FOB', # Usar o nome da coluna 'US$ FOB'
                         title='Exportações realizadas para França em US$ ao longo dos anos',
                         opacity=0.65,
                         text_auto=False) # Desabilitar text_auto para formatar manualmente

            # --- Customizações para um visual mais profissional ---
            fig.update_traces(
                marker_color='#1f77b4', # Cor das barras (um azul padrão do Plotly)
                marker_line_color='rgba(0,0,0,0)', # Remover borda das barras
            )
             # Calcular a média para anotação
            mean_us_fob = exportacoes_ano['US$ FOB'].mean()

            fig.update_layout(
                # template="plotly_dark", # Manter o tema escuro se o Streamlit estiver em modo escuro
                title_font_size=20, # Tamanho da fonte do título
                title_x=0.05, # Alinhar o título à esquerda
                xaxis_title="Ano", # Título do eixo X
                yaxis_title="Valor Exportado (US$)", # Título do eixo Y
                hovermode="x unified", # Melhor experiência de hover
                plot_bgcolor='rgba(0,0,0,0)', # Fundo do gráfico transparente
                paper_bgcolor='rgba(0,0,0,0)', # Fundo do papel transparente
                font=dict(color="white"), # Cor da fonte para todo o gráfico (útil para modo escuro)
                xaxis=dict(
                    showgrid=False, # Remover grade do eixo X
                    tickmode='array', # Garantir que todos os anos apareçam
                    tickvals=exportacoes_ano['Year'],
                    ticktext=[str(year) for year in exportacoes_ano['Year']]
                ),
                yaxis=dict(
                    showgrid=True, # Manter grade do eixo Y
                    gridcolor='#333333', # Cor da grade para modo escuro
                    tickformat='$.2s' # Formato dos ticks do eixo Y (ex: $1B, $2B)
                ),
                # Adicionar anotações para os valores exatos no topo das barras
                annotations=[
                    go.layout.Annotation(
                        x=row['Year'],
                        y=row['US$ FOB'],
                        text=dl.data_proc.format_value_dynamic(row['US$ FOB']),
                        showarrow=False,
                        yshift=10, # Ajuste vertical do texto
                        font=dict(color='#1f77b4',size=18,weight='bold'),
                    ) for index, row in exportacoes_ano.iterrows()
                ]
            )
            
            
            
            # Remover o text_auto do px.bar e adicionar anotações manualmente para maior controle
            fig.update_traces(text=None)

            st.plotly_chart(fig, use_container_width=True) # Use st.plotly_chart para exibir no Streamlit
        else:
            st.warning("Não há dados para exibir os gráficos com os filtros selecionados.")

        # --- Novo Gráfico: Exportações por State ---
        # Agrupa por 'State' e soma 'US$ FOB', depois ordena
        exportacoes_estado = df_filtrado.groupby(['State'])["US$ FOB"].sum().sort_values(ascending=False).reset_index()

        if not exportacoes_estado.empty:
            fig_estado = px.bar(exportacoes_estado, # Renomeei a variável para evitar conflito
                                x='State',
                                y='US$ FOB',
                                title='Total em US$ de Exportações por Estado para França',
                                opacity=0.65,
                                text_auto=False) # Desabilitar text_auto para formatar manualmente

            fig_estado.update_traces(
                marker_color='#374b4a', # Uma cor diferente para este gráfico
                marker_line_color='rgba(0,0,0,0)',
                marker_line_width=0,
                textposition='outside'
            )

            fig_estado.update_layout(
                title_font_size=20,
                title_x=0.05,
                xaxis_title="Estado",
                yaxis_title="Valor Exportado (US$)",
                hovermode="x unified",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="white"),
                xaxis=dict(
                    showgrid=False,
                    tickangle=-45 # Rotacionar rótulos do eixo X para melhor leitura
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#333333',
                    tickformat='$.2s'
                ),
                annotations=[
                    go.layout.Annotation(
                        x=row['State'],
                        y=row['US$ FOB'],
                        text=dl.data_proc.format_value_dynamic(row['US$ FOB']),
                        showarrow=False,
                        yshift=10,
                        font=dict(color='#374b4a', size=14, weight='bold')
                    ) for index, row in exportacoes_estado.iterrows()
                ]
            )
            fig_estado.update_traces(text=None) # Remove text_auto from px.bar

            st.plotly_chart(fig_estado, use_container_width=True)
        else:
            st.warning("Não há dados para exibir os gráficos com os filtros selecionados.")

        # --- Novo Gráfico: Exportações por City ---
        # Agrupa por 'City' e soma 'US$ FOB', depois ordena
        exportacoes_cidade = df_filtrado.groupby(['City'])["US$ FOB"].sum().sort_values(ascending=False).reset_index()

        if not exportacoes_cidade.empty:
            fig_cidade_plot = px.bar(exportacoes_cidade, # Renomeei a variável para evitar conflito
                                     x='City',
                                     y='US$ FOB',
                                     title='Total em US$ para França',
                                     opacity=0.65,
                                     text_auto=False) # Desabilitar text_auto para formatar manualmente

            fig_cidade_plot.update_traces(
                marker_color='#09bc8a', # Uma cor diferente para este gráfico
                marker_line_color='rgba(0,0,0,0)',
                marker_line_width=0,
                textposition='outside'
            )

            fig_cidade_plot.update_layout(
                title_font_size=20,
                title_x=0.05,
                xaxis_title="Cidade", # Alterei de "Estado" para "Cidade" aqui
                yaxis_title="Valor Exportado (US$)",
                hovermode="x unified",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="white"),
                xaxis=dict(
                    showgrid=False,
                    tickangle=-45 # Rotacionar rótulos do eixo X para melhor leitura
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#333333',
                    tickformat='$.2s'
                ),
                annotations=[
                    go.layout.Annotation(
                        x=row['City'],
                        y=row['US$ FOB'],
                        text=dl.data_proc.format_value_dynamic(row['US$ FOB']),
                        showarrow=False,
                        yshift=10,
                        font=dict(color='#09bc8a', size=14, weight='bold')
                    ) for index, row in exportacoes_cidade.iterrows()
                ]
            )
            fig_cidade_plot.update_traces(text=None) # Remove text_auto from px.bar

            st.plotly_chart(fig_cidade_plot, use_container_width=True)
        else:
            st.warning("Não há dados para exibir os gráficos com os filtros selecionados.")


        cidade_itens_por_valor = df_filtrado.groupby(['City', 'SH2 Description'])['US$ FOB'].sum().sort_values(ascending=False).reset_index()


        if not cidade_itens_por_valor.empty:
            fig_heatmap = px.density_heatmap(cidade_itens_por_valor,
                                             x='City',
                                             y='SH2 Description',
                                             z='US$ FOB',
                                             title='US$ FOB por Cidade e Descrição SH2 Description',
                                             color_continuous_scale='Plasma') # Outras opções: 'Viridis', 'Inferno', 'Magma', 'Cividis'

            # Atualiza o layout do gráfico para melhorar a estética e legibilidade.
            fig_heatmap.update_layout(
                title_font_size=20, # Tamanho da fonte do título
                title_x=0.05,       # Posição horizontal do título (0.5 é centralizado)
                xaxis_title="Cidade", # Título do eixo X
                yaxis_title="Descrição", # Título do eixo Y
                hovermode="closest", # Define o modo de exibição do tooltip ao passar o mouse
                plot_bgcolor='rgba(0,0,0,0)', # Fundo do gráfico transparente
                paper_bgcolor='rgba(0,0,0,0)', # Fundo do papel (área ao redor do gráfico) transparente
                xaxis=dict(
                    showgrid=False,     # Não mostra as linhas de grade no eixo X
                    tickangle=-45       # Rotaciona os rótulos do eixo X em -45 graus para evitar sobreposição
                ),
                yaxis=dict(
                    showgrid=True,      # Mostra as linhas de grade no eixo Y
                    tickformat='$.2s'   # Formato dos ticks do eixo Y como moeda simplificada (ex: $100k, $1M)
                )
            )

            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.warning("Não há dados para exibir os gráficos com os filtros selecionados.")

        net_weight_by_dolar = df_filtrado.groupby(['City','State','SH4 Description'])[['US$ FOB','Net Weight']].sum().reset_index()

        if not net_weight_by_dolar.empty:
            
            try:
                fig_net_dolar = px.scatter(
                    net_weight_by_dolar,
                    x="Net Weight",
                    y="US$ FOB",
                    log_x=True,
                    log_y=True,
                    title="Dispersão: Peso Líquido vs. Valor US$ FOB (Escala Log.)",
                    color="Net Weight",
                    )
                fig_net_dolar.update_traces(
                    mode='markers'
                )
                

                st.plotly_chart(fig_net_dolar, use_container_width=True)
            except Exception:
                st.warning("Deu problema!")

        else:
            st.warning("Não há dados para exibir a tabela com os filtros selecionados.")
    else:
        st.warning("Nenhum dado disponível após a aplicação dos filtros. Tente ajustar suas seleções.")

with tab2:
    if not df_filtrado.empty:
            top_produtos_list = df_filtrado.groupby(['City','State','SH4 Description'])['US$ FOB'].sum().sort_values(ascending=False).reset_index()
            top_produtos_list = top_produtos_list.groupby('SH4 Description')['US$ FOB'].sum().sort_values(ascending=False).reset_index()
            top_produtos_list = top_produtos_list[['SH4 Description','US$ FOB']]
            top_produtos_list['US$ FOB'] = top_produtos_list['US$ FOB'].apply(lambda x: f"US$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))


            if not top_produtos_list.empty:

                st.title("SH4 Description Ranking Maiores US$ FOB 🔥")
                qtd_itens = st.slider(
                "Quantidade de Produtos para visualizar:",0,len(top_produtos_list['SH4 Description']))
                st.subheader(f"Top {qtd_itens} itens")
                st.dataframe(top_produtos_list.head(qtd_itens), use_container_width=True) # Adicionado use_container_width aqui


            else:
                st.warning("Não há dados para exibir a tabela com os filtros selecionados.")
    else:
                st.warning("Não há dados para exibir a tabela com os filtros selecionados.")

with tab3:
    st.title("Resumo Estatístico do DataFrame 🧠")
    if not df_filtrado.empty:
        try:
            st.text('Os dados estatísticos do Dataset aparecem de acordo com os filtros aplicados. Para ver a análise geral, remova os filtros.')
            st.dataframe(df_filtrado.describe())
            
            # Criar o histograma com Plotly Express
            fig_histogram = px.histogram(
                df_filtrado,
                x='US$ FOB',
                nbins=30, # Número de bins, similar ao 'bins' do seaborn
                title='Distribuição US$ FOB',
                labels={'US$ FOB': 'US$', 'sum': 'Frequência'}, # Rótulos dos eixos
                color_discrete_sequence=['teal'], # Cor das barras
                opacity=0.7 # Opacidade das barras
            )
            
            # Aplicando escala logarítmica ao eixo Y
            fig_histogram.update_layout(
                yaxis_type="log",
                yaxis_title="Contagem (Escala Logarítmica)"
            )

            # Customizações de layout
            fig_histogram.update_layout(
                xaxis_title='US$ FOB',
                yaxis_title='Frequência',
                title_font_size=18, # Tamanho da fonte do título
                title_x=0.5, # Centraliza o título
                plot_bgcolor='rgba(0,0,0,0)', # Fundo do gráfico transparente
                paper_bgcolor='rgba(0,0,0,0)', # Fundo do papel transparente
                xaxis=dict(
                    showgrid=True, # Mostrar grade no eixo X
                    gridcolor='rgba(200,200,200,0.2)' # Cor da grade
                ),
                yaxis=dict(
                    showgrid=True, # Mostrar grade no eixo Y
                    gridcolor='rgba(200,200,200,0.2)' # Cor da grade
                ),
                bargap=0.05 # Espaçamento entre as barras
            )

            # Adicionar a linha vertical para a média
            fig_histogram.add_vline(
                x=df_filtrado['US$ FOB'].mean(),
                line_color='firebrick',
                line_dash='dash',
                line_width=2,
                annotation_text=f'Média: R${df_filtrado['US$ FOB'].mean():,.2f}', # Texto da anotação
                annotation_position="top right", # Posição do texto (ex: "top right", "top left")
                annotation_font_color="firebrick",
                annotation_font_size=12,
                annotation_bgcolor="rgba(255,255,255,0.8)",
                annotation_bordercolor="firebrick",
                annotation_borderwidth=1,
                annotation_borderpad=2
            )
            
                        # Adicionar a linha vertical para a média
            fig_histogram.add_vline(
                x=df_filtrado['US$ FOB'].median(),
                line_color='firebrick',
                line_dash='dash',
                line_width=2,
                annotation_text=f'Média: R${df_filtrado['US$ FOB'].median():,.2f}', # Texto da anotação
                annotation_position="top left", # Posição do texto (ex: "top right", "top left")
                annotation_font_color="firebrick",
                annotation_font_size=12,
                annotation_bgcolor="rgba(255,255,255,0.8)",
                annotation_bordercolor="firebrick",
                annotation_borderwidth=1,
                annotation_borderpad=2
            )
            
            # Se estiver usando Streamlit, você usaria:
            st.plotly_chart(fig_histogram, use_container_width=True)
            
            
            
            Q1 = df_filtrado['Net Weight'].quantile(0.25)
            Q3 = df_filtrado['Net Weight'].quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            df_filtrado_para_boxplot = df_filtrado[(df_filtrado['Net Weight'] >= lower_bound) & (df_filtrado['Net Weight'] <= upper_bound)].copy()

            # Criando o boxplot
            fig_boxplot = go.Figure()

            fig_boxplot.add_trace(go.Box(
                y=df_filtrado_para_boxplot['Net Weight'],
                name='Peso Líquido',
                boxpoints=False # Não mostrar pontos individuais (outliers já removidos)
            ))

            # Aplicando escala logarítmica ao eixo Y
            fig_boxplot.update_layout(
                title='Boxplot do Peso Líquido (Net Weight) (Outliers Removidos, Escala Logarítmica)',
                yaxis_title='Peso Líquido (Net Weight)',
                yaxis_type='log', # Aplicando escala logarítmica
                yaxis=dict(
                    tickmode='auto', # Permite que Plotly escolha os ticks automaticamente
                    ticks='outside', # Ticks do lado de fora
                    tickfont=dict(size=10) # Tamanho da fonte dos ticks
                ),
                showlegend=False # Não mostrar a legenda
            )

            st.plotly_chart(fig_boxplot, use_container_width=True)            
    
    
        except Exception:
            st.warning("Não há dados para exibir a tabela com os filtros selecionados.")        
    else:
         st.warning("Não há dados para exibir a tabela com os filtros selecionados.")


st.markdown("---")
st.caption("Desenvolvido com Streamlit. Discente: Matheus Naranjo Corrêa")