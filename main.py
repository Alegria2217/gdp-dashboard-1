import streamlit as st
import pandas as pd
import openai
import plotly.express as px

# Configura tu clave API de OpenAI
openai.api_key = "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"

# Función para obtener la respuesta de ChatGPT
def obtener_respuesta_chatgpt(pregunta_usuario):
    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Puedes usar "gpt-4" si tienes acceso
        messages=[
            {"role": "system", "content": "Eres un asistente financiero experto."},
            {"role": "user", "content": pregunta_usuario}
        ]
    )
    return respuesta['choices'][0]['message']['content']

# Carga de datos
url = 'https://raw.githubusercontent.com/Alegria2217/gdp-dashboard-1/refs/heads/main/datos_modificados2.csv'
df = pd.read_csv(url)

# Títulos y descripción del dashboard
st.title('Dashboard Financiero Interactivo')
st.markdown("""
Este tablero muestra indicadores financieros clave como el **Ratio de Liquidez**, 
**Ratio Deuda a Patrimonio**, y **Cobertura de Gastos Financieros** para analizar la solvencia de las empresas.
También puedes interactuar con ChatGPT para obtener explicaciones de los resultados.
""")

# Mostrar los datos
st.subheader("Datos cargados:")
st.dataframe(df.head())

# Filtros interactivos
industria = st.selectbox('Selecciona una Industria:', df['Industry'].unique())
tamaño_empresa = st.selectbox('Selecciona el Tamaño de la Empresa:', df['Company_Size'].unique())

# Filtrar los datos según las selecciones del usuario
df_filtrado = df[(df['Industry'] == industria) & (df['Company_Size'] == tamaño_empresa)]

# Visualización de los ratios financieros
st.subheader('Gráficos de Ratios Financieros')

# Ratio de Liquidez
fig_liquidez = px.bar(df_filtrado, x='Company_ID', y='Current_Ratio', 
                      title='Ratio de Liquidez (Activos Circulantes / Pasivos Circulantes)',
                      labels={'Company_ID':'ID de Empresa', 'Current_Ratio':'Ratio de Liquidez'},
                      color='Current_Ratio',
                      color_continuous_scale='Blues')
fig_liquidez.update_layout(font=dict(size=14), title_font=dict(size=20))
st.plotly_chart(fig_liquidez)

# Ratio Deuda a Patrimonio
fig_deuda_patrimonio = px.bar(df_filtrado, x='Company_ID', y='Debt_to_Equity_Ratio', 
                              title='Ratio Deuda a Patrimonio (Deuda Total / Patrimonio Neto)',
                              labels={'Company_ID':'ID de Empresa', 'Debt_to_Equity_Ratio':'Ratio Deuda a Patrimonio'},
                              color='Debt_to_Equity_Ratio',
                              color_continuous_scale='Reds')
fig_deuda_patrimonio.update_layout(font=dict(size=14), title_font=dict(size=20))
st.plotly_chart(fig_deuda_patrimonio)

# Cobertura de Gastos Financieros
fig_cobertura = px.bar(df_filtrado, x='Company_ID', y='Interest_Coverage_Ratio', 
                       title='Cobertura de Gastos Financieros (Ingresos Totales / Gastos Financieros)',
                       labels={'Company_ID':'ID de Empresa', 'Interest_Coverage_Ratio':'Cobertura de Gastos Financieros'},
                       color='Interest_Coverage_Ratio',
                       color_continuous_scale='Greens')
fig_cobertura.update_layout(font=dict(size=14), title_font=dict(size=20))
st.plotly_chart(fig_cobertura)

# Pregunta interactiva a ChatGPT
st.subheader('Consulta a ChatGPT')
pregunta_usuario = st.text_input('Escribe tu pregunta sobre los ratios financieros:')

if st.button('Preguntar'):
    respuesta = obtener_respuesta_chatgpt(pregunta_usuario)
    st.write('Respuesta de ChatGPT:')
    st.write(respuesta)
