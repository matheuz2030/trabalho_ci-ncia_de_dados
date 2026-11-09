import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import shutil

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.autolayout'] = True

excel_path = r'C:\Users\PICHAU\.gemini\antigravity\brain\fede3023-63c1-42db-824f-ab771fa6007a\.user_uploaded\media_1794244678548_df6afad6.xlsx'
output_dir = r'C:\Users\PICHAU\.gemini\antigravity\scratch\trabalho_vestibular'
artifact_dir = r'C:\Users\PICHAU\.gemini\antigravity\brain\fede3023-63c1-42db-824f-ab771fa6007a'

wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb['Todos']
data = []
for r in range(2, ws.max_row+1):
    vals = [ws.cell(r, c).value for c in range(2, 8)]
    if any(vals):
        data.append(vals)

df = pd.DataFrame(data[1:], columns=['Curso', 'Periodo', 'Vestibular', 'Demanda_Media', 'Qtd', 'Eixo'])
df['Demanda_Media'] = pd.to_numeric(df['Demanda_Media'])
df['Qtd'] = pd.to_numeric(df['Qtd'])

# 1. Gráfico: Top 6 Cursos por Período (Demanda Média)
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharex=False)
colors = {'Manhã': '#1f77b4', 'Tarde': '#ff7f0e', 'Noite': '#2ca02c'}

for i, p in enumerate(['Manhã', 'Tarde', 'Noite']):
    sub = df[df['Periodo'] == p]
    agg = sub.groupby('Curso').agg(
        demanda=('Demanda_Media', 'mean'),
        semestres=('Vestibular', 'count'),
        qtd=('Qtd', 'mean')
    ).reset_index()
    # Filter courses with at least 3 semesters to avoid one-off anomalies
    top = agg[agg['semestres'] >= 3].sort_values('demanda', ascending=True).tail(7)
    
    y_pos = range(len(top))
    bars = axes[i].barh(y_pos, top['demanda'], color=colors[p], alpha=0.85, edgecolor='black', linewidth=0.8)
    axes[i].set_yticks(y_pos)
    axes[i].set_yticklabels(top['Curso'], fontsize=9, fontweight='bold')
    axes[i].set_title(f'Turno {p} (Top Cursos - Demanda Média)', fontsize=12, fontweight='bold', pad=10)
    axes[i].set_xlabel('Candidatos por Vaga (Média 2022-2024)', fontsize=10)
    axes[i].set_xlim(0, max(top['demanda']) * 1.18)
    
    for bar in bars:
        w = bar.get_width()
        axes[i].text(w + 0.1, bar.get_y() + bar.get_height()/2, f'{w:.2f}', 
                     ha='left', va='center', fontsize=9, fontweight='bold', color='#333333')

plt.suptitle('Demanda Média dos Cursos por Turno no Vestibular FATEC (2022.1 a 2024.2)', fontsize=14, fontweight='bold', y=1.02)
chart1_path = os.path.join(output_dir, 'grafico_1_top_cursos_periodo.png')
plt.savefig(chart1_path, dpi=300, bbox_inches='tight')
plt.close()
print('Chart 1 created')

# 2. Gráfico: Evolução Temporal dos Principais Cursos Candidatos
fig, ax = plt.subplots(figsize=(12, 6))
sem_order = ['22.1', '22.2', '23.1', '23.2', '24.1', '24.2']

candidate_series = [
    ('ADS (Noite)', 'Análise e Desenvolvimento de Sistemas', 'Noite', '#2ca02c', 'o', '-'),
    ('ADS (Manhã)', 'Análise e Desenvolvimento de Sistemas', 'Manhã', '#1f77b4', 's', '-'),
    ('ADS (Tarde)', 'Análise e Desenvolvimento de Sistemas', 'Tarde', '#ff7f0e', '^', '-'),
    ('DSM (Noite)', 'Desenvolvimento de Software Multiplataforma', 'Noite', '#9467bd', 'D', '--'),
    ('DSM (Manhã)', 'Desenvolvimento de Software Multiplataforma', 'Manhã', '#17becf', 'v', '--'),
    ('Gestão Empresarial (Tarde)', 'Gestão Empresarial', 'Tarde', '#8c564b', 'p', '-.'),
    ('Gestão Empresarial (Noite)', 'Gestão Empresarial', 'Noite', '#e377c2', 'x', '-.'),
    ('GTI (Manhã)', 'Gestão da Tecnologia da Informação', 'Manhã', '#bcbd22', '*', ':'),
    ('RH (Manhã)', 'Gestão de Recursos Humanos', 'Manhã', '#d62728', 'h', ':'),
]

