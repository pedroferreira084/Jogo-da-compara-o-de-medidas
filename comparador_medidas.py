import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# Função para gerar novas medidas
def gerar_novas_medidas():
    st.session_state.A, st.session_state.erro_A, st.session_state.B, st.session_state.erro_B = gerar_medidas_balanceadas()
    st.session_state.contador += 1  # força nova chave
    if 'resposta' in st.session_state:
        del st.session_state['resposta']
    st.rerun()

def gerar_medidas_balanceadas():
    caso = random.choice(['A > B', 'A < B', 'compatíveis'])

    erro_A = np.round(np.random.uniform(0.1, 0.5), 1)
    erro_B = np.round(np.random.uniform(0.1, 0.5), 1)

    if caso == 'A > B':
        B = np.round(np.random.uniform(1, 9), 1)
        A = np.round(B + erro_A + erro_B + np.random.uniform(0.1, 0.5), 1)

    elif caso == 'A < B':
        A = np.round(np.random.uniform(1, 9), 1)
        B = np.round(A + erro_A + erro_B + np.random.uniform(0.1, 0.5), 1)

    else:  # compatíveis
        base = np.round(np.random.uniform(1, 10), 1)
        desvio = np.round(np.random.uniform(-0.5, 0.5), 1)
        A = base + desvio
        B = base - desvio
        A = np.round(A, 2)
        B = np.round(B, 2)

    return A, erro_A, B, erro_B

# titulo e botao de reset
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("## Comparador de Medidas")
with col2:
    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Gerar novas medidas", key="botao_reset"):
        gerar_novas_medidas()

if 'contador' not in st.session_state:
    st.session_state.contador = 0




# Inicializa medidas se ainda não existem
if 'A' not in st.session_state:
    gerar_novas_medidas()

# Recupera as medidas
A = st.session_state.A
erro_A = st.session_state.erro_A
B = st.session_state.B
erro_B = st.session_state.erro_B

# Exibe as medidas
st.write(f"### A = **({A} ± {erro_A})** e B = **({B} ± {erro_B})**")
#st.write(f"### B = **({B} ± {erro_B})**")

# Pergunta ao usuário
resposta = st.radio(
    "Qual das opções é correta?",
    ["A > B", "A < B", "A e B são compatíveis"],
    index=None,
    key=f"resposta_{st.session_state.contador}") #, horizontal=True)


# Avaliação da resposta
mensagem = st.empty()
if resposta:
    dif = abs(A - B)
    desvio_comb = abs(erro_A) + abs(erro_B)

    if dif > desvio_comb and not np.isclose(dif, desvio_comb):
        correta = "A > B" if A > B else "A < B"
    else:
        correta = "A e B são compatíveis"

    if resposta == correta:
        mensagem.success("✅ Resposta correta!")
    else:
        mensagem.error(f"❌ Resposta incorreta. A opção correta era: **{correta}**")
else:
    # Deixa o espaço reservado do mesmo tamanho, com um texto invisível
    mensagem.markdown("<div style='height:72px'></div>", unsafe_allow_html=True)


# Gráfico com barras de erro
mostrar_grafico = st.button("Mostrar Gráfico")
if mostrar_grafico:
    plt.figure(figsize=(3, 1))
    plt.errorbar(1.4, A, yerr=erro_A, fmt='o', label="A", capsize=5)
    plt.errorbar(1.6, B, yerr=erro_B, fmt='o', label="B", capsize=5)
    plt.xlim(1.2, 1.7)
    plt.xticks([1.4, 1.6], ['A', 'B'])
    plt.ylabel("Valor")
    #plt.title("Gráfico das Medidas com Incerteza", fontsize=10)
    plt.grid(True)
    plt.legend(loc='center left')
    st.pyplot(plt)
