import json
import os

with open(r'C:\Users\PICHAU\.gemini\antigravity\scratch\trabalho_vestibular\pop_tiers_data.json', 'r', encoding='utf-8') as f:
    pop_data = json.load(f)

json_str = json.dumps(pop_data, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Power BI - FATEC Demanda Vestibular | Painel de Decisão Estratégica (Rio Preto & População)</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
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
      font-size: 1.85rem;
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
      padding: 0.35rem 0.75rem;
      border-radius: 6px;
      font-size: 0.78rem;
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
    .pop-btn {
      border-color: #0284c7;
    }
    .pop-btn.active {
      background-color: #0284c7 !important;
      border-color: #38bdf8 !important;
      box-shadow: 0 0 12px rgba(2,132,199,0.5) !important;
      color: #ffffff !important;
    }
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
    .tooltip-box {
      position: absolute;
      background: #0f172a;
      border: 1px solid #38bdf8;
      border-radius: 6px;
      padding: 6px 10px;
      font-size: 11px;
      color: white;
      pointer-events: none;
      display: none;
      z-index: 50;
      box-shadow: 0 4px 14px rgba(0,0,0,0.6);
    }
  </style>
</head>
<body class="p-4 md:p-6 antialiased">

  <div id="line-tooltip" class="tooltip-box"></div>

  <!-- CABEÇALHO POWER BI -->
  <header class="pbi-header rounded-xl p-4 mb-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
    <div class="flex items-center gap-3">
      <div class="bg-amber-500 text-slate-950 font-black p-2.5 rounded-lg text-lg flex items-center justify-center shadow-md">
        📊
      </div>
      <div>
        <div class="flex items-center gap-2">
          <span class="text-xs bg-amber-500/20 text-amber-400 font-bold px-2 py-0.5 rounded border border-amber-500/30">POWER BI REPORT</span>
          <span class="text-xs bg-cyan-500/20 text-cyan-300 font-bold px-2 py-0.5 rounded border border-cyan-500/30">ESTUDO: SÃO JOSÉ DO RIO PRETO (~480k hab.)</span>
          <span class="text-xs text-slate-400">Trabalho 4 - FATEC</span>
        </div>
        <h1 class="text-xl md:text-2xl font-bold text-white tracking-tight">Painel de Decisão de Cursos: Análise por Porte Populacional & Turno</h1>
        <p class="text-xs text-slate-400">Demanda Real dos Vestibulares FATEC (2022.1 a 2024.2) • Foco na População de São José do Rio Preto</p>
      </div>
    </div>
    <div class="flex flex-wrap items-center gap-2">
      <div class="bg-slate-800/80 border border-slate-700 px-3 py-1.5 rounded-lg text-right">
        <div class="text-[10px] text-slate-400 uppercase font-semibold">Cidade-Foco</div>
        <div class="text-sm font-bold text-cyan-400">S. J. Rio Preto (480k hab.)</div>
      </div>
      <div class="bg-slate-800/80 border border-slate-700 px-3 py-1.5 rounded-lg text-right">
        <div class="text-[10px] text-slate-400 uppercase font-semibold">Regra do Trabalho</div>
        <div class="text-sm font-bold text-amber-400">1 Curso por Turno</div>
      </div>
    </div>
  </header>

  <!-- BARRA DE SEGMENTADORES (SLICERS) ESTILO POWER BI -->
  <div class="pbi-card p-3 mb-4 space-y-3">
    <!-- Linha 1: Filtro de População / Cidade -->
    <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-2.5">
      <div class="flex flex-wrap items-center gap-2">
        <span class="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1">
          🏢 Filtro de População (Porte da Cidade):
        </span>
        <div class="flex flex-wrap gap-1" id="pop-filters">
          <button class="slicer-btn pop-btn active" onclick="setPopTier('rio_preto_200_600', this)">
            📍 São José do Rio Preto (~480k hab. / 200k a 600k)
          </button>
          <button class="slicer-btn pop-btn" onclick="setPopTier('ate_500', this)">Até 500 mil hab.</button>
          <button class="slicer-btn pop-btn" onclick="setPopTier('ate_200', this)">Até 200 mil hab.</button>
          <button class="slicer-btn pop-btn" onclick="setPopTier('ate_100', this)">Até 100 mil hab.</button>
          <button class="slicer-btn pop-btn" onclick="setPopTier('todos', this)">🌐 Todos (Estado Geral)</button>
        </div>
      </div>
      <div class="text-[11px] text-slate-400 bg-slate-800 px-2.5 py-1 rounded border border-slate-700">
        Aba selecionada no Excel: <b class="text-white" id="active-sheet-indicator">200 a 600</b>
      </div>
    </div>

    <!-- Linha 2: Filtro de Turno e Cenário -->
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div class="flex items-center gap-2">
        <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1">
          🌅 Turno:
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
          🎯 Cenário:
        </span>
        <div class="flex gap-1" id="scenario-filters">
          <button class="slicer-btn active" onclick="setScenario('recomendado', this)">🏆 Recomendação Oficial</button>
          <button class="slicer-btn" onclick="setScenario('demanda_pura', this)">⚡ Demanda Pura (ADS)</button>
        </div>
      </div>
    </div>
  </div>

  <!-- CARDS DE KPI -->
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-5">
    <div class="pbi-card p-4 border-l-4 border-l-blue-500 relative overflow-hidden">
      <div class="flex justify-between items-start mb-1">
        <span class="kpi-title text-blue-400">🌅 Manhã (Recomendado)</span>
        <span class="badge bg-blue-500/20 text-blue-300 border border-blue-500/30">TI & Mobile</span>
      </div>
      <div class="text-lg font-bold text-white truncate" id="kpi-man-course">DSM (Software Multiplataforma)</div>
      <div class="flex items-baseline gap-2 mt-2">
        <span class="kpi-value text-blue-400" id="kpi-man-dem">2.82</span>
        <span class="text-xs text-slate-400">C/V (Candidatos/Vaga)</span>
      </div>
      <div class="mt-2 text-xs text-slate-300 flex justify-between border-t border-slate-800 pt-2" id="kpi-man-sub">
        <span>GTI Manhã: <b class="text-white">4.77 C/V</b></span>
        <span>Sinergia: <b class="text-emerald-400">100%</b></span>
      </div>
    </div>

    <div class="pbi-card p-4 border-l-4 border-l-amber-500 relative overflow-hidden">
      <div class="flex justify-between items-start mb-1">
        <span class="kpi-title text-amber-400">☀️ Tarde (Recomendado)</span>
        <span class="badge bg-amber-500/20 text-amber-300 border border-amber-500/30">Gestão & Negócios</span>
      </div>
      <div class="text-lg font-bold text-white truncate" id="kpi-tar-course">Gestão Empresarial</div>
      <div class="flex items-baseline gap-2 mt-2">
        <span class="kpi-value text-amber-400" id="kpi-tar-dem">1.78</span>
        <span class="text-xs text-slate-400">C/V (Candidatos/Vaga)</span>
      </div>
      <div class="mt-2 text-xs text-slate-300 flex justify-between border-t border-slate-800 pt-2" id="kpi-tar-sub">
        <span>2024: <b class="text-emerald-400">2.12 C/V (↑)</b></span>
        <span>Risco: <b class="text-blue-300">Mínimo</b></span>
      </div>
    </div>

    <div class="pbi-card p-4 border-l-4 border-l-emerald-500 relative overflow-hidden">
      <div class="flex justify-between items-start mb-1">
        <span class="kpi-title text-emerald-400">🌙 Noite (Recomendado)</span>
        <span class="badge bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Líder Regional</span>
      </div>
      <div class="text-lg font-bold text-white truncate" id="kpi-noi-course">ADS (Análise e Desenv. Sist.)</div>
      <div class="flex items-baseline gap-2 mt-2">
        <span class="kpi-value text-emerald-400" id="kpi-noi-dem">11.61</span>
        <span class="text-xs text-slate-400">C/V (Candidatos/Vaga)</span>
      </div>
      <div class="mt-2 text-xs text-slate-300 flex justify-between border-t border-slate-800 pt-2" id="kpi-noi-sub">
        <span>Pico: <b class="text-white">14.01 C/V</b></span>
        <span>Escala: <b class="text-amber-400 font-bold">Recorde</b></span>
      </div>
    </div>

    <div class="pbi-card p-4 border-l-4 border-l-purple-500 relative overflow-hidden">
      <div class="flex justify-between items-start mb-1">
        <span class="kpi-title text-purple-400">📊 Total Combinado</span>
        <span class="badge bg-purple-500/20 text-purple-300 border border-purple-500/30">3 Turnos</span>
      </div>
      <div class="text-lg font-bold text-white truncate" id="kpi-tot-course">Capacidade Plena</div>
      <div class="flex items-baseline gap-2 mt-2">
        <span class="kpi-value text-purple-400" id="kpi-tot-dem">16.21</span>
        <span class="text-xs text-slate-400">C/V Acumulados</span>
      </div>
      <div class="mt-2 text-xs text-slate-300 flex justify-between border-t border-slate-800 pt-2">
        <span>Ociosidade: <b class="text-emerald-400">0%</b></span>
        <span>Retenção: <b class="text-emerald-400">Máxima</b></span>
      </div>
    </div>
  </div>

  <!-- DICIONÁRIO DE TERMOS & GLOSSÁRIO (O QUE É C/V?) -->
  <div class="pbi-card p-4 mb-4 border-l-4 border-l-cyan-500 bg-slate-900/90">
    <div class="flex items-center justify-between mb-1.5 cursor-pointer" onclick="toggleGlossary()">
      <div class="flex items-center gap-2">
        <span class="text-base text-cyan-400">📚</span>
        <h3 class="text-xs font-bold text-white uppercase tracking-wider">
          Dicionário de Indicadores: O que significam C/V, Qtd, População de Rio Preto e Eixo?
        </h3>
      </div>
      <span class="text-[11px] text-cyan-400 font-semibold" id="glossary-toggle-btn">[Clique para recolher/expandir]</span>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs pt-2 border-t border-slate-800" id="glossary-content">
      <div class="bg-slate-800/60 p-2.5 rounded border border-slate-700/60">
        <div class="font-bold text-cyan-300 text-xs mb-1">🎯 C/V (Candidatos por Vaga)</div>
        <p class="text-slate-300 leading-relaxed text-[11px]">
          Relação de concorrência: <b>Inscritos ÷ Vagas</b>.
          <br><b>Exemplo em Rio Preto:</b> Em ADS Noite, a demanda é de <b>11,61 C/V</b>. Significa que para 40 vagas, inscrevem-se <b>464 candidatos</b> (quase 12 por vaga!).
        </p>
      </div>

      <div class="bg-slate-800/60 p-2.5 rounded border border-slate-700/60">
        <div class="font-bold text-emerald-300 text-xs mb-1">📍 São José do Rio Preto (População)</div>
        <p class="text-slate-300 leading-relaxed text-[11px]">
          Com <b>~480 mil habitantes</b> (IBGE), Rio Preto é classificada na planilha nas abas <b>"200 a 600"</b> e <b>"Até 500"</b>. É um polo regional de comércio, saúde e serviços com fortíssima demanda por TI e Gestão.
        </p>
      </div>

      <div class="bg-slate-800/60 p-2.5 rounded border border-slate-700/60">
        <div class="font-bold text-amber-300 text-xs mb-1">🏫 Cidades Menores (&lt;200k hab.)</div>
        <p class="text-slate-300 leading-relaxed text-[11px]">
          Em cidades de até 100k e 200k hab., a vocação agropecuária se destaca fortemente: <b>Mecanização em Agricultura de Precisão</b> (4,38 C/V) e <b>Big Data no Agro</b> (1,96 C/V à tarde).
        </p>
      </div>

      <div class="bg-slate-800/60 p-2.5 rounded border border-slate-700/60">
        <div class="font-bold text-purple-300 text-xs mb-1">🔬 Sinergia de Laboratórios</div>
        <p class="text-slate-300 leading-relaxed text-[11px]">
          Ao alocar <b>DSM na Manhã</b> e <b>ADS na Noite</b>, a faculdade usa 100% dos mesmos laboratórios de informática nos dois turnos, reduzindo o custo de implantação da turma a zero.
        </p>
      </div>
    </div>
  </div>

  <!-- JUSTIFICATIVAS ESTRATÉGICAS COM BASE NA POPULAÇÃO -->
  <div class="pbi-card p-4 mb-4 border-t-2 border-t-amber-400">
    <div class="flex items-center gap-2 mb-2.5">
      <span class="text-base">📌</span>
      <h2 class="text-sm md:text-base font-bold text-white tracking-wide" id="justification-header">
        JUSTIFICATIVAS ESTRATÉGICAS: CENÁRIO SÃO JOSÉ DO RIO PRETO (~480k hab.)
      </h2>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs" id="decision-text-boxes">
      <!-- Manhã -->
      <div class="bg-slate-900/70 p-3.5 rounded-lg border border-slate-800">
        <div class="flex items-center justify-between mb-1.5">
          <span class="font-bold text-blue-400 flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-full bg-blue-500"></span> 🌅 MANHÃ: DSM (ou GTI)
          </span>
          <span class="text-[11px] text-slate-400 bg-slate-800 px-2 py-0.5 rounded font-mono" id="just-man-badge">2,82 a 4,77 C/V</span>
        </div>
        <p class="text-slate-300 leading-relaxed" id="just-man-text">
          <b>Polo Tecnológico Regional:</b> Em cidades do porte de Rio Preto (200k a 600k hab.), a procura por tecnologia matutina é expressiva. DSM (2,82 C/V) e Gestão da TI (4,77 C/V) aproveitam integralmente os laboratórios de ADS instalados para a noite, atendendo o público jovem do Ensino Médio que busca estágios à tarde.
        </p>
      </div>

      <!-- Tarde -->
      <div class="bg-slate-900/70 p-3.5 rounded-lg border border-slate-800">
        <div class="flex items-center justify-between mb-1.5">
          <span class="font-bold text-amber-400 flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span> ☀️ TARDE: Gestão Empresarial
          </span>
          <span class="text-[11px] text-emerald-400 bg-slate-800 px-2 py-0.5 rounded font-mono" id="just-tar-badge">1,78 a 2,12 C/V</span>
        </div>
        <p class="text-slate-300 leading-relaxed" id="just-tar-text">
          <b>Sustentabilidade no Turno Crítico:</b> O turno vespertino em cidades médias é desafiador. Gestão Empresarial mantém procura consistente e segura em Rio Preto (1,78 C/V com pico de 2,35 C/V), diversificando o campus para o eixo de negócios sem risco de salas vazias. (Opção alternativa: DSM Vespertino com 2,82 C/V).
        </p>
      </div>

      <!-- Noite -->
      <div class="bg-slate-900/70 p-3.5 rounded-lg border border-slate-800">
        <div class="flex items-center justify-between mb-1.5">
          <span class="font-bold text-emerald-400 flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> 🌙 NOITE: ADS
          </span>
          <span class="text-[11px] text-amber-400 bg-slate-800 px-2 py-0.5 rounded font-mono" id="just-noi-badge">11,61 C/V</span>
        </div>
        <p class="text-slate-300 leading-relaxed" id="just-noi-text">
          <b>Demanda Explosiva na Faixa de Rio Preto:</b> Na faixa de 200k a 600k habitantes, ADS Noite atinge sua maior força histórica: <b>11,61 C/V</b> (pico de 14,01 C/V). Rio Preto é centro de serviços médicos, comerciais e startups, tornando ADS o curso de maior prestígio e garantia total de preenchimento.
        </p>
      </div>
    </div>
  </div>

  <!-- GRID DE GRÁFICOS VISUAIS POWER BI -->
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">
    <!-- Visual 1: Ranking de Barras Dinâmico -->
    <div class="pbi-card p-4">
      <div class="flex justify-between items-center mb-2">
        <div>
          <h3 class="text-sm font-bold text-white" id="bar-title">Ranking de Demanda por C/V</h3>
          <p class="text-[11px] text-slate-400" id="bar-subtitle">Cursos consolidados da faixa populacional selecionada</p>
        </div>
        <span class="text-xs bg-slate-800 text-cyan-400 px-2 py-0.5 rounded border border-slate-700 font-mono font-bold">Visual: Barras</span>
      </div>
      <div class="h-64 flex flex-col justify-around text-xs" id="bar-chart-container">
        <!-- Renderizado dinamicamente via JS -->
      </div>
    </div>

    <!-- Visual 2: Série Temporal / Gráfico de Linhas Dinâmico -->
    <div class="pbi-card p-4">
      <div class="flex justify-between items-center mb-2">
        <div>
          <h3 class="text-sm font-bold text-white" id="line-chart-title">Série Histórica Dinâmica (2022.1 a 2024.2)</h3>
          <p class="text-[11px] text-slate-400" id="line-chart-subtitle">Atualiza em tempo real com base no porte da cidade e turno</p>
        </div>
        <span class="text-xs bg-slate-800 text-emerald-400 px-2 py-0.5 rounded border border-slate-700 font-mono font-bold">Visual: Linhas</span>
      </div>
      <div class="relative w-full h-64" id="line-chart-wrapper">
        <!-- SVG desenhado e recalculado dinamicamente via JS -->
      </div>
      <div class="flex flex-wrap items-center justify-center gap-2.5 mt-2 text-[10px] text-slate-300" id="line-chart-legend">
        <!-- Legenda atualizada via JS -->
      </div>
    </div>
  </div>

  <!-- TABELA MATRIZ COM BARRAS DE DADOS -->
  <div class="pbi-card p-4 mb-4">
    <div class="flex justify-between items-center mb-2">
      <div>
        <h3 class="text-sm font-bold text-white">Matriz de Indicadores dos Cursos (Faixa Populacional Ativa)</h3>
        <p class="text-[11px] text-slate-400">Dados oficiais validados do arquivo Excel da FATEC</p>
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
            <th class="py-2.5 px-3 w-36">Gráfico C/V</th>
            <th class="py-2.5 px-3">Demanda 2024</th>
            <th class="py-2.5 px-3">Desvio (&sigma;)</th>
            <th class="py-2.5 px-3">Qtd Unidades</th>
            <th class="py-2.5 px-3">Decisão</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800/60" id="matrix-tbody">
          <!-- Linhas renderizadas via JS -->
        </tbody>
      </table>
    </div>
  </div>

  <footer class="pbi-card p-3.5 flex flex-col sm:flex-row justify-between items-center gap-3 text-xs text-slate-400">
    <div class="flex items-center gap-2">
      <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
      <span>Base Oficial FATEC: <b>demanda_vestibular.xlsx</b> (Aba ativa: <b id="footer-sheet" class="text-white">200 a 600</b>)</span>
    </div>
    <div>
      <span>Trabalho 4 - Análise de Demanda FATEC | Rio Preto (~480k hab.) | Apresentação em 09/11</span>
    </div>
  </footer>

  <script>
    // DADOS CARREGADOS DE TODAS AS ABAS POPULACIONAIS DO EXCEL
    const allPopData = __POP_DATA_JSON__;

    let currentPopTier = 'rio_preto_200_600';
    let currentShift = 'todos';
    let currentScenario = 'recomendado';

    const colorsPalette = ['#10b981', '#38bdf8', '#f59e0b', '#a855f7', '#ec4899', '#14b8a6', '#6366f1', '#eab308'];

    function toggleGlossary() {
      const content = document.getElementById('glossary-content');
      const btn = document.getElementById('glossary-toggle-btn');
      if (content.style.display === 'none') {
        content.style.display = 'grid';
        btn.innerText = '[Clique para recolher]';
      } else {
        content.style.display = 'none';
        btn.innerText = '[Clique para expandir]';
      }
    }

    function setPopTier(tierKey, btn) {
      currentPopTier = tierKey;
      document.querySelectorAll('#pop-filters .pop-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const tierInfo = allPopData[tierKey];
      document.getElementById('active-sheet-indicator').innerText = tierInfo.sheet;
      document.getElementById('footer-sheet').innerText = tierInfo.sheet;

      updateKpis();
      updateJustifications();
      renderTable();
      renderBarVisual();
      renderDynamicLineChart();
    }

    function setShift(shift, btn) {
      currentShift = shift;
      document.querySelectorAll('#shift-filters .slicer-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderTable();
      renderBarVisual();
      renderDynamicLineChart();
    }

    function setScenario(scen, btn) {
      currentScenario = scen;
      document.querySelectorAll('#scenario-filters .slicer-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      updateKpis();
      renderTable();
      renderBarVisual();
      renderDynamicLineChart();
    }

    function updateKpis() {
      const tier = allPopData[currentPopTier];
      const courses = tier.courses;

      const kpiManCourse = document.getElementById('kpi-man-course');
      const kpiManDem = document.getElementById('kpi-man-dem');
      const kpiTarCourse = document.getElementById('kpi-tar-course');
      const kpiTarDem = document.getElementById('kpi-tar-dem');
      const kpiNoiCourse = document.getElementById('kpi-noi-course');
      const kpiNoiDem = document.getElementById('kpi-noi-dem');
      const kpiTotDem = document.getElementById('kpi-tot-dem');

      // Buscar valores da aba ativa
      const findCourse = (turno, name) => courses.find(c => c.turno === turno && c.curso.includes(name));

      let adsNoite = findCourse('Noite', 'Análise e Desenvolvimento');
      let dsmManha = findCourse('Manhã', 'Desenvolvimento de Software');
      let gtiManha = findCourse('Manhã', 'Gestão da Tecnologia');
      let gestaoTarde = findCourse('Tarde', 'Gestão Empresarial');
      let agroTarde = findCourse('Tarde', 'Big Data no Agronegócio');
      let mecanoite = findCourse('Noite', 'Mecanização em Agricultura');
      let mecaManha = findCourse('Manhã', 'Mecanização em Agricultura');

      if (currentScenario === 'demanda_pura') {
        let adsManha = findCourse('Manhã', 'Análise e Desenvolvimento');
        let adsTarde = findCourse('Tarde', 'Análise e Desenvolvimento');
        kpiManCourse.innerText = 'ADS (Manhã)';
        kpiManDem.innerText = adsManha ? adsManha.media.toFixed(2) : '5.16';
        kpiTarCourse.innerText = 'ADS (Tarde)';
        kpiTarDem.innerText = adsTarde ? adsTarde.media.toFixed(2) : '4.23';
        kpiNoiCourse.innerText = 'ADS (Noite)';
        kpiNoiDem.innerText = adsNoite ? adsNoite.media.toFixed(2) : '9.90';
        let total = (adsManha ? adsManha.media : 5.16) + (adsTarde ? adsTarde.media : 4.23) + (adsNoite ? adsNoite.media : 9.90);
        kpiTotDem.innerText = total.toFixed(2);
        return;
      }

      // Cenário Recomendado dinâmico por porte populacional
      if (currentPopTier === 'ate_100' || currentPopTier === 'ate_200') {
        kpiManCourse.innerText = mecaManha ? 'Mecanização Agrícola (Manhã)' : (dsmManha ? 'DSM (Manhã)' : 'ADS (Manhã)');
        kpiManDem.innerText = mecaManha ? mecaManha.media.toFixed(2) : (dsmManha ? dsmManha.media.toFixed(2) : '2.51');

        kpiTarCourse.innerText = agroTarde ? 'Big Data no Agro (Tarde)' : 'Gestão Empresarial (Tarde)';
        kpiTarDem.innerText = agroTarde ? agroTarde.media.toFixed(2) : (gestaoTarde ? gestaoTarde.media.toFixed(2) : '1.86');

        kpiNoiCourse.innerText = 'ADS Noite (ou Mecanização)';
        kpiNoiDem.innerText = adsNoite ? adsNoite.media.toFixed(2) : '4.50';

        let mVal = mecaManha ? mecaManha.media : 2.40;
        let tVal = agroTarde ? agroTarde.media : 1.96;
        let nVal = adsNoite ? adsNoite.media : 4.50;
        kpiTotDem.innerText = (mVal + tVal + nVal).toFixed(2);
      } else {
        // Rio Preto e Cidades Médias/Grandes
        kpiManCourse.innerText = dsmManha ? 'DSM (Software Multiplataforma)' : (gtiManha ? 'Gestão da TI' : 'ADS Manhã');
        kpiManDem.innerText = dsmManha ? dsmManha.media.toFixed(2) : (gtiManha ? gtiManha.media.toFixed(2) : '3.21');

        kpiTarCourse.innerText = gestaoTarde ? 'Gestão Empresarial (Tarde)' : 'ADS Tarde';
        kpiTarDem.innerText = gestaoTarde ? gestaoTarde.media.toFixed(2) : '1.83';

        kpiNoiCourse.innerText = 'ADS (Análise e Desenv. Sist.)';
        kpiNoiDem.innerText = adsNoite ? adsNoite.media.toFixed(2) : '9.90';

        let mVal = dsmManha ? dsmManha.media : 3.21;
        let tVal = gestaoTarde ? gestaoTarde.media : 1.83;
        let nVal = adsNoite ? adsNoite.media : 9.90;
        kpiTotDem.innerText = (mVal + tVal + nVal).toFixed(2);
      }
    }

    function updateJustifications() {
      const header = document.getElementById('justification-header');
      const textMan = document.getElementById('just-man-text');
      const textTar = document.getElementById('just-tar-text');
      const textNoi = document.getElementById('just-noi-text');
      const badgeMan = document.getElementById('just-man-badge');
      const badgeTar = document.getElementById('just-tar-badge');
      const badgeNoi = document.getElementById('just-noi-badge');

      if (currentPopTier === 'rio_preto_200_600') {
        header.innerText = 'JUSTIFICATIVAS: SÃO JOSÉ DO RIO PRETO (~480k hab. / FAIXA 200k a 600k)';
        badgeMan.innerText = '2,82 C/V (GTI: 4,77)';
        badgeTar.innerText = '1,78 C/V (2024: 2,12)';
        badgeNoi.innerText = '11,61 C/V (Pico: 14,01)';
        textMan.innerHTML = '<b>Polo de Serviços e Tecnologia:</b> Em cidades do porte de Rio Preto (480k hab.), a vocação em TI e Serviços Médicos é latente. DSM e GTI têm demanda consolidada na manhã e aproveitam 100% dos laboratórios noturnos de ADS.';
        textTar.innerHTML = '<b>Estabilidade no Turno Vespertino:</b> Gestão Empresarial sustenta a tarde de Rio Preto com 1,78 C/V (acelerando para 2,12 em 2024). Atende o forte setor terciário, hospitalar e de franquias da cidade.';
        textNoi.innerHTML = '<b>Demanda Noturna Recorde:</b> Na faixa de Rio Preto, ADS Noite salta de 9,90 para impressionantes <b>11,61 C/V</b> com pico de 14,01 C/V em 2024.1, garantindo o vestibular mais concorrido da região.';
      } else if (currentPopTier === 'ate_100' || currentPopTier === 'ate_200') {
        header.innerText = `JUSTIFICATIVAS: CIDADES PEQUENAS (${currentPopTier === 'ate_100' ? 'ATÉ 100k' : 'ATÉ 200k'} HAB.)`;
        badgeMan.innerText = '2,40 C/V (Agro)';
        badgeTar.innerText = '1,96 C/V (Big Data Agro)';
        badgeNoi.innerText = '4,50 C/V (Meca: 4,38)';
        textMan.innerHTML = '<b>Vocação Agropecuária Matutina:</b> Em municípios menores, <i>Mecanização em Agricultura de Precisão</i> (2,40 C/V) e <i>Agroindústria</i> (1,71 C/V) disputam a liderança matutina diretamente com TI.';
        textTar.innerHTML = '<b>Big Data no Agronegócio Lidera a Tarde:</b> Nesta faixa populacional, Big Data no Agro atinge 1,96 C/V à tarde, superando inclusive ADS (1,87 C/V) e Gestão Empresarial (1,86 C/V).';
        textNoi.innerHTML = '<b>Forte Procura por Tecnologia no Campo:</b> À noite, ADS (4,50 C/V) e Mecanização Agrícola (4,38 C/V) são os dois grandes motores de concorrência nessas unidades.';
      } else {
        header.innerText = 'JUSTIFICATIVAS: CENÁRIO GERAL (TODOS OS MUNICÍPIOS DO ESTADO)';
        badgeMan.innerText = '3,21 C/V';
        badgeTar.innerText = '1,83 C/V';
        badgeNoi.innerText = '9,90 C/V';
        textMan.innerHTML = '<b>Sinergia Máxima de Infraestrutura:</b> Aproveitamento integral dos laboratórios de informática de ADS para a turma de DSM da manhã, gerando custo de implantação de turma quase nulo.';
        textTar.innerHTML = '<b>Proteção do Turno Crítico:</b> Gestão Empresarial apresenta demanda sólida com crescimento recente (2,05 C/V em 2024) e baixíssimo desvio padrão (&sigma; = 0,36).';
        textNoi.innerHTML = '<b>Líder Absoluto de Procura:</b> ADS é o curso mais concorrido e consolidado de toda a história das FATECs, com 9,90 C/V em mais de 22 faculdades simultâneas.';
      }
    }

    // GRÁFICO DE BARRAS DINÂMICO
    function renderBarVisual() {
      const container = document.getElementById('bar-chart-container');
      const titleEl = document.getElementById('bar-title');
      const subtitleEl = document.getElementById('bar-subtitle');
      container.innerHTML = '';

      const tier = allPopData[currentPopTier];
      let courses = tier.courses;

      if (currentShift !== 'todos') {
        titleEl.innerText = `Ranking de Demanda: Turno ${currentShift.toUpperCase()} (${tier.sheet})`;
        subtitleEl.innerText = `Top cursos do período na faixa: ${tier.sheet}`;
        courses = courses.filter(c => c.turno === currentShift);
      } else {
        titleEl.innerText = `Ranking Geral de Demanda C/V (${tier.sheet})`;
        subtitleEl.innerText = `Top cursos por concorrência na faixa: ${tier.sheet}`;
      }

      // Ordenar por média e pegar os top 7 com pelo menos 3 semestres
      const filtered = courses.filter(c => c.semestres >= 3).sort((a,b) => b.media - a.media).slice(0, 7);

      const maxVal = filtered.length > 0 ? Math.max(...filtered.map(f => f.media)) : 10;

      filtered.forEach((item, idx) => {
        const pct = Math.min(100, (item.media / maxVal) * 100);
        const isRec = (item.status === 'RECOMENDADO' || item.curso.includes('Análise e Desenvolvimento'));
        const color = isRec ? (item.turno === 'Noite' ? '#10b981' : item.turno === 'Manhã' ? '#38bdf8' : '#f59e0b') : '#64748b';

        const row = document.createElement('div');
        row.className = 'flex items-center gap-2 py-0.5';
        row.innerHTML = `
          <div class="w-44 text-right truncate text-[11px] ${isRec ? 'font-bold text-white' : 'text-slate-400'}">
            ${isRec ? '⭐ ' : ''}${item.curso} (${item.turno[0]})
          </div>
          <div class="flex-1 bg-slate-800/80 h-5 rounded overflow-hidden relative flex items-center">
            <div class="h-full rounded transition-all duration-500" style="width: ${pct}%; background-color: ${color};"></div>
            <span class="absolute right-2 text-[10px] font-bold text-white">${item.media.toFixed(2)} C/V</span>
          </div>
        `;
        container.appendChild(row);
      });
    }

    // GRÁFICO DE LINHAS 100% DINÂMICO
    function renderDynamicLineChart() {
      const wrapper = document.getElementById('line-chart-wrapper');
      const legendDiv = document.getElementById('line-chart-legend');
      const titleEl = document.getElementById('line-chart-title');
      const subtitleEl = document.getElementById('line-chart-subtitle');

      const tier = allPopData[currentPopTier];
      const seriesDict = tier.series;

      titleEl.innerText = `Série Histórica Semestral (${tier.sheet} - 2022.1 a 2024.2)`;
      subtitleEl.innerText = `Mostrando concorrência semestre a semestre para o filtro: ${currentShift === 'todos' ? 'Destaques' : currentShift}`;

      // Filtrar as chaves a exibir
      let activeKeys = Object.keys(seriesDict);
      if (currentShift !== 'todos') {
        activeKeys = activeKeys.filter(k => seriesDict[k].turno === currentShift);
      }

      // Ordenar pelas maiores médias e limitar a 5 linhas para não poluir
      activeKeys.sort((a,b) => seriesDict[b].media - seriesDict[a].media);
      activeKeys = activeKeys.slice(0, 5);

      if (activeKeys.length === 0) {
        wrapper.innerHTML = '<div class="text-xs text-slate-400 p-4">Sem dados históricos para a combinação selecionada.</div>';
        legendDiv.innerHTML = '';
        return;
      }

      // Encontrar max Y
      let maxVal = 0;
      activeKeys.forEach(k => {
        seriesDict[k].vals.forEach(v => {
          if (v !== null && v !== undefined) maxVal = Math.max(maxVal, v);
        });
      });
      maxVal = Math.max(4, Math.ceil(maxVal * 1.15));

      const width = 500;
      const height = 220;
      const padLeft = 38;
      const padRight = 18;
      const padTop = 18;
      const padBottom = 28;

      const plotW = width - padLeft - padRight;
      const plotH = height - padTop - padBottom;

      const semesters = ['22.1', '22.2', '23.1', '23.2', '24.1', '24.2'];
      const xStep = plotW / (semesters.length - 1);

      let svgHtml = `<svg viewBox="0 0 ${width} ${height}" class="w-full h-full overflow-visible">`;

      // Grade horizontal
      const gridSteps = 4;
      for (let g = 0; g <= gridSteps; g++) {
        const yVal = (maxVal / gridSteps) * g;
        const yPos = padTop + plotH - (yVal / maxVal) * plotH;
        svgHtml += `
          <line x1="${padLeft}" y1="${yPos}" x2="${width - padRight}" y2="${yPos}" stroke="#1e293b" stroke-dasharray="3,3" />
          <text x="${padLeft - 6}" y="${yPos + 3.5}" fill="#64748b" font-size="8.5" text-anchor="end">${yVal.toFixed(1)}</text>
        `;
      }

      // Rótulos X
      semesters.forEach((sem, idx) => {
        const xPos = padLeft + idx * xStep;
        svgHtml += `<text x="${xPos}" y="${height - 8}" fill="#94a3b8" font-size="9.5" font-weight="600" text-anchor="middle">${sem}</text>`;
      });

      // Linhas
      let legendHtml = '';
      activeKeys.forEach((key, colorIdx) => {
        const s = seriesDict[key];
        const lineColor = colorsPalette[colorIdx % colorsPalette.length];

        let points = [];
        let pointsCoords = [];

        s.vals.forEach((v, idx) => {
          if (v !== null && v !== undefined) {
            const xPos = padLeft + idx * xStep;
            const yPos = padTop + plotH - (v / maxVal) * plotH;
            points.push(`${xPos},${yPos}`);
            pointsCoords.push({ x: xPos, y: yPos, val: v, sem: semesters[idx] });
          }
        });

        if (points.length > 1) {
          svgHtml += `<polyline fill="none" stroke="${lineColor}" stroke-width="2.2" points="${points.join(' ')}" opacity="0.9" />`;
        }

        pointsCoords.forEach(pt => {
          svgHtml += `
            <circle cx="${pt.x}" cy="${pt.y}" r="3.5" fill="${lineColor}" stroke="#0b111e" stroke-width="1.5"
                    class="cursor-pointer hover:r-5 transition-all"
                    onmouseover="showLineTooltip(event, '${s.curso} (${s.turno})', '${pt.sem}', ${pt.val})"
                    onmouseout="hideLineTooltip()" />
            <text x="${pt.x}" y="${pt.y - 5}" fill="${lineColor}" font-size="8" font-weight="bold" text-anchor="middle"
                  style="paint-order: stroke; stroke: #0b111e; stroke-width: 2px;">
              ${pt.val.toFixed(1)}
            </text>
          `;
        });

        legendHtml += `
          <span class="flex items-center gap-1.5 cursor-pointer hover:text-white">
            <span class="w-2.5 h-1 rounded" style="background-color: ${lineColor};"></span>
            <span>${s.curso} (${s.turno})</span>
          </span>
        `;
      });

      svgHtml += `</svg>`;
      wrapper.innerHTML = svgHtml;
      legendDiv.innerHTML = legendHtml;
    }

    function showLineTooltip(e, name, sem, val) {
      const tt = document.getElementById('line-tooltip');
      tt.innerHTML = `<b>${name}</b><br>Vestibular: <span class="text-amber-300 font-bold">${sem}</span><br>Demanda: <span class="text-emerald-400 font-bold">${val.toFixed(2)} C/V</span>`;
      tt.style.display = 'block';
      tt.style.left = (e.pageX + 10) + 'px';
      tt.style.top = (e.pageY - 35) + 'px';
    }

    function hideLineTooltip() {
      document.getElementById('line-tooltip').style.display = 'none';
    }

    // TABELA MATRIZ
    function renderTable() {
      const tbody = document.getElementById('matrix-tbody');
      tbody.innerHTML = '';

      const tier = allPopData[currentPopTier];
      let courses = tier.courses;

      if (currentShift !== 'todos') {
        courses = courses.filter(d => d.turno === currentShift);
      }

      // Ordenar por Demanda
      courses.sort((a,b) => b.media - a.media);

      courses.slice(0, 15).forEach(d => {
        const isRec = (d.status === 'RECOMENDADO' || (d.curso.includes('Análise e Desenvolvimento') && d.turno === 'Noite'));
        const pctBar = Math.min(100, (d.media / 12.0) * 100);
        const tr = document.createElement('tr');
        tr.className = `hover:bg-slate-800/40 transition-colors ${isRec ? 'bg-slate-800/30 font-medium' : ''}`;
        
        let badgeClass = 'bg-slate-800 text-slate-400 border border-slate-700';
        if (isRec) badgeClass = 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-bold';
        else if (d.status.includes('Líder')) badgeClass = 'bg-blue-500/20 text-blue-300 border border-blue-500/40';

        const color = d.turno === 'Noite' ? '#10b981' : d.turno === 'Manhã' ? '#38bdf8' : '#f59e0b';

        tr.innerHTML = `
          <td class="py-2.5 px-3">
            <span class="inline-flex items-center gap-1.5 font-bold ${d.turno === 'Manhã' ? 'text-blue-400' : d.turno === 'Tarde' ? 'text-amber-400' : 'text-emerald-400'}">
              ${d.turno === 'Manhã' ? '🌅' : d.turno === 'Tarde' ? '☀️' : '🌙'} ${d.turno}
            </span>
          </td>
          <td class="py-2.5 px-3 text-white font-semibold flex items-center gap-1.5">
            ${isRec ? '<span title="Curso Escolhido Oficial">⭐</span>' : ''} ${d.curso}
          </td>
          <td class="py-2.5 px-3 text-slate-400 text-[11px]">${d.eixo}</td>
          <td class="py-2.5 px-3 font-bold text-white">${d.media.toFixed(2)} C/V</td>
          <td class="py-2.5 px-3">
            <div class="data-bar-container">
              <div class="data-bar" style="width: ${pctBar}%; background-color: ${color};"></div>
            </div>
          </td>
          <td class="py-2.5 px-3 text-slate-300">${d.rec24.toFixed(2)} C/V</td>
          <td class="py-2.5 px-3 text-slate-400">&plusmn;${d.dp.toFixed(2)}</td>
          <td class="py-2.5 px-3 text-slate-300 font-semibold">${d.qtd.toFixed(1)} un.</td>
          <td class="py-2.5 px-3">
            <span class="badge ${badgeClass}">${isRec ? 'RECOMENDADO' : d.status}</span>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    // Inicialização
    updateKpis();
    updateJustifications();
    renderTable();
    renderBarVisual();
    renderDynamicLineChart();
  </script>
</body>
</html>
"""

final_html = html_template.replace('__POP_DATA_JSON__', json_str)

out_proj = r'C:\Users\PICHAU\.gemini\antigravity\scratch\trabalho_vestibular\painel_powerbi.html'
out_art = r'C:\Users\PICHAU\.gemini\antigravity\brain\fede3023-63c1-42db-824f-ab771fa6007a\painel_powerbi.html'

with open(out_proj, 'w', encoding='utf-8') as f:
    f.write(final_html)

with open(out_art, 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Painel Power BI V3 gerado com sucesso!")
