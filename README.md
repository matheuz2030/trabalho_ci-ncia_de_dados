# 📊 Trabalho 4 – Análise de Demanda do Vestibular FATEC

> **Apresentação:** 09/11  
> **Objetivo:** Definir e justificar a abertura de **1 curso por período** (Manhã, Tarde e Noite) com base no histórico do Vestibular FATEC (2022.1 a 2024.2), utilizando análise estatística em Python e Dashboard interativo estilo Power BI.

---

## 🎯 1. Resumo da Decisão (Cursos Escolhidos e Justificativas)

| Período | Curso Escolhido | Demanda Média | Demanda 2024 | Qtd Unidades | Motivo da Escolha (Justificativa Direta) |
| :--- | :--- | :---: | :---: | :---: | :--- |
| 🌅 **Manhã** | **Desenvolvimento de Software Multiplataforma (DSM)** | **3,21** c/v | **3,15** c/v | 5,2 | **100% de Sinergia de Laboratórios:** Reutiliza integralmente os laboratórios de informática montados para o período noturno de ADS, reduzindo o custo de implantação da turma a quase zero. Atende jovens recém-formados no Ensino Médio que estudam de manhã e estagiam à tarde. |
| ☀️ **Tarde** | **Gestão Empresarial** *(ou DSM Vespertino)* | **1,83** c/v | **2,05** c/v | 4,0 | **Proteção do Turno Mais Crítico:** O período da tarde é o mais vulnerável a turmas vazias e evasão escolar (apenas 20 cursos da FATEC operam à tarde). Gestão Empresarial apresenta demanda sólida com **aceleração para 2,05 c/v em 2024**, baixíssimo risco ($\sigma = 0,36$) e diversifica para o eixo de Gestão & Negócios. |
| 🌙 **Noite** | **Análise e Desenvolvimento de Sistemas (ADS)** | **9,90** c/v | **9,96** c/v | 22,3 | **Líder Absoluto de Procura no Estado:** Maior concorrência histórica da FATEC em mais de 22 unidades. Garante preenchimento imediato de 100% das vagas e atende os estudantes que trabalham durante o dia. |

---

## 🚀 2. Como Rodar a Análise

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

### Passo 2: Instalar as Dependências
Certifique-se de ter o **Python 3.10+** instalado e execute:
```bash
pip install -r requirements.txt
```
*(Instala `pandas`, `matplotlib`, `seaborn` e `openpyxl`).*

### Passo 3: Executar a Análise
Execute o script mestre pelo terminal:
```bash
python executar_analise.py
```
> **No Windows:** Você também pode simplesmente dar **2 cliques no arquivo `executar.bat`**.

O script irá:
1. Processar os 892 registros da planilha `demanda_vestibular.xlsx`.
2. Exibir os rankings formatados diretamente no terminal.
3. Atualizar as planilhas `tabela_top5_por_periodo.csv` e `tabela_metricas_completas_cursos.csv`.
4. Gerar os 4 gráficos analíticos em alta resolução (300 DPI).

---

## 🖥️ 3. Como Abrir o Painel Interativo (Estilo Power BI)

O projeto inclui um dashboard interativo completo estilo **Power BI Dark Theme** com cartões KPI, segmentadores dinâmicos de turno e matriz detalhada:

Basta dar dois cliques no arquivo:
```text
painel_powerbi.html
```
*(Ou executar `start painel_powerbi.html` no terminal / prompt de comando).*

---

## 📁 4. Estrutura do Projeto

```text
├── demanda_vestibular.xlsx             # Base histórica oficial de demanda (2022.1 - 2024.2)
├── executar_analise.py                 # Script Python mestre de cálculo estatístico e geração de gráficos
├── executar.bat                        # Atalho executável de 1 clique para Windows
├── painel_powerbi.html                 # Dashboard interativo completo estilo Power BI
├── requirements.txt                    # Dependências do projeto (pandas, matplotlib, openpyxl, seaborn)
├── tabela_top5_por_periodo.csv         # Tabela consolidada dos 5 cursos líderes por turno
├── tabela_metricas_completas_cursos.csv# Base completa com médias, desvios e tendências de todos os cursos
├── grafico_1_top_cursos_periodo.png    # Gráfico de barras horizontais por turno
├── grafico_2_evolucao_temporal.png     # Série histórica semestral dos cursos concorrentes
├── grafico_3_demanda_vs_escala.png     # Matriz de dispersão: Demanda Média vs. Qtd de Unidades
├── grafico_4_proposta_recomendada.png  # Gráfico comparativo final para slides de apresentação
└── README.md                           # Documentação e guia do trabalho
```

---

## 📈 5. Gráficos Gerados

### Proposta Recomendada por Período
![Proposta Recomendada](grafico_4_proposta_recomendada.png)

### Ranking de Cursos por Turno
![Top Cursos](grafico_1_top_cursos_periodo.png)

### Série Histórica (2022.1 a 2024.2)
![Evolução Temporal](grafico_2_evolucao_temporal.png)

### Matriz de Dispersão (Demanda vs. Escala)
![Demanda vs Escala](grafico_3_demanda_vs_escala.png)

---

## 👥 Integrantes do Grupo
* Trabalho 4 – Gestão / Análise de Dados
* Apresentação: **09/11**
