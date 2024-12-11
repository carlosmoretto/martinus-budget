import streamlit as st

def authenticate():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False  # Inicia com o usuário não autenticado

    with st.sidebar:
        st.header("Login")
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        if st.button("Login"):
            if st.secrets.user.get(username, False) and password == st.secrets.user[username].USER_PASS:  # Verificação simples das credenciais
                st.session_state['authenticated'] = st.secrets.user[username]  # Atualiza o estado da sessão para autenticado
                st.rerun()
                return True
            else:
                st.error("Usuário ou senha incorretos.")
                st.session_state['authenticated'] = False  # Mantém ou define como não autenticado

    return st.session_state['authenticated']

def logout():
    if 'authenticated' in st.session_state:
        del st.session_state['authenticated']  # Remove a informação de autenticação do usuário
        # st.experimental_rerun()  # Reinicia o app para refletir o logout
        st.rerun()  # Reinicia o app para refletir o logout