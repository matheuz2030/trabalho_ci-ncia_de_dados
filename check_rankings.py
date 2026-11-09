import openpyxl
import pandas as pd
import numpy as np

excel_path = r'C:\Users\PICHAU\.gemini\antigravity\scratch\trabalho_vestibular\demanda_vestibular.xlsx'
wb = openpyxl.load_workbook(excel_path, data_only=True)

sheets = ['200 a 600', 'Até 500', 'Até 200', 'Até 100', 'Todos']

for s in sheets:
    ws = wb[s]
    data = [[ws.cell(r, c).value for c in range(2, 8)] for r in range(2, ws.max_row+1)]
    df = pd.DataFrame(data[1:], columns=['Curso', 'Periodo', 'Vestibular', 'Demanda_Media', 'Qtd', 'Eixo'])
    df['Demanda_Media'] = pd.to_numeric(df['Demanda_Media'])
    df['Qtd'] = pd.to_numeric(df['Qtd'])
    
    print(f"\n==================== ABA: {s} ====================")
    for p in ['Manhã', 'Tarde', 'Noite']:
        sub = df[df['Periodo'] == p]
        agg = sub.groupby('Curso').agg(
            demanda=('Demanda_Media', 'mean'),
            semestres=('Vestibular', 'count'),
            qtd=('Qtd', 'mean')
        ).reset_index()
        # Sort by demand
        top = agg[agg['semestres'] >= 3].sort_values('demanda', ascending=False).head(5)
        print(f"--- {p.upper()} ---")
        for rank, (_, r) in enumerate(top.iterrows(), 1):
            print(f"  {rank}º: {r['Curso']:<42} | Demanda: {r['demanda']:>5.2f} C/V | Qtd: {r['qtd']:>4.1f} un.")
