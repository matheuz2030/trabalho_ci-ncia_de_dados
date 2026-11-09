import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.autolayout'] = True

excel_path = r'C:\Users\PICHAU\.gemini\antigravity\scratch\trabalho_vestibular\demanda_vestibular.xlsx'
output_dir = r'C:\Users\PICHAU\.gemini\antigravity\scratch\trabalho_vestibular'
artifact_dir = r'C:\Users\PICHAU\.gemini\antigravity\brain\fede3023-63c1-42db-824f-ab771fa6007a'

wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb['Todos']
data = []
for r in range(2, ws.max_row+1):
    vals = [ws.cell(r, c).value for c in range(2, 8)]
    if any(vals): data.append(vals)

df = pd.DataFrame(data[1:], columns=['Curso', 'Periodo', 'Vestibular', 'Demanda_Media', 'Qtd', 'Eixo'])
df['Demanda_Media'] = pd.to_numeric(df['Demanda_Media'])
df['Qtd'] = pd.to_numeric(df['Qtd'])

# -------------------------------------------------------------
# GRÁFICO 2 MELHORADO: EVOLUÇÃO TEMPORAL COM EXPLICAÇÃO DE C/V
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 7))
sem_order = ['22.1', '22.2', '23.1', '23.2', '24.1', '24.2']
x_indices = np.arange(len(sem_order))

# Faixas sombreadas de sazonalidade (.1 = vestibular de início de ano, maior procura)
for i in [0, 2, 4]:
    ax.axvspan(i - 0.35, i + 0.35, color='#f8fafc', alpha=0.9, zorder=0)
    ax.text(i, 13.3, 'Vestibular .1\n(Início de Ano)', ha='center', va='bottom', fontsize=8, color='#64748b', fontweight='semibold')

for i in [1, 3, 5]:
    ax.text(i, 13.3, 'Vestibular .2\n(Meio de Ano)', ha='center', va='bottom', fontsize=8, color='#94a3b8', fontstyle='italic')

series_to_plot = [
    ('ADS (Noite) - Curso Escolhido', 'Análise e Desenvolvimento de Sistemas', 'Noite', '#10b981', 'o', '-', 2.8, 8),
    ('ADS (Manhã) - Benchmark', 'Análise e Desenvolvimento de Sistemas', 'Manhã', '#38bdf8', 's', '--', 2.0, 6),
    ('ADS (Tarde) - Benchmark', 'Análise e Desenvolvimento de Sistemas', 'Tarde', '#0ea5e9', '^', ':', 1.8, 6),
    ('DSM (Manhã) - Curso Escolhido', 'Desenvolvimento de Software Multiplataforma', 'Manhã', '#3b82f6', 'D', '-', 2.4, 7),
    ('DSM (Noite) - Alternativa TI', 'Desenvolvimento de Software Multiplataforma', 'Noite', '#8b5cf6', 'v', '--', 1.8, 6),
    ('Gestão Empresarial (Tarde) - Curso Escolhido', 'Gestão Empresarial', 'Tarde', '#f59e0b', 'p', '-', 2.4, 7),
    ('Gestão de RH (Manhã) - Alternativa Gestão', 'Gestão de Recursos Humanos', 'Manhã', '#ec4899', 'h', ':', 1.8, 6),
]

for label, curso, periodo, color, marker, ls, lw, ms in series_to_plot:
    sub = df[(df['Curso'] == curso) & (df['Periodo'] == periodo)]
    s_map = sub.set_index('Vestibular')['Demanda_Media'].reindex(sem_order)
    y_vals = s_map.values
    ax.plot(x_indices, y_vals, label=label, color=color, marker=marker, 
            linestyle=ls, linewidth=lw, markersize=ms, zorder=3)
    
    # Adicionar rótulo numérico apenas nos cursos recomendados para manter clareza
    if 'Curso Escolhido' in label:
        for idx, y in enumerate(y_vals):
            if not np.isnan(y):
                offset = 0.35 if 'ADS' in label else (-0.45 if 'Gestão' in label else 0.35)
                ax.annotate(f'{y:.2f}', (idx, y), textcoords="offset points", 
                            xytext=(0, 6 if offset > 0 else -12),
                            ha='center', fontsize=8, fontweight='bold', color=color,
                            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec=color, alpha=0.85, lw=0.8),
                            zorder=4)

ax.set_title('Série Histórica da Demanda Semestral (2022.1 a 2024.2) dos Cursos FATEC\nEvidência da Sazonalidade (Início vs. Meio de Ano) e Estabilidade das Escolhas', 
             fontsize=13, fontweight='bold', pad=18)
ax.set_xticks(x_indices)
ax.set_xticklabels(sem_order, fontsize=11, fontweight='bold')
ax.set_xlabel('Semestre do Vestibular (Sazonalidade: .1 Início de Ano | .2 Meio de Ano)', fontsize=11, fontweight='bold', labelpad=8)
ax.set_ylabel('C/V = Candidatos por Vaga (Inscritos Totais ÷ Vagas Ofertadas)', fontsize=11, fontweight='bold', labelpad=8)
ax.set_ylim(0, 14.5)
ax.set_xlim(-0.5, 5.5)

# Caixa de Legenda Explicativa sobre C/V
legend = ax.legend(loc='upper right', frameon=True, fontsize=8.5, facecolor='white', framealpha=0.95, edgecolor='#cbd5e1')
legend.set_title('Legenda de Cursos por Turno', prop={'size': 9, 'weight': 'bold'})

# Caixa Informativa sobre o que é C/V
text_box = (
    "O QUE É C/V (CANDIDATOS POR VAGA)?\n"
    "• C/V = Total de Inscritos ÷ Vagas Ofertadas.\n"
    "• C/V > 1,5: Turma autossustentável sem vagas ociosas.\n"
    "• C/V > 3,0: Alta concorrência e prestígio de mercado.\n"
    "• C/V > 9,0: Fenômeno estadual de procura (caso de ADS Noite)."
)
ax.text(0.02, 0.04, text_box, transform=ax.transAxes, fontsize=8.5,
        verticalalignment='bottom', bbox=dict(boxstyle='round,pad=0.5', facecolor='#f1f5f9', edgecolor='#94a3b8', alpha=0.95),
        zorder=5)

chart2_path = os.path.join(output_dir, 'grafico_2_evolucao_temporal.png')
plt.savefig(chart2_path, dpi=300, bbox_inches='tight')
plt.close()
print("Novo grafico_2_evolucao_temporal.png gerado com sucesso!")

# Copiar para pasta de artefatos
shutil.copy2(chart2_path, os.path.join(artifact_dir, 'grafico_2_evolucao_temporal.png'))
