
import streamlit as st
from datetime import date, datetime, time

from models.evento import Evento
from services.gerenciador_eventos import GerenciadorEventos


st.set_page_config(
    page_title="EventTree",
    page_icon="🌳",
    layout="wide",
)


@st.cache_resource
def obter_gerenciador():
    return GerenciadorEventos()


gerenciador = obter_gerenciador()

st.title("🌳 EventTree")
st.subheader("Sistema de Gerenciamento de Eventos")
st.write(
    "Organize eventos utilizando Min-Heap, Árvore AVL "
    "e Árvore Rubro-Negra."
)

eventos = gerenciador.listar_eventos()
proximo = gerenciador.proximo_evento()

col1, col2, col3 = st.columns(3)
col1.metric("Total de eventos", gerenciador.quantidade())
col2.metric("Próximo evento", proximo.nome if proximo else "Nenhum")
col3.metric(
    "Eventos com vagas",
    sum(1 for evento in eventos if evento.vagas > 0),
)

st.divider()

aba_cadastro, aba_lista, aba_consulta, aba_gerenciar = st.tabs(
    ["Cadastrar evento", "Listar eventos", "Consultar período", "Gerenciar"]
)

with aba_cadastro:
    st.header("Cadastrar novo evento")

    with st.form("form_cadastro"):
        id_evento = st.number_input("ID do evento", min_value=1, step=1)
        nome = st.text_input("Nome do evento")
        descricao = st.text_area("Descrição")
        categoria = st.selectbox(
            "Categoria",
            ["Workshop", "Palestra", "Curso", "Seminário", "Outro"],
        )
        local = st.text_input("Local")
        data_evento = st.date_input("Data", value=date.today())
        hora_evento = st.time_input("Horário", value=time(18, 0))
        vagas = st.number_input("Quantidade de vagas", min_value=0, step=1)

        enviar = st.form_submit_button("Cadastrar evento")

        if enviar:
            if not nome.strip() or not local.strip():
                st.error("Preencha o nome e o local do evento.")
            else:
                try:
                    evento = Evento(
                        id=int(id_evento),
                        nome=nome.strip(),
                        descricao=descricao.strip(),
                        categoria=categoria,
                        local=local.strip(),
                        data_hora=datetime.combine(data_evento, hora_evento),
                        vagas=int(vagas),
                    )
                    gerenciador.cadastrar(evento)
                    st.success("Evento cadastrado com sucesso!")
                    st.rerun()
                except ValueError as erro:
                    st.error(str(erro))

with aba_lista:
    st.header("Eventos cadastrados")

    if eventos:
        for evento in eventos:
            with st.expander(
                f"#{evento.id} - {evento.nome} "
                f"({evento.data_hora.strftime('%d/%m/%Y %H:%M')})"
            ):
                st.write(f"**Descrição:** {evento.descricao}")
                st.write(f"**Categoria:** {evento.categoria}")
                st.write(f"**Local:** {evento.local}")
                st.write(f"**Vagas:** {evento.vagas}")
    else:
        st.info("Nenhum evento cadastrado.")

with aba_consulta:
    st.header("Consultar eventos por período")

    inicio = st.date_input("Data inicial", value=date.today(), key="data_inicio")
    fim = st.date_input("Data final", value=date.today(), key="data_fim")

    if st.button("Consultar período"):
        if inicio > fim:
            st.error("A data inicial não pode ser posterior à final.")
        else:
            resultado = gerenciador.consultar_intervalo(
                datetime.combine(inicio, time.min),
                datetime.combine(fim, time.max),
            )
            if resultado:
                st.success(f"{len(resultado)} evento(s) encontrado(s).")
                for evento in resultado:
                    st.write(
                        f"**{evento.nome}** — "
                        f"{evento.data_hora.strftime('%d/%m/%Y %H:%M')} "
                        f"| {evento.local}"
                    )
            else:
                st.info("Nenhum evento encontrado nesse período.")

with aba_gerenciar:
    st.header("Atualizar ou remover eventos")

    if not eventos:
        st.info("Não existem eventos para gerenciar.")
    else:
        ids = [evento.id for evento in eventos]
        id_selecionado = st.selectbox(
            "Selecione o evento",
            ids,
            format_func=lambda id: next(
                evento.nome for evento in eventos if evento.id == id
            ),
        )

        evento_selecionado = gerenciador.buscar(id_selecionado)

        with st.form("form_atualizar"):
            novo_nome = st.text_input("Nome", value=evento_selecionado.nome)
            nova_descricao = st.text_area(
                "Descrição", value=evento_selecionado.descricao
            )
            categorias = ["Workshop", "Palestra", "Curso", "Seminário", "Outro"]
            nova_categoria = st.selectbox(
                "Categoria",
                categorias,
                index=categorias.index(evento_selecionado.categoria)
                if evento_selecionado.categoria in categorias else 4,
            )
            novo_local = st.text_input("Local", value=evento_selecionado.local)
            nova_data = st.date_input(
                "Data", value=evento_selecionado.data_hora.date()
            )
            nova_hora = st.time_input(
                "Horário", value=evento_selecionado.data_hora.time()
            )
            novas_vagas = st.number_input(
                "Vagas",
                min_value=0,
                value=evento_selecionado.vagas,
                step=1,
            )

            atualizar = st.form_submit_button("Salvar alterações")

            if atualizar:
                if not novo_nome.strip() or not novo_local.strip():
                    st.error("Preencha o nome e o local.")
                else:
                    try:
                        novo_evento = Evento(
                            id=id_selecionado,
                            nome=novo_nome.strip(),
                            descricao=nova_descricao.strip(),
                            categoria=nova_categoria,
                            local=novo_local.strip(),
                            data_hora=datetime.combine(nova_data, nova_hora),
                            vagas=int(novas_vagas),
                        )
                        gerenciador.atualizar(id_selecionado, novo_evento)
                        st.success("Evento atualizado!")
                        st.rerun()
                    except ValueError as erro:
                        st.error(str(erro))

        if st.button("Remover evento selecionado", type="primary"):
            gerenciador.remover(id_selecionado)
            st.success("Evento removido!")
            st.rerun()
