#---------------------------------------------
#Visão Empresa
#---------------------------------------------
#Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

#Bibliotecas necessárias
import folium
import pandas as pd
import streamlit as st
from PIL import Image

from streamlit_folium import folium_static

import datetime
import datetime as dt
from datetime import datetime
datetime.now()

#---------------------------------------------
#Funções
#---------------------------------------------

def country_maps( df1 ):
        df1_aux = ( df1.loc[:,['City','Road_traffic_density','Delivery_location_latitude', 'Delivery_location_longitude']]
                       .groupby(['City','Road_traffic_density'])
                       .median()
                       .reset_index() )

        map = folium.Map()
        for index, location_info in df1_aux.iterrows():
            folium.Marker([location_info['Delivery_location_latitude'],                                                                        location_info['Delivery_location_longitude']],
                        popup=location_info[['City','Road_traffic_density']]).add_to(map)
        
            folium_static(map, width=1024, height=600)
            
def order_share_by_week( df1 ):
    df1_aux01 = ( df1.loc[:, ['ID', 'week_of_year']]
                     .groupby(['week_of_year'])
                     .count()
                     .reset_index() )
    df1_aux02 = ( df1.loc[:, ['Delivery_person_ID', 'week_of_year']]
                    .groupby('week_of_year')
                    .nunique()
                    .reset_index() )
        
    df1_aux = pd.merge(df1_aux01, df1_aux02, how = 'inner', on='week_of_year')
    df1_aux['order_by_deliver'] = df1_aux['ID'] / df1_aux['Delivery_person_ID']

    #gráfico de linhas
    fig = px.line(df1_aux, x = 'week_of_year', y = 'order_by_deliver')
            
    return fig

def order_by_week( df1 ):
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df1_aux = ( df1.loc[:, ['ID', 'week_of_year']]
                 .groupby('week_of_year')   
                 .count()
                 .reset_index() )

    #gráfico de linhas (line)
    fig = px.line(df1_aux, x='week_of_year', y='ID')
    return fig

def traficc_order_city( df1 ):
    df1_aux = ( df1.loc[:, ['ID', 'City','Road_traffic_density']]
                   .groupby(['City','Road_traffic_density'])
                   .count()
                   .reset_index() )
                
    fig = px.scatter(df1_aux, x ='City', y= 'Road_traffic_density', size = 'ID' , color = 'City')
                
    return fig

def traficc_order_share( df1 ):
    df1_aux = ( df1.loc[:, ['ID', 'Road_traffic_density']]
                   .groupby('Road_traffic_density')
                   .count()
                   .reset_index() )
    
    df1_aux = df1_aux.loc[df1_aux['Road_traffic_density'] != 'NaN ',:]
    df1_aux['entregas_perc'] = df1_aux['ID'] / df1_aux['ID'].sum()  # serve para calcular a porcentagem, sum é para soma a coluna ID
    
    #gráfico de pizza (pie)
    fig = px.pie(df1_aux, values ='entregas_perc', names= 'Road_traffic_density')
               
    return fig

def order_metric( df1 ):
    cols = ['ID', 'Order_Date']
    #Seleção de linhas
    df1_aux = df1.loc[:,cols].groupby('Order_Date').count().reset_index()
    # desenhar o gráfico de barras (bar)
    fig = px.bar(df1_aux, x='Order_Date', y='ID')
    st.plotly_chart(fig, use_container_width=True)
            
    return fig

def clean_code (df1):
    """ Esta função tem a responsabilidade de limpar um dateframe
        
        Tipos de limpeza:
        1. Remoção dos dados NaN
        2. Mudança dos tipos de colunas de dados
        3. Remoção dos espaços das variáveis de texto
        4. Formatação das colunas de datas
        5. Limpeza da coluna de tempo ( remoção do texto da variável numérica )
        
        Input: Dataframe
        Outup: Dataframe
    
    """
    
    #1. Remoção dos NaN
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1['Festival'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    
    #2. Convertendo a coluna Ratings de texto para decimal (float)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    
    #3. Convertendo a coluna Order_date de texto para data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')   
    
    #4. Convertendo multiple_deliveries de texto para número inteiro (int)
    linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    
    #Removendo os espaços dentro das strings/texto/object
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    
    #Limpando coluna time taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min)') [1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)
    
    return df1


#_______________________Início da Estrutura Lógica do Código____________________________________

#_____________________
#Import dataset
#_____________________
df = pd.read_csv('dataset/train.csv')

#_____________________
#Limpeza dos dados
#_____________________
df1 = clean_code(df)

#---------------------------------------------
#Barra lateral
#---------------------------------------------
st.header('Marketplace - Visão Empresa')

image_path = 'logo.png'
image = Image.open(image_path)
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastet Delivey in Town')
st.sidebar.markdown("""___""")

st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider('Até qual valor?', 
                                value=pd.datetime(2022, 4, 13), 
                                min_value=pd.datetime(2022, 2, 11), 
                                max_value=pd.datetime(2022, 4, 6), 
                                format='DD-MM-YYYY')

st.sidebar.markdown("""___""")

traffic_options = st.sidebar.multiselect('Quais as condições do trânsito', ['Low', 'Medium', 'Hight', 'Jam'], default=['Low', 'Medium', 'Hight', 'Jam'])

st.sidebar.markdown("""___""")

#filtro de datas
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

#filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#---------------------------------------------
#Layout do Streamlit
#---------------------------------------------
tab1, tab2, tab3 = st.tabs(['Visão Gerencial','Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        #Order Metric
        #Quantidade de pedidos por semana
        fig = order_metric( df1 )
        st.markdown("# Orders by day")
        st.plotly_chart(fig, use_container_width=True)
        
    with st.container():
        col1, col2 = st.columns( 2 )
        
        with col1:
            fig = traficc_order_share( df1 )
            st.header("Traficc Order Share")
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            fig = traficc_order_city( df1 )
            st.header("Traficc Order City")
            st.plotly_chart(fig, use_container_width=True)
                      
with tab2:
    with st.container():
        st.markdown("# Order by Week")
        fig = order_by_week( df1 )
        st.plotly_chart(fig, use_container_width=True)
    
    with st.container(): 
        st.markdown("# Order Share by Week")
        fig = order_share_by_week( df1 )
        st.plotly_chart(fig, use_container_width=True)
        
with tab3:
    st.header( "Country Maps")
    country_maps( df1 )
    
        
#df1_aux.head()
print('Estou aqui')


