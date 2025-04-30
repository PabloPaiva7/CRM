import streamlit as st
import pandas as pd
import os

# 📁 Configurações
ARQUIVO = 'clientes.csv'
CAMPOS = ['ID', 'Nome', 'Email', 'Telefone', 'Status']

# 🛠️ Utilitários
def inicializar_arquivo():
    if not os.path.exists(ARQUIVO):
        pd.DataFrame(columns=CAMPOS).to_csv(ARQUIVO, index=False)

def carregar_dados():
    return pd.read_csv(ARQUIVO)

def salvar_dados(df):
    df.to_csv(ARQUIVO, index=False)

def gerar_novo_id(df):
    if df.empty:
        return '1'
    return str(int(df['ID'].max()) + 1)

# 🚀 App Streamlit
def main():
    st.set_page_config(page_title="CRM Simples", layout="centered")
    st.title("📋 CRM - Gestão de Clientes")
    inicializar_arquivo()
    df = carregar_dados()

    menu = st.sidebar.radio("Navegação", ["📄 Listar", "➕ Adicionar", "✏️ Atualizar", "❌ Remover"])

    if menu == "📄 Listar":
        st.subheader("📋 Lista de Clientes")
        if df.empty:
            st.warning("Nenhum cliente cadastrado.")
        else:
            st.dataframe(df, use_container_width=True)

    elif menu == "➕ Adicionar":
        st.subheader("➕ Adicionar Cliente")
        with st.form("form_add"):
            nome = st.text_input("Nome completo")
            email = st.text_input("Email")
            telefone = st.text_input("Telefone")
            status = st.selectbox("Status", ["Ativo", "Inativo"])
            submitted = st.form_submit_button("Salvar")
            if submitted:
                if nome and email:
                    novo_id = gerar_novo_id(df)
                    novo = pd.DataFrame([[novo_id, nome, email, telefone, status]], columns=CAMPOS)
                    df = pd.concat([df, novo], ignore_index=True)
                    salvar_dados(df)
                    st.success("✅ Cliente adicionado com sucesso.")
                else:
                    st.error("Nome e Email são obrigatórios.")

    elif menu == "✏️ Atualizar":
        st.subheader("✏️ Atualizar Cliente")
        if df.empty:
            st.info("Nenhum cliente cadastrado.")
        else:
            cliente_id = st.selectbox("Selecione o ID do cliente", df['ID'])
            cliente = df[df['ID'] == cliente_id].iloc[0]

            with st.form("form_update"):
                nome = st.text_input("Nome", cliente['Nome'])
                email = st.text_input("Email", cliente['Email'])
                telefone = st.text_input("Telefone", cliente['Telefone'])
                status = st.selectbox("Status", ["Ativo", "Inativo"], index=["Ativo", "Inativo"].index(cliente['Status']))
                submitted = st.form_submit_button("Atualizar")

                if submitted:
                    df.loc[df['ID'] == cliente_id, ['Nome', 'Email', 'Telefone', 'Status']] = [nome, email, telefone, status]
                    salvar_dados(df)
                    st.success("✅ Cliente atualizado com sucesso.")

    elif menu == "❌ Remover":
        st.subheader("❌ Remover Cliente")
        if df.empty:
            st.info("Nenhum cliente cadastrado.")
        else:
            cliente_id = st.selectbox("Selecione o ID para remoção", df['ID'])
            cliente = df[df['ID'] == cliente_id].iloc[0]
            st.write(f"🧍 Nome: **{cliente['Nome']}**")
            if st.button("Remover Cliente"):
                df = df[df['ID'] != cliente_id]
                salvar_dados(df)
                st.success("✅ Cliente removido com sucesso.")

if __name__ == '__main__':
    main()
