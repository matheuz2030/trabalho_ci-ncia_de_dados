# 📊 Trabalho 4 – Análise de Demanda do Vestibular FATEC
### 📍 Estudo de Caso Estratificado: São José do Rio Preto (~480 mil habitantes)

> **Apresentação:** 09/11  
> **Objetivo:** Definir e justificar a abertura de **1 curso por período** (Manhã, Tarde e Noite) com base no histórico oficial de demanda dos Vestibulares FATEC (2022.1 a 2024.2), estratificado pelo porte populacional de **São José do Rio Preto (~480k hab.)** e comparado com outras faixas do estado de SP.

---

## 🎯 1. Decisão Recomendada para São José do Rio Preto (~480k hab.)

São José do Rio Preto possui aproximadamente **480.000 habitantes** (Censo IBGE), enquadrando-se perfeitamente na aba **"200 a 600"** e **"Até 500"** da planilha do vestibular:

| Período | Curso Escolhido | Demanda Média Rio Preto (200k-600k) | Demanda Geral (Todos) | Motivo da Escolha (Justificativa Estratégica) |
| :--- | :--- | :---: | :---: | :--- |
| 🌅 **Manhã** | **Desenvolvimento de Software Multiplataforma (DSM)** *(ou GTI)* | **2,82** C/V *(GTI: 4,77)* | **3,21** C/V | **100% de Sinergia de Laboratórios:** Rio Preto é um polo de comércio, serviços médicos e tecnologia. Alocar DSM de manhã aproveita integralmente os laboratórios de informática montados para o período noturno de ADS, reduzindo o custo de implantação da turma a quase zero. |
| ☀️ **Tarde** | **Gestão Empresarial** *(ou DSM Vespertino)* | **1,78** C/V *(Pico 2,35)* | **1,83** C/V | **Proteção do Turno Mais Crítico:** A tarde é o período mais vulnerável a turmas vazias e evasão escolar (apenas 20 cursos da FATEC operam à tarde). Gestão Empresarial apresenta demanda sólida com aceleração recente e atende o forte setor de comércio e serviços de Rio Preto. |
| 🌙 **Noite** | **Análise e Desenvolvimento de Sistemas (ADS)** | **11,61** C/V *(Pico 14,01)* | **9,90** C/V | **Demanda Explosiva na Faixa de Rio Preto:** Em cidades médias-grandes como Rio Preto (200k-600k), a procura por ADS Noite explode para **11,61 C/V** (pico de 14,01 C/V), garantindo concorrência recorde e preenchimento total de vagas. |

---

## 🏢 2. Comparativo por Porte Populacional (Planilha FATEC)

A planilha original do professor possui abas divididas por faixas populacionais. O impacto do porte da cidade na demanda é nítido:

```
+----------------------------------------------------------------------------------------------------+
| PORTE DA CIDADE          | MANHÃ                           | TARDE                     | NOITE     |
+----------------------------------------------------------------------------------------------------+
| 📍 Rio Preto (200k-600k) | ADS (4,91) / GTI (4,77) / DSM (2,82) | ADS (4,90) / DSM (2,82) / Gestão (1,78) | ADS (11,61) / GTI (6,01)  |
| 🏙️ Até 500 mil hab.      | ADS (4,00) / GTI (3,13)         | ADS (3,81) / Gestão (1,89)| ADS (8,20) / Banco Dados (5,45)   |
| 🌾 Até 200 mil hab.      | ADS (2,51) / Mecanização (2,40) | Big Data Agro (1,96)      | ADS (4,50) / Mecanização (4,38)   |
| 🚜 Até 100 mil hab.      | ADS (2,51) / Mecanização (2,40) | Big Data Agro (1,96)      | ADS (4,50) / Mecanização (4,38)   |
| 🌐 Todos (Estado Geral)  | ADS (5,16) / DSM (3,21)         | ADS (4,23) / DSM (2,36)   | ADS (9,90) / Mídias Dig. (6,72)   |
+----------------------------------------------------------------------------------------------------+
```

