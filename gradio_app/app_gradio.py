from datetime import datetime
import os
import pandas as pd
import gradio as gr

ARQUIVO_CSV = "pacientes.csv"
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]


def carregar_dados():
    """Carrega o histórico existente ou retorna um DataFrame vazio com cabeçalho."""
    if os.path.exists(ARQUIVO_CSV):
        return pd.read_csv(ARQUIVO_CSV).tail(5)
    return pd.DataFrame(columns=COLUNAS)


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    """Valida as entradas, registra a nova linha no CSV local e atualiza o histórico."""
    if not nome or not str(nome).strip():
        return "⚠️ O nome do paciente é obrigatório.", carregar_dados()

    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": str(nome).strip(),
        "idade": int(idade) if idade is not None else 0,
        "convenio": convenio,
        "prioridade": int(prioridade),
        "motivo": motivo,
    }

    novo = pd.DataFrame([linha])

    # Gravação no arquivo local
    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False)

    msg_confirmacao = f"✅ Paciente '{linha['nome']}' cadastrado com sucesso!"
    return msg_confirmacao, pd.read_csv(ARQUIVO_CSV).tail(5)


# Interface usando gr.Blocks com layout em coluna única para telas mobile
with gr.Blocks(title="Cadastro de Pacientes - Recepção") as demo:
    gr.Markdown("## 🩺 Cadastro de Pacientes — Recepção")

    # Coluna única (Vertical) garantindo usabilidade em dispositivos móveis
    with gr.Column():
        nome = gr.Textbox(
            label="Nome do paciente", placeholder="Digite o nome completo"
        )
        idade = gr.Number(label="Idade", value=18, precision=0)
        convenio = gr.Dropdown(
            choices=[
                "Particular",
                "Unimed",
                "Bradesco Saúde",
                "SulAmérica",
                "Outro",
            ],
            label="Convênio",
            value="Particular",
        )
        prioridade = gr.Slider(
            minimum=1,
            maximum=5,
            step=1,
            value=1,
            label="Prioridade do atendimento (1 a 5)",
        )
        motivo = gr.Textbox(
            label="Motivo da consulta / observações",
            lines=3,
            placeholder="Descreva o motivo da consulta ou observações gerais...",
        )

        botao = gr.Button("Cadastrar", variant="primary")

        saida_msg = gr.Textbox(label="Status", interactive=False)
        tabela = gr.Dataframe(
            value=carregar_dados,
            label="Últimos pacientes cadastrados",
            interactive=False,
        )

    # Associação do evento do botão
    botao.click(
        fn=cadastrar_paciente,
        inputs=[nome, idade, convenio, prioridade, motivo],
        outputs=[saida_msg, tabela],
    )

if __name__ == "__main__":
    demo.launch()
