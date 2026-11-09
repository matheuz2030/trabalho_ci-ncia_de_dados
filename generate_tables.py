import openpyxl
import pandas as pd
import numpy as np
import os

excel_path = r'C:\Users\PICHAU\.gemini\antigravity\brain\fede3023-63c1-42db-824f-ab771fa6007a\.user_uploaded\media_1794244678548_df6afad6.xlsx'
output_dir = r'C:\Users\PICHAU\.gemini\antigravity\scratch\trabalho_vestibular'

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

sem_map = {'22.1': 1, '22.2': 2, '23.1': 3, '23.2': 4, '24.1': 5, '24.2': 6}
df['Sem_Num'] = df['Vestibular'].map(sem_map)

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
        
        d24_1 = grp.loc[grp['Vestibular']=='24.1', 'Demanda_Media'].values
        d24_2 = grp.loc[grp['Vestibular']=='24.2', 'Demanda_Media'].values
        v24_1 = d24_1[0] if len(d24_1) > 0 else np.nan
        v24_2 = d24_2[0] if len(d24_2) > 0 else np.nan
        mean_rec = np.nanmean([v24_1, v24_2])
        
        slope = np.polyfit(grp['Sem_Num'], grp['Demanda_Media'], 1)[0] if n_sem >= 3 else 0.0
        weighted = mean_dem * mean_qtd
        
        rows.append({
            'Periodo': p,
            'Curso': curso,
            'Eixo': grp['Eixo'].iloc[0],
            'Semestres_Ofertados': n_sem,
            'Demanda_Media_Geral': round(mean_dem, 2),
            'Demanda_Recente_2024': round(mean_rec, 2) if not np.isnan(mean_rec) else np.nan,
            'Demanda_Min': round(min_dem, 2),
            'Demanda_Max': round(max_dem, 2),
            'Desvio_Padrao': round(std_dem, 2),
            'Tendencia_Inclinacao': round(slope, 3),
            'Qtd_Media_Unidades': round(mean_qtd, 1),
            'Demanda_Ponderada': round(weighted, 2)
        })

df_metrics = pd.DataFrame(rows)
df_metrics.sort_values(by=['Periodo', 'Demanda_Media_Geral'], ascending=[True, False], inplace=True)
csv_metrics_path = os.path.join(output_dir, 'tabela_metricas_completas_cursos.csv')
df_metrics.to_csv(csv_metrics_path, index=False, encoding='utf-8-sig')

top_rows = []
for p in ['Manhã', 'Tarde', 'Noite']:
    sub = df_metrics[(df_metrics['Periodo'] == p) & (df_metrics['Semestres_Ofertados'] >= 3)]
    top_rows.append(sub.head(5))

top_periodos = pd.concat(top_rows, ignore_index=True)
top_periodos_path = os.path.join(output_dir, 'tabela_top5_por_periodo.csv')
top_periodos.to_csv(top_periodos_path, index=False, encoding='utf-8-sig')
print('Tables updated successfully.')
