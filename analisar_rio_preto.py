import openpyxl
import pandas as pd
import numpy as np

excel_path = r'C:\Users\PICHAU\.gemini\antigravity\scratch\trabalho_vestibular\demanda_vestibular.xlsx'
wb = openpyxl.load_workbook(excel_path, data_only=True)

sheets = ['Todos', 'Até 100', 'Até 200', 'Até 500', 'Até 600', '100 a 600', '200 a 600']

pop_summary = {}

for s in wb.sheetnames:
    if 'Popula' in s: continue
    ws = wb[s]
    data = []
    for r in range(2, ws.max_row+1):
        vals = [ws.cell(r, c).value for c in range(2, 8)]
        if any(vals): data.append(vals)
    df = pd.DataFrame(data[1:], columns=['Curso', 'Periodo', 'Vestibular', 'Demanda_Media', 'Qtd', 'Eixo'])
    df['Demanda_Media'] = pd.to_numeric(df['Demanda_Media'])
    df['Qtd'] = pd.to_numeric(df['Qtd'])
    
    pop_summary[s] = df

print("Abas disponíveis na planilha:")
for s in pop_summary.keys():
    print(f"- {s} ({len(pop_summary[s])} linhas)")

# Rio Preto: ~480.000 habitantes
# Portanto, Rio Preto se enquadra perfeitamente nas abas:
# 'Até 500', 'Até 600', '100 a 600' e '200 a 600'
print("\n" + "="*80)
print("COMPARAÇÃO ESPECÍFICA: RIO PRETO (~480k hab.) vs OUTROS PORTES")
print("="*80)

compare_sheets = ['Até 100', 'Até 200', 'Até 500', '200 a 600', 'Todos']

for s in compare_sheets:
    df = pop_summary[s]
    print(f"\n--- FAIXA POPULACIONAL: {s.upper()} ---")
    for p in ['Manhã', 'Tarde', 'Noite']:
        sub = df[df['Periodo'] == p]
        agg = sub.groupby('Curso').agg(
            demanda=('Demanda_Media', 'mean'),
            semestres=('Vestibular', 'count'),
            qtd=('Qtd', 'mean')
        ).reset_index()
        top = agg[agg['semestres'] >= 3].sort_values('demanda', ascending=False).head(4)
        items = [f"{r['Curso']} (Dem: {r['demanda']:.2f} | Qtd: {r['qtd']:.1f})" for _, r in top.iterrows()]
        print(f"  {p:6s}: " + " | ".join(items))
