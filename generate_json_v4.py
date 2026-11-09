import json
import openpyxl
import pandas as pd
import numpy as np

excel_path = r'C:\Users\PICHAU\.gemini\antigravity\scratch\trabalho_vestibular\demanda_vestibular.xlsx'
wb = openpyxl.load_workbook(excel_path, data_only=True)

tier_sheets = {
    'rio_preto': '200 a 600',       # São José do Rio Preto (~480k hab.)
    'ate_500': 'Até 500',           # Até 500 mil hab.
    'faixa_100_600': '100 a 600',   # 100 a 600 mil hab.
    'pequenas_ate_200': 'Até 200',  # Cidades Pequenas (Até 100k / Até 200k hab. - idênticas no Excel)
    'todos': 'Todos'                # Estado Geral
}

sem_order = ['22.1', '22.2', '23.1', '23.2', '24.1', '24.2']
sem_map = {s: i+1 for i, s in enumerate(sem_order)}

exported_data = {}

for tier_key, sheet_name in tier_sheets.items():
    ws = wb[sheet_name]
    data = [[ws.cell(r, c).value for c in range(2, 8)] for r in range(2, ws.max_row+1)]
    df = pd.DataFrame(data[1:], columns=['Curso', 'Periodo', 'Vestibular', 'Demanda_Media', 'Qtd', 'Eixo'])
    df['Demanda_Media'] = pd.to_numeric(df['Demanda_Media'])
    df['Qtd'] = pd.to_numeric(df['Qtd'])
    
    courses_summary = []
    series_history = {}
    
    for (curso, periodo), grp in df.groupby(['Curso', 'Periodo']):
        n_sem = len(grp)
        mean_dem = grp['Demanda_Media'].mean()
        std_dem = grp['Demanda_Media'].std() if n_sem > 1 else 0.0
        mean_qtd = grp['Qtd'].mean()
        
        d24_1 = grp.loc[grp['Vestibular']=='24.1', 'Demanda_Media'].values
        d24_2 = grp.loc[grp['Vestibular']=='24.2', 'Demanda_Media'].values
        v24_1 = d24_1[0] if len(d24_1) > 0 else np.nan
        v24_2 = d24_2[0] if len(d24_2) > 0 else np.nan
        mean_rec = np.nanmean([v24_1, v24_2])
        
        piv = grp.set_index('Vestibular')['Demanda_Media'].reindex(sem_order)
        vals_list = [round(float(v), 2) if not np.isnan(v) else None for v in piv.values]
        
        series_key = f"{curso}_{periodo}"
        series_history[series_key] = {
            'curso': curso,
            'turno': periodo,
            'vals': vals_list,
            'media': round(mean_dem, 2),
            'rec24': round(mean_rec, 2) if not np.isnan(mean_rec) else round(mean_dem, 2),
            'dp': round(std_dem, 2),
            'qtd': round(mean_qtd, 1),
            'eixo': grp['Eixo'].iloc[0],
            'semestres': n_sem
        }
        
        courses_summary.append({
            'turno': periodo,
            'curso': curso,
            'eixo': grp['Eixo'].iloc[0],
            'media': round(mean_dem, 2),
            'rec24': round(mean_rec, 2) if not np.isnan(mean_rec) else round(mean_dem, 2),
            'dp': round(std_dem, 2),
            'qtd': round(mean_qtd, 1),
            'semestres': n_sem,
            'key': series_key
        })
        
    exported_data[tier_key] = {
        'sheet': sheet_name,
        'courses': courses_summary,
        'series': series_history
    }

with open(r'C:\Users\PICHAU\.gemini\antigravity\scratch\trabalho_vestibular\pop_tiers_data_v4.json', 'w', encoding='utf-8') as f:
    json.dump(exported_data, f, ensure_ascii=False, indent=2)

print("pop_tiers_data_v4.json gerado com sucesso!")
