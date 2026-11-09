# -*- coding: utf-8 -*-
"""
Trabalho 4 - Análise de Demanda do Vestibular FATEC (2022 a 2024)
Script Completo de Execução com Estratificação Populacional (São José do Rio Preto - 480k hab.)
"""

import os
import sys
import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("=" * 80)
    print(" FATEC - ANÁLISE DE DEMANDA DO VESTIBULAR (TRABALHO 4)")
    print(" ESTUDO ESTRATIFICADO: SÃO JOSÉ DO RIO PRETO (~480 MIL HABITANTES)")
    print("=" * 80)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, "demanda_vestibular.xlsx")
    
    if not os.path.exists(excel_path):
        fallback = r"C:\Users\PICHAU\.gemini\antigravity\brain\fede3023-63c1-42db-824f-ab771fa6007a\.user_uploaded\media_1794244678548_df6afad6.xlsx"
        if os.path.exists(fallback):
            excel_path = fallback
        else:
            print(f"[ERRO] Arquivo de dados não encontrado em: {excel_path}")
            return

    print(f"[*] Carregando base de dados: {excel_path}")
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    
    # Carregar aba Geral (Todos) e aba de Rio Preto (200 a 600)
    def load_sheet(sheet_name):
        ws = wb[sheet_name]
        data = []
        for r in range(2, ws.max_row + 1):
            vals = [ws.cell(r, c).value for c in range(2, 8)]
            if any(vals): data.append(vals)
        df = pd.DataFrame(data[1:], columns=['Curso', 'Periodo', 'Vestibular', 'Demanda_Media', 'Qtd', 'Eixo'])
        df['Demanda_Media'] = pd.to_numeric(df['Demanda_Media'], errors='coerce')
        df['Qtd'] = pd.to_numeric(df['Qtd'], errors='coerce')
        return df

    df_todos = load_sheet('Todos')
    df_rp = load_sheet('200 a 600')
    df_small = load_sheet('Até 200')

    print(f"[OK] Aba 'Todos' carregada: {len(df_todos)} registros.")
    print(f"[OK] Aba '200 a 600' (São José do Rio Preto ~480k hab.) carregada: {len(df_rp)} registros.")
    print(f"[OK] Aba 'Até 200' (Cidades Menores) carregada: {len(df_small)} registros.\n")

    # Exibição do Cenário Rio Preto
    print("=" * 80)
    print(" 📍 RESULTADOS OFICIAIS PARA SÃO JOSÉ DO RIO PRETO (~480k hab. / '200 a 600')")
    print("=" * 80)
    for p in ['Manhã', 'Tarde', 'Noite']:
        sub = df_rp[df_rp['Periodo'] == p]
        agg = sub.groupby('Curso').agg(
            demanda=('Demanda_Media', 'mean'),
            qtd=('Qtd', 'mean'),
            semestres=('Vestibular', 'count')
        ).reset_index()
        top = agg[agg['semestres'] >= 3].sort_values('demanda', ascending=False).head(3)
        print(f"\n>>> TURNO {p.upper()}:")
        for idx, (_, r) in enumerate(top.iterrows(), 1):
            print(f"  {idx}. {r['Curso']:<42} | Demanda: {r['demanda']:>5.2f} C/V | Qtd Unidades: {r['qtd']:>3.1f}")

    print("\n" + "=" * 80)
    print(" PROPOSTA FINAL RECOMENDADA PARA SÃO JOSÉ DO RIO PRETO")
    print("=" * 80)
    print(" * MANHÃ: Desenvolvimento de Software Multiplataforma (DSM) ou Gestão da TI (GTI)")
    print("          Demanda: 2.82 C/V (DSM) / 4.77 C/V (GTI) | Sinergia: 100% de laboratórios com ADS.")
    print(" * TARDE: Gestão Empresarial (ou DSM Vespertino)")
    print("          Demanda: 1.78 C/V (2024: 2.12 C/V) | Protege o turno vespertino e atende comércio/serviços.")
    print(" * NOITE: Análise e Desenvolvimento de Sistemas (ADS)")
    print("          Demanda: 11.61 C/V (pico 14.01 C/V) | Concorrência máxima no polo de Rio Preto.")
    print("=" * 80)

    # Re-executar build_dashboard_v3
    from build_dashboard_v3 import final_html
    print("\n[*] Painel Power BI HTML atualizado com filtros de população e Rio Preto.")
    print("[*] Abra o arquivo 'painel_powerbi.html' para visualizar a tela interativa!")

if __name__ == '__main__':
    main()
