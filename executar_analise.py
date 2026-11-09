# -*- coding: utf-8 -*-
"""
Trabalho 4 - Análise de Demanda do Vestibular FATEC (2022 a 2024)
Script Completo de Execução
Gera tabelas estatísticas em CSV, rankings no terminal e 4 gráficos analíticos.
"""

import os
import sys
import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("=" * 75)
    print(" FATEC - ANÁLISE DE DEMANDA DO VESTIBULAR (TRABALHO 4)")
    print("=" * 75)
    
    # 1. Localização do arquivo Excel
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, "demanda_vestibular.xlsx")
    
    if not os.path.exists(excel_path):
        # Fallback para o caminho original caso executado de outro lugar
        fallback = r"C:\Users\PICHAU\.gemini\antigravity\brain\fede3023-63c1-42db-824f-ab771fa6007a\.user_uploaded\media_1794244678548_df6afad6.xlsx"
        if os.path.exists(fallback):
            excel_path = fallback
        else:
            print(f"[ERRO] Arquivo de dados não encontrado em: {excel_path}")
            return

    print(f"[*] Carregando base de dados: {excel_path}")
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws = wb['Todos']
    
    data = []
    for r in range(2, ws.max_row + 1):
        vals = [ws.cell(r, c).value for c in range(2, 8)]
        if any(vals):
            data.append(vals)

    df = pd.DataFrame(data[1:], columns=['Curso', 'Periodo', 'Vestibular', 'Demanda_Media', 'Qtd', 'Eixo'])
    df['Demanda_Media'] = pd.to_numeric(df['Demanda_Media'], errors='coerce')
    df['Qtd'] = pd.to_numeric(df['Qtd'], errors='coerce')

    sem_map = {'22.1': 1, '22.2': 2, '23.1': 3, '23.2': 4, '24.1': 5, '24.2': 6}
    df['Sem_Num'] = df['Vestibular'].map(sem_map)
    print(f"[OK] {len(df)} registros carregados com sucesso (6 semestres: 2022.1 a 2024.2).\n")

    # 2. Cálculo das Métricas Completas por Curso e Período
    print("[*] Calculando métricas estatísticas...")
    rows = []
    for p in ['Manhã', 'Tarde', 'Noite']:
        sub = df[df['Periodo'] == p]
        for curso, grp in sub.groupby('Curso'):
            n_sem = len(grp)
            mean_dem = grp['Demanda_Media'].mean()
            std_dem = grp['Demanda_Media'].std() if n_sem > 1 else 0.0
            min_dem = grp['Demanda_Media'].min()
            max_dem = grp['Demanda_Media'].max()
            mean_qtd = grp['Qtd'].mean()
            
            d24_1 = grp.loc[grp['Vestibular'] == '24.1', 'Demanda_Media'].values
            d24_2 = grp.loc[grp['Vestibular'] == '24.2', 'Demanda_Media'].values
            v24_1 = d24_1[0] if len(d24_1) > 0 else np.nan
            v24_2 = d24_2[0] if len(d24_2) > 0 else np.nan
            mean_rec = np.nanmean([v24_1, v24_2])
            
            slope = np.polyfit(grp['Sem_Num'], grp['Demanda_Media'], 1)[0] if n_sem >= 3 else 0.0
            weighted = mean_dem * mean_qtd
            
            rows.append({
                'Periodo': p,
                'Curso': curso,
                'Eixo': grp['Eixo'].iloc[0],
                'Semestres': n_sem,
                'Demanda_Media': round(mean_dem, 2),
                'Demanda_Recente_24': round(mean_rec, 2) if not np.isnan(mean_rec) else np.nan,
                'Desvio_Padrao': round(std_dem, 2),
                'Tendencia': round(slope, 3),
                'Qtd_Media': round(mean_qtd, 1),
                'Demanda_Ponderada': round(weighted, 2)
            })

    df_metrics = pd.DataFrame(rows)
    df_metrics.sort_values(by=['Periodo', 'Demanda_Media'], ascending=[True, False], inplace=True)
    
    # Exportar CSV completo
    csv_full = os.path.join(script_dir, "tabela_metricas_completas_cursos.csv")
    df_metrics.to_csv(csv_full, index=False, encoding='utf-8-sig')
    print(f"[OK] Tabela completa salva em: {csv_full}")

    # Top 5 filtrando cursos com pelo menos 3 semestres de oferta
    top_rows = []
    for p in ['Manhã', 'Tarde', 'Noite']:
        sub = df_metrics[(df_metrics['Periodo'] == p) & (df_metrics['Semestres'] >= 3)]
        top_rows.append(sub.head(5))

    top_periodos = pd.concat(top_rows, ignore_index=True)
    csv_top5 = os.path.join(script_dir, "tabela_top5_por_periodo.csv")
    top_periodos.to_csv(csv_top5, index=False, encoding='utf-8-sig')
    print(f"[OK] Tabela Top 5 salva em: {csv_top5}\n")

    # 3. Exibir Rankings Formatados no Terminal
    print("=" * 75)
    print(" TOP 5 CURSOS POR PERÍODO (CURSOS CONSOLIDADOS >= 3 SEMESTRES)")
    print("=" * 75)
    for p in ['Manhã', 'Tarde', 'Noite']:
        print(f"\n>>> PERÍODO: {p.upper()}")
        print("-" * 75)
        p_df = top_periodos[top_periodos['Periodo'] == p]
        for idx, (_, r) in enumerate(p_df.iterrows(), 1):
            print(f" {idx}. {r['Curso']:<42} | Dem. Média: {r['Demanda_Media']:>5.2f} c/v | 2024: {r['Demanda_Recente_24']:>5.2f} c/v | Qtd Unidades: {r['Qtd_Media']:>4.1f}")
    
    print("\n" + "=" * 75)
    print(" PROPOSTA RECOMENDADA (1 CURSO POR PERÍODO - PORTFÓLIO ESTRATÉGICO)")
    print("=" * 75)
    print(" * MANHÃ: Desenvolvimento de Software Multiplataforma (DSM) -> 3.21 c/v (Qtd: 5.2)")
    print("          Justificativa: 100% de sinergia de laboratórios com ADS; alta procura matutina.")
    print(" * TARDE: Gestão Empresarial -> 1.83 c/v (2024: 2.05 c/v | Qtd: 4.0)")
    print("          Justificativa: Estabilidade no turno mais crítico; diversifica para Gestão e Negócios.")
    print(" * NOITE: Análise e Desenvolvimento de Sistemas (ADS) -> 9.90 c/v (Qtd: 22.3)")
    print("          Justificativa: Líder absoluto e indiscutível de procura no estado; alta consolidação.")
    print("=" * 75)

    # 4. Geração dos Gráficos
    print("\n[*] Gerando 4 gráficos em alta resolução (300 DPI)...")
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
    plt.rcParams['font.size'] = 10
    plt.rcParams['figure.autolayout'] = True

    # Gráfico 1: Top Cursos por Período
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    colors = {'Manhã': '#1f77b4', 'Tarde': '#ff7f0e', 'Noite': '#2ca02c'}
    for i, p in enumerate(['Manhã', 'Tarde', 'Noite']):
        sub = df[df['Periodo'] == p]
        agg = sub.groupby('Curso').agg(demanda=('Demanda_Media', 'mean'), semestres=('Vestibular', 'count')).reset_index()
        top = agg[agg['semestres'] >= 3].sort_values('demanda', ascending=True).tail(7)
        y_pos = range(len(top))
        bars = axes[i].barh(y_pos, top['demanda'], color=colors[p], alpha=0.85, edgecolor='black', linewidth=0.8)
        axes[i].set_yticks(y_pos)
        axes[i].set_yticklabels(top['Curso'], fontsize=9, fontweight='bold')
        axes[i].set_title(f'Turno {p} (Top Cursos)', fontsize=12, fontweight='bold', pad=10)
        axes[i].set_xlabel('Candidatos por Vaga (Média 2022-2024)', fontsize=10)
        axes[i].set_xlim(0, max(top['demanda']) * 1.18)
        for bar in bars:
            w = bar.get_width()
            axes[i].text(w + 0.1, bar.get_y() + bar.get_height()/2, f'{w:.2f}', ha='left', va='center', fontsize=9, fontweight='bold')

    plt.suptitle('Demanda Média dos Cursos por Turno no Vestibular FATEC (2022.1 a 2024.2)', fontsize=14, fontweight='bold', y=1.02)
    g1 = os.path.join(script_dir, "grafico_1_top_cursos_periodo.png")
    plt.savefig(g1, dpi=300, bbox_inches='tight')
    plt.close()
    print(" [1/4] grafico_1_top_cursos_periodo.png gerado.")

    # Gráfico 2: Evolução Temporal
    fig, ax = plt.subplots(figsize=(12, 6))
    sem_order = ['22.1', '22.2', '23.1', '23.2', '24.1', '24.2']
    candidate_series = [
        ('ADS (Noite)', 'Análise e Desenvolvimento de Sistemas', 'Noite', '#2ca02c', 'o', '-'),
        ('ADS (Manhã)', 'Análise e Desenvolvimento de Sistemas', 'Manhã', '#1f77b4', 's', '-'),
        ('ADS (Tarde)', 'Análise e Desenvolvimento de Sistemas', 'Tarde', '#ff7f0e', '^', '-'),
        ('DSM (Noite)', 'Desenvolvimento de Software Multiplataforma', 'Noite', '#9467bd', 'D', '--'),
        ('DSM (Manhã)', 'Desenvolvimento de Software Multiplataforma', 'Manhã', '#17becf', 'v', '--'),
        ('Gestão Empresarial (Tarde)', 'Gestão Empresarial', 'Tarde', '#8c564b', 'p', '-.'),
        ('GTI (Manhã)', 'Gestão da Tecnologia da Informação', 'Manhã', '#bcbd22', '*', ':'),
    ]
    for label, curso, periodo, color, marker, ls in candidate_series:
        sub = df[(df['Curso'] == curso) & (df['Periodo'] == periodo)]
        sub_map = sub.set_index('Vestibular')['Demanda_Media'].reindex(sem_order)
        ax.plot(sem_order, sub_map.values, label=label, color=color, marker=marker, linestyle=ls, linewidth=2.2, markersize=7)

    ax.set_title('Série Histórica da Demanda (Candidatos/Vaga) dos Cursos Candidatos (2022.1 - 2024.2)', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Semestre do Vestibular', fontsize=11, fontweight='bold')
    ax.set_ylabel('Demanda Média (Candidatos por Vaga)', fontsize=11, fontweight='bold')
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, fontsize=9)
    ax.grid(True, linestyle='--', alpha=0.6)
    g2 = os.path.join(script_dir, "grafico_2_evolucao_temporal.png")
    plt.savefig(g2, dpi=300, bbox_inches='tight')
    plt.close()
    print(" [2/4] grafico_2_evolucao_temporal.png gerado.")

    # Gráfico 3: Demanda vs Escala
    fig, ax = plt.subplots(figsize=(11, 7))
    agg_all = df.groupby(['Curso', 'Periodo']).agg(demanda=('Demanda_Media', 'mean'), qtd=('Qtd', 'mean'), semestres=('Vestibular', 'count')).reset_index()
    agg_cons = agg_all[agg_all['semestres'] >= 3]
    for p in ['Manhã', 'Tarde', 'Noite']:
        p_data = agg_cons[agg_cons['Periodo'] == p]
        ax.scatter(p_data['qtd'], p_data['demanda'], label=p, color=colors[p], s=p_data['demanda']*25, alpha=0.7, edgecolors='black', linewidth=0.7)

    ax.set_title('Mapeamento Estratégico: Demanda Média vs. Escala de Oferta (Qtd de Unidades)', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Quantidade Média de Unidades FATEC no Estado (Consolidação)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Demanda Média (Candidatos / Vaga)', fontsize=11, fontweight='bold')
    ax.legend(title='Turno', loc='upper left', frameon=True)
    g3 = os.path.join(script_dir, "grafico_3_demanda_vs_escala.png")
    plt.savefig(g3, dpi=300, bbox_inches='tight')
    plt.close()
    print(" [3/4] grafico_3_demanda_vs_escala.png gerado.")

    # Gráfico 4: Proposta Recomendada
    fig, ax = plt.subplots(figsize=(10, 5.5))
    rec = [
        ('Manhã', 'DSM\n(Software Multiplataforma)', 3.21, 3.15, '#1f77b4'),
        ('Tarde', 'Gestão Empresarial\n(Vespertino)', 1.83, 2.05, '#ff7f0e'),
        ('Noite', 'ADS\n(Análise e Desenv. Sistemas)', 9.90, 9.96, '#2ca02c')
    ]
    x = np.arange(len(rec))
    w = 0.35
    r1 = ax.bar(x - w/2, [r[2] for r in rec], w, label='Média Histórica (22-24)', color=[r[4] for r in rec], alpha=0.75, edgecolor='black')
    r2 = ax.bar(x + w/2, [r[3] for r in rec], w, label='Média Recente (2024)', color=[r[4] for r in rec], hatch='//', alpha=0.95, edgecolor='black')
    ax.set_ylabel('Candidatos por Vaga', fontsize=11, fontweight='bold')
    ax.set_title('Proposta Recomendada de Abertura de Cursos por Período (FATEC)', fontsize=13, fontweight='bold', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{r[0]}:\n{r[1]}" for r in rec], fontsize=10, fontweight='bold')
    ax.legend(frameon=True, fontsize=10)
    for r in r1:
        h = r.get_height()
        ax.annotate(f'{h:.2f}', xy=(r.get_x() + r.get_width() / 2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')
    for r in r2:
        h = r.get_height()
        ax.annotate(f'{h:.2f}', xy=(r.get_x() + r.get_width() / 2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')

    g4 = os.path.join(script_dir, "grafico_4_proposta_recomendada.png")
    plt.savefig(g4, dpi=300, bbox_inches='tight')
    plt.close()
    print(" [4/4] grafico_4_proposta_recomendada.png gerado.")

    print("\n" + "=" * 75)
    print(" [CONCLUÍDO] Análise finalizada com sucesso!")
    print(f" Arquivos disponíveis na pasta: {script_dir}")
    print("=" * 75)

if __name__ == '__main__':
    main()
