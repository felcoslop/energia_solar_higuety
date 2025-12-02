import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_processor import load_data
import base64
from pathlib import Path
import os

# Page config
st.set_page_config(
    page_title="Dashboard Energia Solar",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check for required files
REQUIRED_FILES = {
    'excel': 'Monitoramento (1).xlsx',
    'image': 'Gemini_Generated_Image_da229vda229vda22.png',
    'css': 'style.css'
}

missing_files = []
for file_type, file_path in REQUIRED_FILES.items():
    if not os.path.exists(file_path):
        missing_files.append(f"{file_type}: {file_path}")

if missing_files:
    st.error("⚠️ Arquivos necessários não encontrados:")
    for missing in missing_files:
        st.error(f"  - {missing}")
    st.info(f"Diretório atual: {os.getcwd()}")
    st.info(f"Arquivos disponíveis: {os.listdir('.')}")
    st.stop()

# Load background image and convert to base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Erro ao carregar imagem: {e}")
        return ""

# Load CSS with background image
def load_css():
    try:
        bg_image = get_base64_image("Gemini_Generated_Image_da229vda229vda22.png")
        
        with open("style.css", "r") as f:
            css = f.read()
        
        # Replace placeholder with actual base64
        css = css.replace("PLACEHOLDER_BASE64", bg_image)
        
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Erro ao carregar CSS: {e}")

load_css()

# Load data
@st.cache_data
def get_data():
    return load_data("Monitoramento (1).xlsx")

df = get_data()

# Sidebar filters
st.sidebar.title("Filtros")

# Date range filter
if not df.empty:
    min_date = df['Tempo'].min()
    max_date = df['Tempo'].max()
    
    date_range = st.sidebar.date_input(
        "Período",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Year filter
    years = sorted(df['Ano'].unique())
    selected_years = st.sidebar.multiselect(
        "Ano",
        options=years,
        default=years
    )
    
    # CAD filter
    cads = sorted(df['CAD'].unique())
    selected_cads = st.sidebar.multiselect(
        "CAD",
        options=cads,
        default=cads
    )
    
    # Month filter
    months = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    selected_months = st.sidebar.multiselect(
        "Mês",
        options=list(months.keys()),
        format_func=lambda x: months[x],
        default=list(months.keys())
    )
    
    # Apply filters
    df_filtered = df[
        (df['Tempo'] >= pd.to_datetime(date_range[0])) &
        (df['Tempo'] <= pd.to_datetime(date_range[1])) &
        (df['Ano'].isin(selected_years)) &
        (df['Mes'].isin(selected_months)) &
        (df['CAD'].isin(selected_cads))
    ]
else:
    df_filtered = df

# Main content
if not df.empty and 'selected_cads' in locals():
    cad_title = ' + '.join(selected_cads) if selected_cads else 'Todas'
else:
    cad_title = 'Todas'
st.title(f"Dashboard Energia Solar - {cad_title}")

# KPIs
if not df_filtered.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_energia = df_filtered['Energia_kWh'].sum() / 1000  # Convert to MWh
        st.metric("Energia Total", f"{total_energia:.2f} MWh")
    
    with col2:
        pr_medio = df_filtered['PR_Mensal'].mean()
        st.metric("PR Médio", f"{pr_medio:.2%}" if pd.notna(pr_medio) else "N/A")
    
    with col3:
        pot_media = df_filtered['Pot_kWp'].mean()
        st.metric("Potência Média", f"{pot_media:.2f} kWp" if pd.notna(pot_media) else "N/A")
    
    with col4:
        energia_esp_media = df_filtered['Energia_Especifica_kWh_kWp'].mean()
        st.metric("Energia Específica Média", f"{energia_esp_media:.2f} kWh/kWp" if pd.notna(energia_esp_media) else "N/A")
    
    st.markdown("---")
    
    # Annual Summary
    st.header("Resumo Anual")
    
    df_anual = df_filtered.groupby(['Ano', 'CAD']).agg({
        'Energia_kWh': 'sum',
        'PR_Mensal': 'mean',
        'Pot_kWp': 'mean',
        'Energia_Especifica_kWh_kWp': 'mean'
    }).reset_index()
    
    df_anual.columns = ['Ano', 'CAD', 'Energia Total (kWh)', 'PR Médio', 'Potência kWp Média', 'Energia Específica Média']
    
    st.dataframe(
        df_anual, 
        use_container_width=True,
        column_config={
            "PR Médio": st.column_config.NumberColumn(
                "PR Médio",
                format="%.2f%%"
            )
        }
    )
    
    st.markdown("---")
    
    # Monthly Summary
    st.header("Resumo Mensal")
    
    df_mensal = df_filtered.groupby(['Ano', 'Mes', 'CAD']).agg({
        'Energia_kWh': 'sum',
        'PR_Mensal': 'mean',
        'Energia_Especifica_kWh_kWp': 'mean'
    }).reset_index()
    
    df_mensal['Mes_Nome'] = df_mensal['Mes'].map(months)
    df_mensal.columns = ['Ano', 'Mes_Num', 'CAD', 'Energia Total (kWh)', 'PR Médio', 'Energia Específica Média', 'Mês']
    
    st.dataframe(
        df_mensal[['Ano', 'Mês', 'CAD', 'Energia Total (kWh)', 'PR Médio', 'Energia Específica Média']], 
        use_container_width=True,
        column_config={
            "PR Médio": st.column_config.NumberColumn(
                "PR Médio",
                format="%.2f%%"
            )
        }
    )
    
    st.markdown("---")
    
    # Charts
    st.header("Gráficos")
    
    # Monthly Energy Bar Chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Energia Mensal")
        df_mensal['Ano'] = df_mensal['Ano'].astype(str)
fig_mensal = px.bar(
            df_mensal,
            x='Mês',
            y='Energia Total (kWh)',
            color='Ano',
            barmode='group',
            color_discrete_sequence=['#FF8C3B', '#FF4F4F', '#FFB300']
        )
        fig_mensal.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#D3C8E7',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig_mensal.update_traces(marker_line_width=0)
        st.plotly_chart(fig_mensal, use_container_width=True)
    
    with col2:
        st.subheader("Evolução do PR")
        # Convert year to string for proper legend display
        df_mensal_pr = df_mensal.copy()
        df_mensal_pr['Ano'] = df_mensal_pr['Ano'].astype(str)
        
        # Define specific colors for years
        color_map = {
            '2023': '#29B5E8',  # Blue
            '2024': '#9747FF',  # Purple
            '2025': '#FFDD44'   # Yellow (fallback/future)
        }
        
        fig_pr = px.line(
            df_mensal_pr,
            x='Mês',
            y='PR Médio',
            color='Ano',
            markers=True,
            color_discrete_map=color_map
        )
        fig_pr.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#D3C8E7',
            xaxis=dict(showgrid=False),
            yaxis=dict(
                showgrid=True, 
                gridcolor='rgba(255,255,255,0.1)',
                tickformat='.1%'
            ),
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        # Update hover template to show percentage
        fig_pr.update_traces(hovertemplate='Mês=%{x}<br>PR Médio=%{y:.2%}<br>Ano=%{legendgroup}')
        st.plotly_chart(fig_pr, use_container_width=True)
    
    # Daily Energy vs Irradiation Scatter
    st.subheader("Energia Diária vs Irradiação")
    
    df_scatter = df_filtered[
        (df_filtered['Irradiacao_Mensal'].notna()) & 
        (df_filtered['Energia_kWh'].notna())
    ].copy()
    
    if not df_scatter.empty:
        fig_scatter = px.scatter(
            df_scatter,
            x='Irradiacao_Mensal',
            y='Energia_kWh',
            color='Ano',
            hover_data=['Tempo', 'PR_Mensal'],
            color_discrete_sequence=['#FFDD44', '#FF8C3B', '#FF3366']
        )
        fig_scatter.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#D3C8E7',
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title='Irradiação (kWh/m².dia)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title='Energia (kWh)'),
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Dados insuficientes para o gráfico de dispersão.")

    
    # Time series - Daily Energy
    st.subheader("Série Temporal - Energia Diária")
    
    fig_ts = px.area(
        df_filtered,
        x='Tempo',
        y='Energia_kWh',
        color_discrete_sequence=['#FF6A2A']
    )
    fig_ts.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#D3C8E7',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_ts, use_container_width=True)

else:
    st.warning("Nenhum dado disponível para os filtros selecionados.")
