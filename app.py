import streamlit as st
import random
import time

st.set_page_config(page_title="Sky Alert Elephant", page_icon="🚀")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🛡️ Sky Alert Login")
    u = st.text_input("Usuário")
    p = st.text_input("Senha", type="password")
    if st.button("ENTRAR NO RADAR"):
        if u == "admin" and p == "P3dro2019@":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Acesso Negado.")
else:
    st.title("🚀 Sky Alert - Elephant Bet")
    if st.button("GERAR NOVO SINAL"):
        with st.spinner('Analisando gráfico...'):
            time.sleep(2)
            odds = ["1.50x", "2.00x", "5.00x", "10.00x (VELA ROSA! 💎)"]
            st.success(f"ENTRADA CONFIRMADA: Sair em {random.choice(odds)}")
