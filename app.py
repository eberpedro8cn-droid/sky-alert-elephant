import streamlit as st
import random
import time
import pandas as pd
import gspread

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Sky Alert Elephant", page_icon="🐘", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffcc00; }
    div.stButton > button:first-child {
        background-color: #ffcc00; color: black; border: none;
        border-radius: 10px; width: 100%; height: 3.5em; font-weight: bold; font-size: 18px;
    }
    .signal-box {
        padding: 15px; border: 3px solid #ffcc00; border-radius: 20px; 
        text-align: center; background-color: #1a1a1a; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM A PLANILHA ---
def conecta_bd():
    try:
        credentials = st.secrets["gspread_credentials"]
        gc = gspread.service_account_from_dict(credentials)
        sh = gc.open("BD_SkyAlert") 
        return sh.sheet1
    except:
        return None

wks = conecta_bd()

# --- ESTADO DA SESSÃO ---
if 'logado' not in st.session_state:
    st.session_state['logado'] = False
if 'eh_admin' not in st.session_state:
    st.session_state['eh_admin'] = False

# --- TELA DE LOGIN / ADMIN ---
if not st.session_state['logado']:
    st.image("https://www.elephantbet.co.ao/assets/images/logo.png", width=180)
    st.title("🐘 SKY ALERT - ACESSO")
    
    aba1, aba2 = st.tabs(["Ativar Chave VIP 🔑", "Acesso Admin ⚙️"])
    
    with aba1:
        chave_input = st.text_input("Sua Chave VIP", placeholder="SA-XXXX-XXXX")
        if st.button("ATIVAR AGORA 🚀"):
            if wks:
                try:
                    registro = wks.find(chave_input)
                    if registro:
                        status = wks.cell(registro.row, 3).value
                        if status == 'ativa':
                            wks.update_cell(registro.row, 3, 'usada') 
                            st.session_state['logado'] = True
                            st.rerun()
                        else:
                            st.error("Chave já utilizada!")
                    else:
                        st.error("Chave inválida!")
                except:
                    st.error("Erro ao validar.")
            else:
                st.error("Erro no Banco de Dados. Verifique os Secrets.")

    with aba2:
        user_admin = st.text_input("Usuário Admin")
        pass_admin = st.text_input("Senha Admin", type="password")
        if st.button("ENTRAR COMO DONO 👑"):
            if user_admin == "admin" and pass_admin == "P3dro2019@": 
                st.session_state['eh_admin'] = True
                st.session_state['logado'] = True
                st.rerun()
            else:
                st.error("Acesso Negado.")

# --- PAINEL DO ADMIN (GERAR CHAVES) ---
elif st.session_state['eh_admin']:
    st.title("👑 PAINEL DO DONO")
    if st.button("SAIR"):
        st.session_state['logado'] = False
        st.session_state['eh_admin'] = False
        st.rerun()

    st.subheader("Gerar Novas Chaves VIP")
    qtd = st.number_input("Quantidade", min_value=1, max_value=20, value=1)
    if st.button("GERAR E SALVAR NA PLANILHA ✨"):
        novas = []
        for _ in range(qtd):
            token = f"SA-{random.randint(1000,9999)}-{random.randint(1000,9999)}"
            novas.append([token, "30", "ativa"])
        if wks:
            wks.append_rows(novas)
            st.success("Gerado com sucesso!")
            st.code("\n".join([c[0] for c in novas]))

# --- PAINEL DO CLIENTE (SINAIS) ---
else:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.header("🐘 Sky Alert")
        if st.button("🚀 GERAR SINAL"):
            st.markdown(f'<div class="signal-box"><h2>SINAL: {random.choice(["1.50x", "2.00x", "5.00x"])}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.components.v1.iframe("https://www.elephantbet.co.ao/games/aviatrix", height=600)