for label, curso, periodo, color, marker, ls in candidate_series:
    sub = df[(df['Curso'] == curso) & (df['Periodo'] == periodo)]
    sub_map = sub.set_index('Vestibular')['Demanda_Media'].reindex(sem_order)
    ax.plot(sem_order, sub_map.values, label=label, color=color, marker=marker, 
            linestyle=ls, linewidth=2.2, markersize=7)

ax.set_title('Série Histórica da Demanda (Candidatos/Vaga) dos Cursos Candidatos (2022.1 - 2024.2)', 
             fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Semestre do Vestibular', fontsize=11, fontweight='bold')
ax.set_ylabel('Demanda Média (Candidatos por Vaga)', fontsize=11, fontweight='bold')
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, fontsize=9)
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_ylim(0, 14)

chart2_path = os.path.join(output_dir, 'grafico_2_evolucao_temporal.png')
plt.savefig(chart2_path, dpi=300, bbox_inches='tight')
plt.close()
print('Chart 2 created')

# 3. Gráfico: Demanda Média vs Quantidade de Unidades (Dispersão / Quadrantes)
fig, ax = plt.subplots(figsize=(11, 7))
agg_all = df.groupby(['Curso', 'Periodo']).agg(
    demanda=('Demanda_Media', 'mean'),
    qtd=('Qtd', 'mean'),
    semestres=('Vestibular', 'count')
).reset_index()

agg_cons = agg_all[agg_all['semestres'] >= 3]

color_map = {'Manhã': '#1f77b4', 'Tarde': '#ff7f0e', 'Noite': '#2ca02c'}

for p in ['Manhã', 'Tarde', 'Noite']:
    p_data = agg_cons[agg_cons['Periodo'] == p]
    ax.scatter(p_data['qtd'], p_data['demanda'], label=p, color=color_map[p], 
               s=p_data['demanda']*25, alpha=0.7, edgecolors='black', linewidth=0.7)

# Destacar pontos-chave
labels_to_show = [
    ('Análise e Desenvolvimento de Sistemas', 'Noite'),
    ('Análise e Desenvolvimento de Sistemas', 'Manhã'),
    ('Análise e Desenvolvimento de Sistemas', 'Tarde'),
    ('Desenvolvimento de Software Multiplataforma', 'Noite'),
    ('Desenvolvimento de Software Multiplataforma', 'Manhã'),
    ('Desenvolvimento de Software Multiplataforma', 'Tarde'),
    ('Gestão Empresarial', 'Noite'),
    ('Gestão Empresarial', 'Manhã'),
    ('Gestão Empresarial', 'Tarde'),
    ('Logística', 'Noite'),
    ('Gestão de Recursos Humanos', 'Manhã'),
    ('Gestão da Tecnologia da Informação', 'Manhã'),
    ('Automação Industrial', 'Noite'),
    ('Design de Mídias Digitais', 'Noite'),
    ('Secretariado e Assessoria Internacional', 'Noite'),
]

for curso, periodo in labels_to_show:
    row = agg_cons[(agg_cons['Curso'] == curso) & (agg_cons['Periodo'] == periodo)]
    if not row.empty:
        r = row.iloc[0]
        short_name = curso.replace('Análise e Desenvolvimento de Sistemas', 'ADS') \
                          .replace('Desenvolvimento de Software Multiplataforma', 'DSM') \
                          .replace('Gestão da Tecnologia da Informação', 'GTI') \
                          .replace('Gestão Empresarial', 'Gestão Emp.') \
                          .replace('Gestão de Recursos Humanos', 'Gestão RH') \
                          .replace('Automação Industrial', 'Automação Ind.') \
                          .replace('Secretariado e Assessoria Internacional', 'Secretariado')
        ax.annotate(f"{short_name} ({r['Periodo'][0]})", (r['qtd'], r['demanda']),
                    textcoords="offset points", xytext=(5, 5), fontsize=8, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.75))

