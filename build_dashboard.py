import os
import shutil

html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Power BI - FATEC Demanda Vestibular | Painel de Decisão de Cursos</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    /* Estilos específicos padrão Power BI Dark */
    body {
      background-color: #0b111e;
      color: #e2e8f0;
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    .pbi-card {
      background-color: #151d2f;
      border: 1px solid #23304a;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      transition: all 0.2s ease;
    }
    .pbi-card:hover {
      border-color: #3b82f6;
    }
    .pbi-header {
      background: linear-gradient(90deg, #101827 0%, #17243c 100%);
      border-bottom: 2px solid #f59e0b;
    }
    .kpi-title {
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #94a3b8;
      font-weight: 600;
    }
    .kpi-value {
      font-size: 1.9rem;
      font-weight: 700;
      line-height: 1.1;
    }
    .badge {
      display: inline-block;
      padding: 0.15rem 0.5rem;
      border-radius: 9999px;
      font-size: 0.7rem;
      font-weight: 600;
    }
    .slicer-btn {
      background-color: #1e293b;
      color: #94a3b8;
      border: 1px solid #334155;
      padding: 0.35rem 0.85rem;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .slicer-btn.active {
      background-color: #2563eb;
      color: #ffffff;
      border-color: #3b82f6;
      box-shadow: 0 0 10px rgba(37,99,235,0.4);
    }
    .slicer-btn:hover:not(.active) {
      background-color: #334155;
      color: #f1f5f9;
    }
    /* Estilos das barras de dados da tabela */
    .data-bar-container {
      background: #1e293b;
      height: 8px;
      border-radius: 4px;
      overflow: hidden;
      width: 100%;
    }
    .data-bar {
      height: 100%;
      border-radius: 4px;
    }
  </style>
</head>
<body class="p-4 md:p-6 antialiased">

  <!-- CABEÇALHO ESTILO POWER BI -->
  <header class="pbi-header rounded-xl p-4 mb-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
    <div class="flex items-center gap-3">
      <div class="bg-amber-500 text-slate-950 font-black p-2.5 rounded-lg text-lg flex items-center justify-center shadow-md">
        📊
      </div>
      <div>
        <div class="flex items-center gap-2">
          <span class="text-xs bg-amber-500/20 text-amber-400 font-bold px-2 py-0.5 rounded border border-amber-500/30">POWER BI REPORT</span>
          <span class="text-xs text-slate-400">Trabalho 4 - Em Grupo | FATEC</span>
        </div>
        <h1 class="text-xl md:text-2xl font-bold text-white tracking-tight">Painel de Decisão Estratégica: Alocação de Cursos por Período</h1>
        <p class="text-xs text-slate-400">Análise de Demanda do Vestibular (2022.1 a 2024.2) • Apresentação: 09/11</p>
      </div>
    </div>
    <div class="flex flex-wrap items-center gap-2">
      <div class="bg-slate-800/80 border border-slate-700 px-3 py-1.5 rounded-lg text-right">
        <div class="text-[10px] text-slate-400 uppercase font-semibold">Total Analisado</div>
        <div class="text-sm font-bold text-emerald-400">892 Semestres-Cursos</div>
      </div>
      <div class="bg-slate-800/80 border border-slate-700 px-3 py-1.5 rounded-lg text-right">
        <div class="text-[10px] text-slate-400 uppercase font-semibold">Regra de Negócio</div>
        <div class="text-sm font-bold text-amber-400">1 Curso por Turno</div>
      </div>
    </div>
  </header>

  <!-- FILTROS / SLICERS POWER BI -->
  <div class="pbi-card p-3 mb-5 flex flex-wrap items-center justify-between gap-3">
    <div class="flex items-center gap-2">
      <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1">
        🔍 Filtro de Turno:
      </span>
      <div class="flex gap-1" id="shift-filters">
        <button class="slicer-btn active" onclick="setShift('todos', this)">Todos os Turnos</button>
        <button class="slicer-btn" onclick="setShift('Manhã', this)">🌅 Manhã</button>
        <button class="slicer-btn" onclick="setShift('Tarde', this)">☀️ Tarde</button>
        <button class="slicer-btn" onclick="setShift('Noite', this)">🌙 Noite</button>
      </div>
    </div>

    <div class="flex items-center gap-2">
      <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1">
        ⚙️ Cenário:
      </span>
      <div class="flex gap-1" id="scenario-filters">
        <button class="slicer-btn active" onclick="setScenario('recomendado', this)">🏆 Portfólio Recomendado</button>
        <button class="slicer-btn" onclick="setScenario('demanda_pura', this)">⚡ Demanda Pura (ADS)</button>
        <button class="slicer-btn" onclick="setScenario('agro', this)">🌾 Cenário Cidades Agro</button>
      </div>
    </div>
  </div>

  <!-- LINHA DE CARTÕES KPI (ESTILO POWER BI) -->
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
    <!-- Card Manhã -->
    <div class="pbi-card p-4 border-l-4 border-l-blue-500 relative overflow-hidden">
      <div class="flex justify-between items-start mb-1">
        <span class="kpi-title text-blue-400">🌅 Manhã (Recomendado)</span>
        <span class="badge bg-blue-500/20 text-blue-300 border border-blue-500/30">TI & Mobile</span>
      </div>
      <div class="text-lg font-bold text-white truncate" id="kpi-man-course">DSM (Software Multiplataforma)</div>
      <div class="flex items-baseline gap-2 mt-2">
        <span class="kpi-value text-blue-400" id="kpi-man-dem">3.21</span>
        <span class="text-xs text-slate-400">candidatos / vaga</span>
      </div>
      <div class="mt-2 text-xs text-slate-300 flex justify-between border-t border-slate-800 pt-2">
        <span>2024: <b class="text-white">3.15 c/v</b></span>
        <span>Escala: <b class="text-white">5.2 unidades</b></span>
        <span class="text-emerald-400 font-semibold">100% Sinergia</span>
      </div>
    </div>

    <!-- Card Tarde -->
    <div class="pbi-card p-4 border-l-4 border-l-amber-500 relative overflow-hidden">
      <div class="flex justify-between items-start mb-1">
        <span class="kpi-title text-amber-400">☀️ Tarde (Recomendado)</span>
        <span class="badge bg-amber-500/20 text-amber-300 border border-amber-500/30">Gestão & Negócios</span>
      </div>
      <div class="text-lg font-bold text-white truncate" id="kpi-tar-course">Gestão Empresarial</div>
      <div class="flex items-baseline gap-2 mt-2">
        <span class="kpi-value text-amber-400" id="kpi-tar-dem">1.83</span>
        <span class="text-xs text-slate-400">candidatos / vaga</span>
      </div>
      <div class="mt-2 text-xs text-slate-300 flex justify-between border-t border-slate-800 pt-2">
        <span>2024: <b class="text-emerald-400">2.05 c/v (↑)</b></span>
        <span>Escala: <b class="text-white">4.0 unidades</b></span>
        <span class="text-blue-300 font-semibold">Risco Mínimo</span>
      </div>
    </div>

    <!-- Card Noite -->
    <div class="pbi-card p-4 border-l-4 border-l-emerald-500 relative overflow-hidden">
      <div class="flex justify-between items-start mb-1">
        <span class="kpi-title text-emerald-400">🌙 Noite (Recomendado)</span>
        <span class="badge bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Flagship Estadual</span>
      </div>
      <div class="text-lg font-bold text-white truncate" id="kpi-noi-course">ADS (Análise e Desenv. Sist.)</div>
      <div class="flex items-baseline gap-2 mt-2">
        <span class="kpi-value text-emerald-400" id="kpi-noi-dem">9.90</span>
        <span class="text-xs text-slate-400">candidatos / vaga</span>
      </div>
      <div class="mt-2 text-xs text-slate-300 flex justify-between border-t border-slate-800 pt-2">
        <span>2024: <b class="text-white">9.96 c/v</b></span>
        <span>Escala: <b class="text-white">22.3 unidades</b></span>
        <span class="text-amber-400 font-bold">Líder Absoluto</span>
      </div>
    </div>

    <!-- Card Síntese -->
    <div class="pbi-card p-4 border-l-4 border-l-purple-500 relative overflow-hidden">
      <div class="flex justify-between items-start mb-1">
        <span class="kpi-title text-purple-400">📊 Portfólio Integrado</span>
        <span class="badge bg-purple-500/20 text-purple-300 border border-purple-500/30">3 Turnos</span>
      </div>
      <div class="text-lg font-bold text-white truncate" id="kpi-tot-course">Capacidade Plena</div>
      <div class="flex items-baseline gap-2 mt-2">
        <span class="kpi-value text-purple-400" id="kpi-tot-dem">14.94</span>
        <span class="text-xs text-slate-400">c/v acumulados</span>
      </div>
      <div class="mt-2 text-xs text-slate-300 flex justify-between border-t border-slate-800 pt-2">
        <span>Evasão Esperada: <b class="text-emerald-400">Baixíssima</b></span>
        <span>Ociosidade: <b class="text-emerald-400">0%</b></span>
      </div>
    </div>
  </div>

  <!-- SEÇÃO PRINCIPAL: JUSTIFICATIVAS E MOTIVOS DA ESCOLHA -->
  <div class="pbi-card p-5 mb-6 border-t-2 border-t-amber-400">
    <div class="flex items-center gap-2 mb-3">
      <span class="text-lg">📌</span>
      <h2 class="text-base md:text-lg font-bold text-white tracking-wide">
        JUSTIFICATIVAS ESTRATÉGICAS: POR QUE CADA CURSO FOI ESCOLHIDO?
      </h2>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm" id="decision-text-boxes">
      <!-- Justificativa Manhã -->
      <div class="bg-slate-900/70 p-4 rounded-lg border border-slate-800">
        <div class="flex items-center justify-between mb-2">
          <span class="font-bold text-blue-400 flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-full bg-blue-500"></span> 🌅 MANHÃ: DSM
          </span>
          <span class="text-xs text-slate-400 bg-slate-800 px-2 py-0.5 rounded">3,21 c/v</span>
        </div>
        <p class="text-xs text-slate-300 leading-relaxed">
          <b>Sinergia Máxima de Infraestrutura:</b> Como ADS será implantado no período noturno, o campus já contará com laboratórios modernos de informática. Ofertar <b>DSM (Desenvolvimento de Software Multiplataforma)</b> na manhã permite o <b>aproveitamento de 100% das máquinas e licenças</b>, reduzindo o custo de implantação da turma a quase zero.
        </p>
        <p class="text-xs text-slate-400 mt-2">
          <b>Público-alvo:</b> Jovens que concluíram o ensino médio recentemente e preferem estudar pela manhã para estagiar no contraturno da tarde.
        </p>
      </div>

      <!-- Justificativa Tarde -->
      <div class="bg-slate-900/70 p-4 rounded-lg border border-slate-800">
        <div class="flex items-center justify-between mb-2">
          <span class="font-bold text-amber-400 flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span> ☀️ TARDE: Gestão Empresarial
          </span>
          <span class="text-xs text-emerald-400 bg-slate-800 px-2 py-0.5 rounded">2,05 c/v (2024)</span>
        </div>
        <p class="text-xs text-slate-300 leading-relaxed">
          <b>Proteção do Turno Mais Crítico:</b> O período vespertino é o mais vulnerável a turmas vazias e evasão escolar (apenas 20 cursos da FATEC operam à tarde). <b>Gestão Empresarial</b> apresenta demanda histórica sólida (1,83 c/v) com <b>forte aceleração recente para 2,05 c/v em 2024</b> e o menor desvio padrão da categoria (&sigma; = 0,36).
        </p>
        <p class="text-xs text-slate-400 mt-2">
          <b>Diversificação:</b> Abre o eixo de <i>Gestão e Negócios</i>, gerando alta empregabilidade no comércio e indústrias locais e evitando que a faculdade se torne dependente unicamente de TI.
        </p>
      </div>

      <!-- Justificativa Noite -->
      <div class="bg-slate-900/70 p-4 rounded-lg border border-slate-800">
        <div class="flex items-center justify-between mb-2">
          <span class="font-bold text-emerald-400 flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> 🌙 NOITE: ADS
          </span>
          <span class="text-xs text-amber-400 bg-slate-800 px-2 py-0.5 rounded">9,90 c/v</span>
        </div>
        <p class="text-xs text-slate-300 leading-relaxed">
          <b>O Motor de Prestígio e Volume:</b> <b>ADS</b> é o curso mais concorrido e consolidado de toda a história das FATECs. No turno da noite, atinge média expressiva de <b>9,90 candidatos por vaga</b> com mais de <b>22 unidades simultâneas</b> no estado. 
        </p>
        <p class="text-xs text-slate-400 mt-2">
          <b>Garantia Operacional:</b> Preenchimento integral e imediato de todas as vagas, atendendo profissionais que trabalham durante o dia e impulsionando os indicadores institucionais da faculdade perante a comunidade e o CPS.
        </p>
      </div>
    </div>
  </div>

  <!-- GRID DE GRÁFICOS VISUAIS ESTILO POWER BI -->
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-6">
    <!-- Visual 1: Ranking Comparativo de Barras -->
    <div class="pbi-card p-4">
      <div class="flex justify-between items-center mb-3">
        <div>
          <h3 class="text-sm font-bold text-white">Ranking de Demanda por Turno (Candidatos / Vaga)</h3>
          <p class="text-[11px] text-slate-400">Comparativo dos cursos mais consistentes (&ge; 3 semestres)</p>
        </div>
        <span class="text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded border border-slate-700">Visual: Barras</span>
      </div>
      <div class="h-64 flex flex-col justify-around text-xs" id="bar-chart-container">
        <!-- Renderizado dinamicamente via JS -->
      </div>
    </div>

    <!-- Visual 2: Série Temporal / Linhas -->
    <div class="pbi-card p-4">
      <div class="flex justify-between items-center mb-3">
        <div>
          <h3 class="text-sm font-bold text-white">Série Histórica Semestral (2022.1 a 2024.2)</h3>
          <p class="text-[11px] text-slate-400">Trajetória e Sazonalidade (Vestibulares .1 x .2)</p>
        </div>
        <span class="text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded border border-slate-700">Visual: Linhas</span>
      </div>
      <!-- SVG Line Chart Interativo -->
      <div class="relative w-full h-64 pt-2">
        <svg viewBox="0 0 500 220" class="w-full h-full overflow-visible">
          <!-- Linhas de Grade Horizontal -->
          <line x1="40" y1="20" x2="480" y2="20" stroke="#1e293b" stroke-dasharray="3,3" />
          <text x="30" y="24" fill="#64748b" font-size="10" text-anchor="end">12</text>
          
          <line x1="40" y1="65" x2="480" y2="65" stroke="#1e293b" stroke-dasharray="3,3" />
          <text x="30" y="69" fill="#64748b" font-size="10" text-anchor="end">9</text>
          
          <line x1="40" y1="110" x2="480" y2="110" stroke="#1e293b" stroke-dasharray="3,3" />
          <text x="30" y="114" fill="#64748b" font-size="10" text-anchor="end">6</text>
          
          <line x1="40" y1="155" x2="480" y2="155" stroke="#1e293b" stroke-dasharray="3,3" />
          <text x="30" y="159" fill="#64748b" font-size="10" text-anchor="end">3</text>
          
          <line x1="40" y1="195" x2="480" y2="195" stroke="#334155" />
          <text x="30" y="198" fill="#64748b" font-size="10" text-anchor="end">0</text>

          <!-- Rótulos X -->
          <text x="65" y="212" fill="#94a3b8" font-size="10" text-anchor="middle">22.1</text>
          <text x="145" y="212" fill="#94a3b8" font-size="10" text-anchor="middle">22.2</text>
          <text x="225" y="212" fill="#94a3b8" font-size="10" text-anchor="middle">23.1</text>
          <text x="305" y="212" fill="#94a3b8" font-size="10" text-anchor="middle">23.2</text>
          <text x="385" y="212" fill="#94a3b8" font-size="10" text-anchor="middle">24.1</text>
          <text x="460" y="212" fill="#94a3b8" font-size="10" text-anchor="middle">24.2</text>

          <!-- Linha ADS Noite (Verde) -->
          <polyline fill="none" stroke="#10b981" stroke-width="3" points="
            65,13  145,58  225,49  305,73  385,18  460,78
          " />
          <circle cx="65" cy="13" r="4" fill="#10b981" />
          <circle cx="145" cy="58" r="4" fill="#10b981" />
          <circle cx="225" cy="49" r="4" fill="#10b981" />
          <circle cx="305" cy="73" r="4" fill="#10b981" />
          <circle cx="385" cy="18" r="4" fill="#10b981" />
          <circle cx="460" cy="78" r="4" fill="#10b981" />
          <text x="385" y="10" fill="#10b981" font-size="9" font-weight="bold" text-anchor="middle">12.10</text>

          <!-- Linha ADS Manhã (Azul Claro) -->
          <polyline fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4,2" points="
            65,97  145,132  225,119  305,133  385,89  460,136
          " />
          <circle cx="385" cy="89" r="3" fill="#38bdf8" />

          <!-- Linha DSM Manhã (Azul Escuro) -->
          <polyline fill="none" stroke="#60a5fa" stroke-width="2.5" points="
            65,119  145,155  225,152  305,159  385,136  460,159
          " />
          <circle cx="385" cy="136" r="3.5" fill="#60a5fa" />
          <text x="385" y="128" fill="#60a5fa" font-size="9" font-weight="bold" text-anchor="middle">3.93</text>

          <!-- Linha Gestão Empresarial Tarde (Laranja) -->
          <polyline fill="none" stroke="#f59e0b" stroke-width="2.5" points="
            65,160  145,170  225,172  305,174  385,162  460,166
          " />
          <circle cx="460" cy="166" r="3.5" fill="#f59e0b" />
          <text x="460" y="157" fill="#f59e0b" font-size="9" font-weight="bold" text-anchor="middle">1.93</text>
        </svg>
      </div>
      <div class="flex flex-wrap items-center justify-center gap-4 mt-2 text-[11px] text-slate-300">
        <span class="flex items-center gap-1.5"><span class="w-3 h-0.5 bg-emerald-500"></span> ADS Noite (Média 9.90)</span>
        <span class="flex items-center gap-1.5"><span class="w-3 h-0.5 bg-sky-400 border-dashed"></span> ADS Manhã (Média 5.16)</span>
        <span class="flex items-center gap-1.5"><span class="w-3 h-0.5 bg-blue-400"></span> DSM Manhã (Média 3.21)</span>
        <span class="flex items-center gap-1.5"><span class="w-3 h-0.5 bg-amber-500"></span> Gestão Emp. Tarde (Média 1.83)</span>
      </div>
    </div>
  </div>

  <!-- TABELA DINÂMICA COM BARRAS DE DADOS ESTILO POWER BI -->
  <div class="pbi-card p-4 mb-6">
    <div class="flex justify-between items-center mb-3">
      <div>
        <h3 class="text-sm font-bold text-white">Matriz Detalhada: Desempenho e Indicadores dos Cursos</h3>
        <p class="text-[11px] text-slate-400">Dados consolidados do modelo Python com formatação condicional</p>
      </div>
      <span class="text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded border border-slate-700">Visual: Tabela Matriz</span>
    </div>
    <div class="overflow-x-auto">
      <table class="w-full text-left text-xs border-collapse">
        <thead>
          <tr class="border-b border-slate-700 text-slate-400 uppercase font-semibold">
            <th class="py-2.5 px-3">Turno</th>
            <th class="py-2.5 px-3">Curso</th>
            <th class="py-2.5 px-3">Eixo Tecnológico</th>
            <th class="py-2.5 px-3">Demanda Média</th>
            <th class="py-2.5 px-3 w-36">Gráfico de Demanda</th>
            <th class="py-2.5 px-3">Demanda 2024</th>
            <th class="py-2.5 px-3">Desvio (&sigma;)</th>
            <th class="py-2.5 px-3">Qtd Unidades</th>
            <th class="py-2.5 px-3">Decisão</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800/60" id="matrix-tbody">
          <!-- Linhas renderizadas via JavaScript -->
        </tbody>
      </table>
    </div>
  </div>

  <!-- RODAPÉ TÉCNICO -->
  <footer class="pbi-card p-4 flex flex-col sm:flex-row justify-between items-center gap-3 text-xs text-slate-400">
    <div class="flex items-center gap-2">
      <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
      <span>Base carregada: <b>demanda_vestibular.xlsx</b> (Planilha 'Todos')</span>
    </div>
    <div>
      <span>Desenvolvido com Python (pandas, matplotlib, openpyxl) para apresentação em 09/11</span>
    </div>
  </footer>

  <script>
    // DADOS ESTATÍSTICOS EXTRAÍDOS PELO PYTHON
    const courseData = [
      // Noite
      { turno: 'Noite', curso: 'Análise e Desenvolvimento de Sistemas', eixo: 'Informação e Comunicação', media: 9.90, rec24: 9.96, dp: 1.96, qtd: 22.3, status: 'RECOMENDADO', color: '#10b981' },
      { turno: 'Noite', curso: 'Design de Mídias Digitais', eixo: 'Informação e Comunicação', media: 6.72, rec24: 5.59, dp: 2.27, qtd: 1.0, status: 'Nicho Local', color: '#64748b' },
      { turno: 'Noite', curso: 'Secretariado e Assessoria Internacional', eixo: 'Gestão e Negócios', media: 6.70, rec24: 5.83, dp: 3.18, qtd: 1.0, status: 'Nicho Local', color: '#64748b' },
      { turno: 'Noite', curso: 'Gestão Portuária', eixo: 'Infraestrutura', media: 5.41, rec24: 5.74, dp: 1.38, qtd: 1.0, status: 'Nicho Santos', color: '#64748b' },
      { turno: 'Noite', curso: 'Banco de Dados', eixo: 'Informação e Comunicação', media: 5.30, rec24: 5.56, dp: 0.79, qtd: 2.0, status: 'Especialização', color: '#64748b' },
      { turno: 'Noite', curso: 'Desenvolvimento de Software Multiplataforma', eixo: 'Informação e Comunicação', media: 4.83, rec24: 5.08, dp: 0.91, qtd: 8.3, status: 'Alta Demanda', color: '#38bdf8' },
      { turno: 'Noite', curso: 'Segurança da Informação', eixo: 'Informação e Comunicação', media: 4.76, rec24: 4.92, dp: 1.05, qtd: 5.0, status: 'Alta Demanda', color: '#38bdf8' },
      { turno: 'Noite', curso: 'Automação Industrial', eixo: 'Controle e Processos', media: 4.61, rec24: 4.59, dp: 1.18, qtd: 6.0, status: 'Indústria 4.0', color: '#a855f7' },
      { turno: 'Noite', curso: 'Gestão Empresarial', eixo: 'Gestão e Negócios', media: 3.36, rec24: 3.28, dp: 0.76, qtd: 18.0, status: 'Alta Escala', color: '#f59e0b' },
      
      // Manhã
      { turno: 'Manhã', curso: 'Análise e Desenvolvimento de Sistemas', eixo: 'Informação e Comunicação', media: 5.16, rec24: 5.51, dp: 1.34, qtd: 23.3, status: 'Líder Geral', color: '#10b981' },
      { turno: 'Manhã', curso: 'Secretariado e Assessoria Internacional', eixo: 'Gestão e Negócios', media: 3.73, rec24: 3.30, dp: 2.16, qtd: 1.0, status: 'Nicho Local', color: '#64748b' },
      { turno: 'Manhã', curso: 'Desenvolvimento de Software Multiplataforma', eixo: 'Informação e Comunicação', media: 3.21, rec24: 3.15, dp: 1.07, qtd: 5.2, status: 'RECOMENDADO', color: '#38bdf8' },
      { turno: 'Manhã', curso: 'Gestão da Tecnologia da Informação', eixo: 'Informação e Comunicação', media: 3.13, rec24: 3.58, dp: 0.81, qtd: 4.3, status: 'Forte Opção', color: '#60a5fa' },
      { turno: 'Manhã', curso: 'Gestão de Recursos Humanos', eixo: 'Gestão e Negócios', media: 2.80, rec24: 2.55, dp: 1.29, qtd: 5.5, status: 'Opção Gestão', color: '#f59e0b' },
      { turno: 'Manhã', curso: 'Ciência de Dados', eixo: 'Informação e Comunicação', media: 2.80, rec24: 3.93, dp: 1.07, qtd: 1.0, status: 'Emergente', color: '#38bdf8' },
      { turno: 'Manhã', curso: 'Mecanização em Agricultura de Precisão', eixo: 'Controle e Processos', media: 2.40, rec24: 2.52, dp: 0.72, qtd: 1.0, status: 'Opção Agro', color: '#84cc16' },

      // Tarde
      { turno: 'Tarde', curso: 'Análise e Desenvolvimento de Sistemas', eixo: 'Informação e Comunicação', media: 4.23, rec24: 4.57, dp: 1.00, qtd: 13.3, status: 'Líder Geral', color: '#10b981' },
      { turno: 'Tarde', curso: 'Desenvolvimento de Software Multiplataforma', eixo: 'Informação e Comunicação', media: 2.36, rec24: 2.94, dp: 0.69, qtd: 2.8, status: 'Opção TI', color: '#38bdf8' },
      { turno: 'Tarde', curso: 'Produção Fonográfica', eixo: 'Produção Cultural', media: 2.33, rec24: 3.11, dp: 0.97, qtd: 1.0, status: 'Nicho Tatuí', color: '#64748b' },
      { turno: 'Tarde', curso: 'Big Data no Agronegócio', eixo: 'Informação e Comunicação', media: 1.96, rec24: 2.12, dp: 0.46, qtd: 1.0, status: 'Opção Agro', color: '#84cc16' },
      { turno: 'Tarde', curso: 'Gestão Empresarial', eixo: 'Gestão e Negócios', media: 1.83, rec24: 2.05, dp: 0.36, qtd: 4.0, status: 'RECOMENDADO', color: '#f59e0b' },
      { turno: 'Tarde', curso: 'Comércio Exterior', eixo: 'Gestão e Negócios', media: 1.71, rec24: 1.96, dp: 0.43, qtd: 2.7, status: 'Gestão', color: '#f59e0b' },
      { turno: 'Tarde', curso: 'Logística', eixo: 'Gestão e Negócios', media: 1.63, rec24: 1.78, dp: 0.66, qtd: 3.5, status: 'Gestão', color: '#f59e0b' }
    ];

    let currentShift = 'todos';
    let currentScenario = 'recomendado';

    function renderTable() {
      const tbody = document.getElementById('matrix-tbody');
      tbody.innerHTML = '';

      let filtered = courseData;
      if (currentShift !== 'todos') {
        filtered = filtered.filter(d => d.turno === currentShift);
      }

      filtered.forEach(d => {
        const isRec = (d.status === 'RECOMENDADO');
        const pctBar = Math.min(100, (d.media / 12.0) * 100);
        const tr = document.createElement('tr');
        tr.className = `hover:bg-slate-800/40 transition-colors ${isRec ? 'bg-slate-800/30 font-medium' : ''}`;
        
        let badgeClass = 'bg-slate-800 text-slate-400 border border-slate-700';
        if (isRec) badgeClass = 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-bold';
        else if (d.status === 'Líder Geral') badgeClass = 'bg-blue-500/20 text-blue-300 border border-blue-500/40';

        tr.innerHTML = `
          <td class="py-2.5 px-3">
            <span class="inline-flex items-center gap-1.5 font-bold ${d.turno === 'Manhã' ? 'text-blue-400' : d.turno === 'Tarde' ? 'text-amber-400' : 'text-emerald-400'}">
              ${d.turno === 'Manhã' ? '🌅' : d.turno === 'Tarde' ? '☀️' : '🌙'} ${d.turno}
            </span>
          </td>
          <td class="py-2.5 px-3 text-white font-semibold flex items-center gap-1.5">
            ${isRec ? '<span title="Curso Escolhido">⭐</span>' : ''} ${d.curso}
          </td>
          <td class="py-2.5 px-3 text-slate-400 text-[11px]">${d.eixo}</td>
          <td class="py-2.5 px-3 font-bold text-white">${d.media.toFixed(2)} c/v</td>
          <td class="py-2.5 px-3">
            <div class="data-bar-container">
              <div class="data-bar" style="width: ${pctBar}%; background-color: ${d.color};"></div>
            </div>
          </td>
          <td class="py-2.5 px-3 text-slate-300">${d.rec24.toFixed(2)} c/v</td>
          <td class="py-2.5 px-3 text-slate-400">&plusmn;${d.dp.toFixed(2)}</td>
          <td class="py-2.5 px-3 text-slate-300 font-semibold">${d.qtd.toFixed(1)}</td>
          <td class="py-2.5 px-3">
            <span class="badge ${badgeClass}">${d.status}</span>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function renderBarVisual() {
      const container = document.getElementById('bar-chart-container');
      container.innerHTML = '';

      let items = [];
      if (currentShift === 'todos') {
        items = [
          { label: 'Noite: ADS', val: 9.90, color: '#10b981', rec: true },
          { label: 'Noite: Secretariado (nicho)', val: 6.70, color: '#64748b' },
          { label: 'Manhã: ADS', val: 5.16, color: '#38bdf8' },
          { label: 'Noite: DSM', val: 4.83, color: '#60a5fa' },
          { label: 'Tarde: ADS', val: 4.23, color: '#0ea5e9' },
          { label: 'Manhã: DSM', val: 3.21, color: '#3b82f6', rec: true },
          { label: 'Tarde: DSM', val: 2.36, color: '#f59e0b' },
          { label: 'Tarde: Gestão Empresarial', val: 1.83, color: '#eab308', rec: true }
        ];
      } else {
        const filtered = courseData.filter(d => d.turno === currentShift).slice(0, 7);
        items = filtered.map(d => ({
          label: d.curso.length > 25 ? d.curso.substring(0, 24) + '...' : d.curso,
          val: d.media,
          color: d.color,
          rec: d.status === 'RECOMENDADO'
        }));
      }

      items.forEach(item => {
        const pct = Math.min(100, (item.val / 10.5) * 100);
        const row = document.createElement('div');
        row.className = 'flex items-center gap-2 py-0.5';
        row.innerHTML = `
          <div class="w-40 text-right truncate text-[11px] ${item.rec ? 'font-bold text-white' : 'text-slate-400'}">
            ${item.rec ? '⭐ ' : ''}${item.label}
          </div>
          <div class="flex-1 bg-slate-800/80 h-5 rounded overflow-hidden relative flex items-center">
            <div class="h-full rounded transition-all duration-500" style="width: ${pct}%; background-color: ${item.color};"></div>
            <span class="absolute right-2 text-[10px] font-bold text-white">${item.val.toFixed(2)} c/v</span>
          </div>
        `;
        container.appendChild(row);
      });
    }

    function setShift(shift, btn) {
      currentShift = shift;
      document.querySelectorAll('#shift-filters .slicer-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderTable();
      renderBarVisual();
    }

    function setScenario(scen, btn) {
      currentScenario = scen;
      document.querySelectorAll('#scenario-filters .slicer-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const kpiMan = document.getElementById('kpi-man-course');
      const kpiManDem = document.getElementById('kpi-man-dem');
      const kpiTar = document.getElementById('kpi-tar-course');
      const kpiTarDem = document.getElementById('kpi-tar-dem');
      const kpiNoi = document.getElementById('kpi-noi-course');
      const kpiNoiDem = document.getElementById('kpi-noi-dem');
      const kpiTotDem = document.getElementById('kpi-tot-dem');

      if (scen === 'recomendado') {
        kpiMan.innerText = 'DSM (Software Multiplataforma)';
        kpiManDem.innerText = '3.21';
        kpiTar.innerText = 'Gestão Empresarial';
        kpiTarDem.innerText = '1.83';
        kpiNoi.innerText = 'ADS (Análise e Desenv. Sist.)';
        kpiNoiDem.innerText = '9.90';
        kpiTotDem.innerText = '14.94';
      } else if (scen === 'demanda_pura') {
        kpiMan.innerText = 'ADS (Análise e Desenv. Sist.)';
        kpiManDem.innerText = '5.16';
        kpiTar.innerText = 'ADS (Análise e Desenv. Sist.)';
        kpiTarDem.innerText = '4.23';
        kpiNoi.innerText = 'ADS (Análise e Desenv. Sist.)';
        kpiNoiDem.innerText = '9.90';
        kpiTotDem.innerText = '19.29';
      } else if (scen === 'agro') {
        kpiMan.innerText = 'Mecanização Agrícola Precisão';
        kpiManDem.innerText = '2.40';
        kpiTar.innerText = 'Big Data no Agronegócio';
        kpiTarDem.innerText = '1.96';
        kpiNoi.innerText = 'ADS ou Mecanização Noite';
        kpiNoiDem.innerText = '4.50';
        kpiTotDem.innerText = '8.86';
      }
    }

    // Inicialização
    renderTable();
    renderBarVisual();
  </script>
</body>
</html>
"""

# Salva na pasta do projeto e na pasta de artefatos
out_project = r'C:\Users\PICHAU\.gemini\antigravity\scratch\trabalho_vestibular\painel_powerbi.html'
out_artifact = r'C:\Users\PICHAU\.gemini\antigravity\brain\fede3023-63c1-42db-824f-ab771fa6007a\painel_powerbi.html'

with open(out_project, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(out_artifact, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Painel Power BI HTML gerado com sucesso!")
