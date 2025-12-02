# 🚀 Guia de Deploy Gratuito - Streamlit Community Cloud

## ✅ Pré-requisitos

1. Conta no GitHub (gratuita)
2. Conta no Streamlit Community Cloud (gratuita)

---

## 📋 Passo a Passo Completo

### 1️⃣ Criar Repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login (ou crie uma conta)
2. Clique em **"New repository"** (botão verde no canto superior direito)
3. Configure o repositório:
   - **Repository name**: `dashboard-energia-solar` (ou outro nome de sua preferência)
   - **Description**: Dashboard de monitoramento de energia solar
   - **Visibilidade**: **Public** (obrigatório para o plano gratuito do Streamlit Cloud)
   - **NÃO** marque "Add a README file" (já temos um)
4. Clique em **"Create repository"**

### 2️⃣ Subir o Projeto para o GitHub

Abra o terminal/PowerShell na pasta do projeto e execute:

```bash
# Inicializar git (se ainda não foi inicializado)
git init

# Adicionar todos os arquivos
git add .

# Fazer o primeiro commit
git commit -m "Initial commit - Dashboard Energia Solar"

# Conectar com o repositório remoto (SUBSTITUA SEU_USUARIO pelo seu username do GitHub)
git remote add origin https://github.com/SEU_USUARIO/dashboard-energia-solar.git

# Enviar para o GitHub
git branch -M main
git push -u origin main
```

**⚠️ Importante**: Na primeira vez, o Git pedirá suas credenciais do GitHub.

### 3️⃣ Deploy no Streamlit Community Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Clique em **"Sign in with GitHub"** e autorize o acesso
3. Clique em **"New app"**
4. Preencha as informações:
   - **Repository**: Selecione `SEU_USUARIO/dashboard-energia-solar`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Clique em **"Deploy!"**

🎉 **Pronto!** Seu aplicativo estará disponível em alguns minutos em uma URL como:
`https://SEU_USUARIO-dashboard-energia-solar-app-xxxxx.streamlit.app`

---

## 🔄 Atualizações Futuras

Sempre que você quiser atualizar o aplicativo:

```bash
# Fazer alterações nos arquivos
# Depois:

git add .
git commit -m "Descrição das alterações"
git push
```

O Streamlit Cloud detectará automaticamente as mudanças e fará o redeploy!

---

## 🆓 Outras Opções Gratuitas (Alternativas)

### Render
- Site: [render.com](https://render.com)
- Plano gratuito: Sim (com limitações de 750 horas/mês)
- **Processo**: Conecta com GitHub, detecta automaticamente Python, cria web service

### Railway
- Site: [railway.app](https://railway.app)
- Plano gratuito: $5 de créditos/mês
- **Processo**: Similar ao Render, conecta com GitHub

### Hugging Face Spaces
- Site: [huggingface.co/spaces](https://huggingface.co/spaces)
- Plano gratuito: Sim
- **Processo**: Cria um Space tipo "Streamlit", faz upload dos arquivos

---

## ❓ Problemas Comuns

### Erro ao fazer push para o GitHub
- **Solução**: Configure suas credenciais Git:
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

### App não inicia no Streamlit Cloud
- Verifique os logs na dashboard do Streamlit Cloud
- Certifique-se de que todos os arquivos necessários estão no repositório:
  - `app.py`
  - `data_processor.py`
  - `style.css`
  - `requirements.txt`
  - `Monitoramento (1).xlsx`
  - `Gemini_Generated_Image_da229vda229vda22.png`

### Imagem de fundo não aparece
- Verifique se o arquivo `.png` está no repositório
- O arquivo deve ter exatamente o mesmo nome: `Gemini_Generated_Image_da229vda229vda22.png`

---

## 📞 Suporte

- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Community Forum**: [discuss.streamlit.io](https://discuss.streamlit.io)
