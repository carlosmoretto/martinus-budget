import streamlit as st
import streamlit.components.v1 as components
import time
import jwt

from authentication.login import authenticate, logout

st.set_page_config(layout="wide", page_title="MT-ASSESSORIA - AUTOFLOW", page_icon=":smiley:", initial_sidebar_state="auto")

# Verifica se o usuário está logado
if not st.session_state.get('authenticated', False):
    authenticate()
    st.sidebar.warning("Por favor, faça login para acessar o aplicativo.")
else:
    if st.sidebar.button("Logout"):
        logout()

    user_dict = st.session_state['authenticated']
    def timer():
        if 'time' not in st.session_state:
            st.session_state.time = 0
        st.session_state.time += 1

        if st.session_state.time >= 2400:
            st.warning('ATENÇÃO: Atualize a página para continuar visualizando.', icon="⚠️")

    @st.fragment(run_every=1)
    def show_timer():
        timer()

    show_timer()

    with st.status('Aguarde alguns instantes'):
        st.write("Gerando relatório personalizado....")

        METABASE_SITE_URL = st.secrets.credential.BI_URL
        METABASE_SECRET_KEY = st.secrets.credential.BI_TOKEN

        payload = {
            "resource": {"dashboard": int(user_dict["BI_BUDGET_ID"])},
            "params": {
                "empresa": user_dict["BI_BUDGET_FILTER"]
            },
            "exp": round(time.time()) + (60 * 40) # 10 minute expiration
        }

        token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

        url_to_render = METABASE_SITE_URL + "/embed/dashboard/" + token + "#bordered=true&titled=true"
        components.iframe(url_to_render, height=1200)