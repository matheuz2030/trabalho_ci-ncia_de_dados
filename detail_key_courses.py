import openpyxl
import pandas as pd
import numpy as np

excel_path = r'C:\Users\PICHAU\.gemini\antigravity\brain\fede3023-63c1-42db-824f-ab771fa6007a\.user_uploaded\media_1794244678548_df6afad6.xlsx'
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

# Detail for key courses across periods
key_courses = [
    'Análise e Desenvolvimento de Sistemas',
    'Desenvolvimento de Software Multiplataforma',
    'Gestão da Tecnologia da Informação',
    'Ciência de Dados',
    'Segurança da Informação',
    'Gestão Empresarial',
    'Logística',
    'Gestão de Recursos Humanos',
    'Comércio Exterior',
    'Automação Industrial',
    'Mecanização em Agricultura de Precisão',
    'Big Data no Agronegócio',
    'Produção Cultural',
    'Produção Fonográfica',
    'Secretariado e Assessoria Internacional'
]

sub_key = df[df['Curso'].isin(key_courses)]
piv = sub_key.pivot_table(index=['Curso', 'Eixo', 'Periodo'], columns='Vestibular', values='Demanda_Media', aggfunc='mean')
sem_order = ['22.1', '22.2', '23.1', '23.2', '24.1', '24.2']
piv = piv.reindex(columns=[c for c in sem_order if c in piv.columns])
piv['Media_Geral'] = piv.mean(axis=1)
piv['Qtd_Media'] = sub_key.groupby(['Curso', 'Eixo', 'Periodo'])['Qtd'].mean()

print(piv.sort_values(by=['Periodo', 'Media_Geral'], ascending=[True, False]).round(2).to_string())
