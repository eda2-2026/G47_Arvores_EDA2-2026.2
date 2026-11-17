| Identificação | Informação |
|---|---|
| **Nome** | Evellyn de Sousa Rocha |
| **Matrícula** | 202045400 |
| **Grupo** | G47 |
| **Disciplina** | Estruturas de Dados 2 (EDA2) |
| **Instituição** | Universidade de Brasília (UnB) |

---

#  EventTree

**Sistema de Gerenciamento de Eventos com Estruturas de Dados**

Projeto desenvolvido em Python para a disciplina de Estruturas de Dados 2 (EDA2), com o objetivo de aplicar estruturas de dados não lineares no gerenciamento e na organização de eventos, esse é um projeto de verão que eu gostaria dde fazer nas férias e tive a oportunidade de fazer nesta materia

---

##  Sobre o projeto

O EventTree é um sistema que permite cadastrar, consultar, atualizar, listar e remover eventos.

Para organizar e recuperar os dados de maneira eficiente, o projeto utiliza três estruturas de dados implementadas manualmente:

- Min-Heap;
- Árvore AVL;
- Árvore Rubro-Negra.

O sistema também utiliza SQLite para persistência dos dados e Streamlit para disponibilizar uma interface gráfica interativa.

## Funcionalidades

- Cadastro de eventos com identificador, nome, descrição, categoria, local, data, horário e quantidade de vagas.
- Listagem de eventos em ordem cronológica.
- Consulta do próximo evento.
- Busca de eventos pelo identificador.
- Consulta de eventos por intervalo de datas.
- Atualização de eventos cadastrados.
- Remoção de eventos.
- Persistência dos dados em banco SQLite.

##  Estruturas de dados utilizadas

### Min-Heap

Responsável por manter os eventos organizados de acordo com a data e o horário, permitindo consultar eficientemente o próximo evento.

Em caso de empate, o identificador do evento é utilizado como critério secundário.

### Árvore AVL

Utilizada para localizar eventos por identificador.

Seu mecanismo de balanceamento mantém a altura da árvore controlada, favorecendo operações eficientes de busca, inserção e remoção.

### Árvore Rubro-Negra

Responsável por manter os eventos organizados cronologicamente e permitir consultas por intervalo de datas.

O balanceamento por cores garante altura logarítmica da árvore.

## Tecnologias utilizadas

- Python 3
- SQLite
- Streamlit
- Pytest
- Git e GitHub

## Organização do projeto

```text
G47_Arvores_EDA2-2026.2/
│
├── estruturas/
│   ├── __init__.py
│   ├── avl.py
│   ├── heap.py
│   └── rubro_negra.py
│
├── models/
│   └── evento.py
│
├── services/
│   ├── gerenciador_eventos.py
│   └── persistencia.py
│
├── tests/
│   ├── test_avl.py
│   ├── test_heap.py
│   ├── test_rubro_negra.py
│   ├── test_gerenciador.py
│   └── test_persistencia.py
│
├── database/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

##  Instalação e execução

### 1. Clonar o repositório

```bash
git clone https://github.com/eda2-2026/G47_Arvores_EDA2-2026.2.git
```

### 2. Acessar a pasta do projeto

```bash
cd G47_Arvores_EDA2-2026.2
```

### 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Executar a aplicação

```bash
python -m streamlit run app.py
```

O Streamlit disponibilizará um endereço local para acessar o sistema pelo navegador.

##  Testes automatizados

O projeto possui testes automatizados para verificar o funcionamento das estruturas de dados, do gerenciamento de eventos e da persistência SQLite.

Para executar:

```bash
python -m pytest -v
```

**Resultado da última execução:** 23 testes aprovados.

##  Vídeo de apresentação

Neste espaço será disponibilizado o vídeo de apresentação do projeto, demonstrando seu funcionamento, as funcionalidades implementadas e as estruturas de dados utilizadas.

 **Assista à apresentação no YouTube:**

[(https://youtu.be/ZBugSyR1jG0)]




##  Contexto acadêmico

Projeto desenvolvido como atividade acadêmica da disciplina de Estruturas de Dados 2, com foco na implementação prática e na aplicação de estruturas de dados não lineares.

##  Agradecimentos

Agradeço à Inteligência Artificial pelo apoio pontual na compreensão de conceitos, esclarecimento de dúvidas e auxílio na documentação durante o desenvolvimento do projeto.