* **Cidades Pequenas (< 200k hab.):** Vocação voltada ao campo. Cursos como **Mecanização em Agricultura de Precisão** (4,38 C/V à noite) e **Big Data no Agronegócio** (1,96 C/V à tarde) disputam diretamente com TI.
* **Cidades do Porte de Rio Preto (200k a 600k hab.):** Polo de serviços terciários e medicina, onde **ADS** (11,61 C/V à noite) e **DSM/GTI** dominam a procura.

---

## 📚 3. Dicionário de Indicadores: O que significa C/V, Qtd e Sazonalidade?

### 🎯 O que é C/V (Candidatos por Vaga)?
É a relação matemática oficial de concorrência do vestibular:
$$\text{C/V} = \frac{\text{Número Total de Candidatos Inscritos}}{\text{Número de Vagas Oferecidas na Turma}}$$

* **Exemplo em São José do Rio Preto:** Para 40 vagas de **ADS Noite**, com **11,61 C/V**, inscrevem-se **464 candidatos** disputando aquelas 40 carteiras.
* **Interpretação para Gestão Escolar:**
  * $\text{C/V} > 1,5$: Turma autossustentável (preenchimento total sem risco de vagas ociosas).
  * $\text{C/V} > 3,0$: Curso de alta concorrência e prestígio regional.
  * $\text{C/V} > 10,0$: Concorrência extrema (nível de vestibulares disputados de universidades públicas).
  * $\text{C/V} < 1,2$: Faixa de alerta institucional de fechamento de turma.

### 🏫 O que é Qtd (Escala / Unidades Ofertantes)?
Indica quantas faculdades FATEC mantêm o curso aberto naquele período. Cursos com **$\text{Qtd} \ge 4$** são carreiras consolidadas no mercado, enquanto **$\text{Qtd} = 1,0$** são nichos locais pontuais.

### 📅 O que é a Sazonalidade dos Semestres (.1 vs .2)?
Os vestibulares **.1 (início de ano)** são historicamente mais concorridos que os **.2 (meio de ano)**, pois os alunos concluem o Ensino Médio em dezembro.

---

## 🖥️ 4. Painel Interativo no Estilo Power BI

O arquivo [`painel_powerbi.html`](painel_powerbi.html) conta com **segmentadores dinâmicos de população**:
* 📍 **São José do Rio Preto (~480k hab. / 200k a 600k)**
* **Até 500 mil hab.**
* **Até 200 mil hab.**
* **Até 100 mil hab.**
* **Todos (Estado Geral)**

> **Ao clicar em qualquer porte populacional ou turno:**
> Os Cards de KPI, o Gráfico de Barras, o Gráfico de Linhas dinâmico e a Tabela Matriz **recalculam e redesenham instantaneamente** na tela!

### Como Abrir o Painel Power BI
Basta dar dois cliques no arquivo:
```text
painel_powerbi.html
```
*(Ou executar `start painel_powerbi.html` no terminal).*

---

## 🚀 5. Como Rodar a Análise no Terminal

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar script de análise
python executar_analise.py
```
*(Ou dar dois cliques no arquivo `executar.bat` no Windows).*

---

## 📁 6. Estrutura do Repositório

```text
├── demanda_vestibular.xlsx             # Base oficial com abas de faixas populacionais
├── executar_analise.py                 # Script Python mestre com análise de Rio Preto
├── executar.bat                        # Atalho executável de 1 clique
├── painel_powerbi.html                 # Dashboard interativo Power BI (População + Turnos Dinâmicos)
├── pop_tiers_data.json                 # Dados extraídos de todas as abas populacionais do Excel
├── requirements.txt                    # Dependências (pandas, matplotlib, openpyxl, seaborn)
├── tabela_top5_por_periodo.csv         # Tabela consolidada dos cursos líderes
├── tabela_metricas_completas_cursos.csv# Base completa de métricas
├── grafico_1_top_cursos_periodo.png    # Gráfico de barras horizontais por turno
├── grafico_2_evolucao_temporal.png     # Série histórica semestral explicativa
├── grafico_3_demanda_vs_escala.png     # Matriz de dispersão: Demanda Média vs. Qtd
├── grafico_4_proposta_recomendada.png  # Gráfico comparativo final para apresentação
└── README.md                           # Documentação completa
```

---

## 👥 Integrantes do Grupo
* Trabalho 4 – Gestão e Análise de Dados
* Apresentação: **09/11**