ax.set_title('Mapeamento Estratégico: Demanda Média vs. Escala de Oferta (Qtd de Unidades FATEC)', 
             fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Quantidade Média de Unidades Ofertantes no Estado (Consolidação)', fontsize=11, fontweight='bold')
ax.set_ylabel('Demanda Média (Candidatos / Vaga)', fontsize=11, fontweight='bold')
ax.legend(title='Turno', loc='upper left', frameon=True)
ax.axhline(y=2.5, color='gray', linestyle=':', alpha=0.7)
ax.axvline(x=5, color='gray', linestyle=':', alpha=0.7)
ax.text(18, 1.2, 'Zona de Alta Escala & Demanda Moderada\n(Cursos Tradicionais de Gestão)', fontsize=9, color='#555555')
ax.text(15, 10.5, 'Zona de Excelência Máxima\n(Alta Escala + Alta Demanda)', fontsize=9, color='#2ca02c', fontweight='bold')
ax.text(1, 7.5, 'Zona de Nicho / Alta Demanda Local\n(Poucas Unidades)', fontsize=9, color='#b22222')

chart3_path = os.path.join(output_dir, 'grafico_3_demanda_vs_escala.png')
plt.savefig(chart3_path, dpi=300, bbox_inches='tight')
plt.close()
print('Chart 3 created')

# 4. Gráfico: Síntese da Proposta Recomendada (3 Cursos)
fig, ax = plt.subplots(figsize=(10, 5.5))

rec_courses = [
    ('Manhã', 'Desenvolvimento de Software\nMultiplataforma (DSM)', 3.21, 3.15, '#1f77b4'),
    ('Tarde', 'Gestão Empresarial\n(ou DSM Vespertino)', 1.83, 2.05, '#ff7f0e'),
    ('Noite', 'Análise e Desenvolvimento\nde Sistemas (ADS)', 9.90, 9.96, '#2ca02c')
]

periods = [r[0] for r in rec_courses]
names = [f"{r[0]}:\n{r[1]}" for r in rec_courses]
means = [r[2] for r in rec_courses]
recents = [r[3] for r in rec_courses]
bar_colors = [r[4] for r in rec_courses]

x = np.arange(len(periods))
width = 0.35

rects1 = ax.bar(x - width/2, means, width, label='Média Histórica (22-24)', color=bar_colors, alpha=0.75, edgecolor='black')
rects2 = ax.bar(x + width/2, recents, width, label='Média Recente (2024)', color=bar_colors, hatch='//', alpha=0.95, edgecolor='black')

ax.set_ylabel('Candidatos por Vaga', fontsize=11, fontweight='bold')
ax.set_title('Proposta Recomendada de Abertura de Cursos por Período (FATEC)', fontsize=13, fontweight='bold', pad=12)
ax.set_xticks(x)
ax.set_xticklabels(names, fontsize=10, fontweight='bold')
ax.legend(frameon=True, fontsize=10)
ax.set_ylim(0, 12)

# Rotulando as barras
for rect in rects1:
    h = rect.get_height()
    ax.annotate(f'{h:.2f}', xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')
for rect in rects2:
    h = rect.get_height()
    ax.annotate(f'{h:.2f}', xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')

chart4_path = os.path.join(output_dir, 'grafico_4_proposta_recomendada.png')
plt.savefig(chart4_path, dpi=300, bbox_inches='tight')
plt.close()
print('Chart 4 created')

# Copy all charts to artifact_dir as well
for f in ['grafico_1_top_cursos_periodo.png', 'grafico_2_evolucao_temporal.png', 'grafico_3_demanda_vs_escala.png', 'grafico_4_proposta_recomendada.png']:
    src = os.path.join(output_dir, f)
    dst = os.path.join(artifact_dir, f)
    shutil.copy2(src, dst)
    print(f'Copied {f} to artifact dir')
