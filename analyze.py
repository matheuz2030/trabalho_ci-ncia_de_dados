import openpyxl
import pandas as pd
import numpy as np

excel_path = r'C:\Users\PICHAU\.gemini\antigravity\brain\fede3023-63c1-42db-824f-ab771fa6007a\.user_uploaded\media_1794244678548_df6afad6.xlsx'
wb = openpyxl.load_workbook(excel_path, data_only=True)

results = []

for s in wb.sheetnames:
    if 'Popula' in s:
        continue
    ws = wb[s]
    data = []
    for r in range(2, ws.max_row+1):
        vals = [ws.cell(r, c).value for c in range(2, 8)]
        if any(vals):
            data.append(vals)
    df = pd.DataFrame(data[1:], columns=['Curso', 'Periodo', 'Vestibular', 'Demanda_Media', 'Qtd', 'Eixo'])
    df['Demanda_Media'] = pd.to_numeric(df['Demanda_Media'])
    df['Qtd'] = pd.to_numeric(df['Qtd'])
    
    for p in ['Manhã', 'Tarde', 'Noite']:
        sub = df[df['Periodo'] == p]
        if sub.empty:
            continue
        agg = sub.groupby('Curso').agg(
            demanda_media=('Demanda_Media', 'mean'),
            semestres=('Vestibular', 'count'),
            qtd_media=('Qtd', 'mean')
        ).reset_index()
        # Filter courses with at least 4 semesters for consistency
        agg_consist = agg[agg['semestres'] >= 4].sort_values('demanda_media', ascending=False)
        if not agg_consist.empty:
            t1 = agg_consist.iloc[0]
            t2 = agg_consist.iloc[1] if len(agg_consist) > 1 else None
            t3 = agg_consist.iloc[2] if len(agg_consist) > 2 else None
            results.append({
                'Sheet': s,
                'Periodo': p,
                'Top1': f"{t1['Curso']} ({t1['demanda_media']:.2f})",
                'Top2': f"{t2['Curso']} ({t2['demanda_media']:.2f})" if t2 is not None else '-',
                'Top3': f"{t3['Curso']} ({t3['demanda_media']:.2f})" if t3 is not None else '-'
            })

res_df = pd.DataFrame(results)
print(res_df.to_string(index=False))
