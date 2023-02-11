import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    #page-icon=" "
)

#image_path = 'C:\Users\waldi\OneDrive\Documentos\repos_ftc'
image = Image.open('logo.png')
st.sidebar.image( image, width=120 )

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )

st.write('# Curry Company Growth Dashboard')

st.markdown(
    """
    Growth Daschboard foi construido para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    
    Como utilizar o Growth Daschboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de investimento.
        - Visão Geográfica: Insigths de Geolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento.
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes.
    ### Ask for Help
    - Time de Data Science no Discord
        - @meigarom
    """ )


