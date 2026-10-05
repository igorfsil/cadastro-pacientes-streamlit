from datetime import datetime
import pandas as pd
import streamlit as st

# Configuração da página para layout focado/centralizado (ideal para mobile)
st.set_page_config(
    page_title="Cadastro de Pacientes", page_icon="🩺", layout="centered"
)

st.title("🩺 Cadastro de Pacientes — Recepção")

# Inicialização da estrutura no st.session_state
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]

if "pacientes" not in st.session_state:
    st.session_state.pacientes = pd.DataFrame(columns=COLUNAS)

# Formulario de cadastro
with st.form("cadastro", clear_on_submit=True):
    nome = st.text_input("Nome do paciente*")
    idade = st.number_input(
        "Idade", min_value=0, max_value=120, value=18, step=1
    )
    convenio = st.selectbox(
        "Convênio",
        ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"],
    )
    prioridade = st.slider(
        "Prioridade do atendimento (1 a 5, sendo 5 = Urgente)",
        min_value=1,
        max_value=5,
        value=1,
    )
    motivo = st.text_area("Motivo da consulta / observações")

    enviado = st.form_submit_button("Registrar Paciente")

# Processamento do formulário
if enviado:
    if not nome.strip():
        st.warning("⚠️ O nome do paciente é obrigatório.")
    else:
        nova_linha = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nome": nome.strip(),
            "idade": int(idade),
            "convenio": convenio,
            "prioridade": int(prioridade),
            "motivo": motivo,
        }

        # Concatena o novo registro ao DataFrame na sessão
        st.session_state.pacientes = pd.concat(
            [st.session_state.pacientes, pd.DataFrame([nova_linha])],
            ignore_index=True,
        )
        st.success(f"✅ Paciente '{nome.strip()}' cadastrado com sucesso!")

# Exibição da tabela e exportação de dados
st.divider()
st.subheader("📋 Últimos Cadastros da Sessão")

if not st.session_state.pacientes.empty:
    st.dataframe(
        st.session_state.pacientes.tail(5), use_container_width=True
    )

    # Botão para exportar e baixar os dados gravados na sessão efêmera
    csv_data = st.session_state.pacientes.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Baixar Planilha Completa (CSV)",
        data=csv_data,
        file_name="pacientes.csv",
        mime="text/csv",
        use_container_width=True,
    )
else:
    st.info("Nenhum paciente cadastrado até o momento nesta sessão.")