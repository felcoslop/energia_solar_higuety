# Dashboard Energia Solar ⚡

Dashboard interativo para monitoramento de energia solar desenvolvido com Streamlit.

## 📊 Funcionalidades

- Visualização de dados de energia solar
- Filtros por período, ano, CAD e mês
- Gráficos interativos de:
  - Energia mensal
  - Evolução do PR (Performance Ratio)
  - Energia vs Irradiação
  - Série temporal de energia diária
- KPIs principais: Energia Total, PR Médio, Potência Média, Energia Específica Média
- Resumos anuais e mensais

## 🚀 Como executar localmente

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o aplicativo:
```bash
streamlit run app.py
```

## 📁 Estrutura do Projeto

- `app.py` - Aplicação principal Streamlit
- `data_processor.py` - Processamento de dados
- `style.css` - Estilos customizados
- `Monitoramento (1).xlsx` - Dados de entrada
- `requirements.txt` - Dependências do projeto

## 📦 Deploy

Este projeto pode ser facilmente deployado no Streamlit Community Cloud gratuitamente.

## 📝 Licença

MIT
