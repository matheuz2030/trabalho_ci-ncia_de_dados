import openpyxl
import pandas as pd

excel_path = r'C:\Users\PICHAU\.gemini\antigravity\scratch\trabalho_vestibular\demanda_vestibular.xlsx'
wb = openpyxl.load_workbook(excel_path, data_only=True)

# Compare Até 100 vs Até 200
ws100 = wb['Até 100']
ws200 = wb['Até 200']

data100 = [[ws100.cell(r, c).value for c in range(2, 8)] for r in range(2, ws100.max_row+1)]
data200 = [[ws200.cell(r, c).value for c in range(2, 8)] for r in range(2, ws200.max_row+1)]

df100 = pd.DataFrame(data100[1:], columns=data100[0])
df200 = pd.DataFrame(data200[1:], columns=data200[0])

print('Shape Até 100:', df100.shape)
print('Shape Até 200:', df200.shape)
print('Are df100 and df200 identical in the original Excel file?')
print(df100.equals(df200))

print('\nComparing all sheets in Excel:')
for s in ['Até 100', 'Até 200', 'Até 500', 'Até 600', '100 a 600', '200 a 600', 'Todos']:
    ws = wb[s]
    d = [[ws.cell(r, c).value for c in range(2, 8)] for r in range(2, ws.max_row+1)]
    df_s = pd.DataFrame(d[1:], columns=d[0])
    df_s.columns = [str(c).strip() for c in df_s.columns]
    col_dem = [c for c in df_s.columns if 'Demanda' in c][0]
    col_cur = [c for c in df_s.columns if 'Curso' in c][0]
    col_per = [c for c in df_s.columns if 'Per' in c][0]
    col_vest = [c for c in df_s.columns if 'Vest' in c][0]
    
    df_s[col_dem] = pd.to_numeric(df_s[col_dem])
    ads_noite = df_s[(df_s[col_cur].str.contains('Desenvolvimento de Sistemas', na=False)) & (df_s[col_per] == 'Noite')]
    m = ads_noite[col_dem].mean()
    v24_1 = ads_noite[df_s[col_vest] == '24.1'][col_dem].values
    print(f"Sheet {s:12s}: rows={len(df_s)} | ADS Noite Mean={m:.2f} | 24.1={v24_1}")
