import json
import os

with open(r'C:\Users\PICHAU\.gemini\antigravity\scratch\trabalho_vestibular\pop_tiers_data_v4.json', 'r', encoding='utf-8') as f:
    pop_data = json.load(f)

json_str = json.dumps(pop_data, ensure_ascii=False)

html_code = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Power BI - FATEC Demanda Vestibular | Painel de Alocação de Cursos (Rio Preto & População)</title>
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
      box-shadow: 0 4px 14px rgba(0,0,0,0.35);
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
    .rank-item {
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .rank-item:hover {
      background-color: #1e293b;
      transform: translateX(4px);
    }
    .rank-item.selected {
      border-left: 3px solid #38bdf8;
      background-color: #1e293b;
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
          <span class="text-xs bg-cyan-500/20 text-cyan-300 font-bold px-2 py-0.5 rounded border border-cyan-500/30" id="header-badge-pop">CIDADE: SÃO JOSÉ DO RIO PRETO (~480k hab.)</span>
          <span class="text-xs text-slate-400">Trabalho 4 - FATEC</span>
        </div>
        <h1 class="text-xl md:text-2xl font-bold text-white tracking-tight">Painel de Decisão de Cursos: Ranking & Alocação por Período</h1>
        <p class="text-xs text-slate-400">Dados Oficiais dos Vestibulares FATEC (2022.1 a 2024.2) • Estratificação Populacional de Rio Preto</p>
      </div>
    </div>
    <div class="flex flex-wrap items-center gap-2">
      <div class="bg-slate-800/80 border border-slate-700 px-3 py-1.5 rounded-lg text-right">
        <div class="text-[10px] text-slate-400 uppercase font-semibold">População Selecionada</div>
        <div class="text-sm font-bold text-cyan-400" id="header-pop-name">Rio Preto (200k-600k)</div>
      </div>
      <div class="bg-slate-800/80 border border-slate-700 px-3 py-1.5 rounded-lg text-right">
        <div class="text-[10px] text-slate-400 uppercase font-semibold">Regra do Trabalho</div>
        <div class="text-sm font-bold text-amber-400">1 Curso por Turno</div>
      </div>
    </div>
  </header>

  <!-- SEGMENTADORES (SLICERS) POWER BI -->
  <div class="pbi-card p-3 mb-4 space-y-3">
    <!-- Linha 1: Filtro de População -->
    <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-2.5">
      <div class="flex flex-wrap items-center gap-2">
        <span class="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1">
          🏢 Filtro de Porte Populacional:
        </span>
        <div class="flex flex-wrap gap-1" id="pop-filters">
          <button class="slicer-btn pop-btn active" onclick="setPopTier('rio_preto', this)">
            📍 São José do Rio Preto (~480k hab. / Aba 200 a 600)
          </button>
          <button class="slicer-btn pop-btn" onclick="setPopTier('ate_500', this)">Até 500 mil hab. (Aba Até 500)</button>
          <button class="slicer-btn pop-btn" onclick="setPopTier('faixa_100_600', this)">100 a 600 mil hab.</button>
          <button class="slicer-btn pop-btn" onclick="setPopTier('pequenas_ate_200', this)">
            🌾 Cidades Pequenas / Agro (Até 100k e 200k hab.*)
          </button>
          <button class="slicer-btn pop-btn" onclick="setPopTier('todos', this)">🌐 Todos (Estado Geral)</button>
        </div>
      </div>
      <div class="text-[11px] text-slate-400 bg-slate-800 px-2.5 py-1 rounded border border-slate-700">
        Aba ativa no Excel: <b class="text-white" id="active-sheet-indicator">200 a 600</b>
      </div>
    </div>

    <!-- Linha 2: Filtro de Turno -->
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div class="flex items-center gap-2">
        <span class="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
          🌅 Turno de Análise:
        </span>
        <div class="flex gap-1" id="shift-filters">
          <button class="slicer-btn active" onclick="setShift('todos', this)">Todos os Turnos (Visão do Campus)</button>
          <button class="slicer-btn" onclick="setShift('Manhã', this)">🌅 Manhã</button>
          <button class="slicer-btn" onclick="setShift('Tarde', this)">☀️ Tarde</button>
          <button class="slicer-btn" onclick="setShift('Noite', this)">🌙 Noite</button>
        </div>
      </div>

      <!-- Nota Técnica sobre Até 100 e Até 200 -->
      <div class="text-[11px] text-slate-400 italic flex items-center gap-1.5" id="note-pop-explanation">
        <span>💡 <i>Dica: Clique em qualquer curso no ranking para destacar sua série histórica!</i></span>
      </div>
    </div>
  </div>

  <!-- AVISO TÉCNICO EXPLICATIVO QUANDO ESCOLHE CIDADES PEQUENAS -->
  <div id="alert-small-cities" class="hidden pbi-card p-3 mb-4 bg-amber-950/40 border-amber-600/50 text-amber-200 text-xs flex items-center gap-2">
    <span>⚠️</span>
    <span><b>Nota Técnica sobre o Excel original:</b> As abas <i>"Até 100"</i> e <i>"Até 200"</i> da planilha fornecida possuem exatamente as mesmas 232 linhas de dados (apenas reordenadas), pois todos os campi abaixo de 200k habitantes situam-se em municípios de até 100k habitantes. Por isso foram agrupadas aqui para evitar confusão!</span>
  </div>

  <!-- CARDS DE KPI DINÂMICOS -->
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
    <div class="pbi-card p-4 border-l-4 border-l-blue-500 relative overflow-hidden">
      <div class="flex justify-between items-start mb-1">
        <span class="kpi-title text-blue-400">🌅 Manhã (1º Escolha)</span>
        <span class="badge bg-blue-500/20 text-blue-300 border border-blue-500/30" id="kpi-man-badge">Recomendado</span>
      </div>
      <div class="text-lg font-bold text-white truncate" id="kpi-man-course">DSM (Software Multiplataforma)</div>
      <div class="flex items-baseline gap-2 mt-2">
        <span class="kpi-value text-blue-400" id="kpi-man-dem">2.82</span>
        <span class="text-xs text-slate-400">C/V (Candidatos/Vaga)</span>
      </div>
      <div class="mt-2 text-xs text-slate-300 flex justify-between border-t border-slate-800 pt-2" id="kpi-man-sub">
        <span>2º Opção: <b class="text-white" id="kpi-man-opt2">GTI (4.77 C/V)</b></span>
        <span class="text-emerald-400 font-semibold">100% Sinergia</span>
      </div>
    </div>

    <div class="pbi-card p-4 border-l-4 border-l-amber-500 relative overflow-hidden">
      <div class="flex justify-between items-start mb-1">
        <span class="kpi-title text-amber-400">☀️ Tarde (1º Escolha)</span>
        <span class="badge bg-amber-500/20 text-amber-300 border border-amber-500/30" id="kpi-tar-badge">Recomendado</span>
      </div>
      <div class="text-lg font-bold text-white truncate" id="kpi-tar-course">Gestão Empresarial</div>
      <div class="flex items-baseline gap-2 mt-2">
        <span class="kpi-value text-amber-400" id="kpi-tar-dem">1.78</span>
        <span class="text-xs text-slate-400">C/V (Candidatos/Vaga)</span>
      </div>
      <div class="mt-2 text-xs text-slate-300 flex justify-between border-t border-slate-800 pt-2" id="kpi-tar-sub">
        <span>2º Opção: <b class="text-white" id="kpi-tar-opt2">DSM (2.82 C/V)</b></span>
        <span class="text-blue-300 font-semibold">Turno Protegido</span>
      </div>
    </div>

    <div class="pbi-card p-4 border-l-4 border-l-emerald-500 relative overflow-hidden">
      <div class="flex justify-between items-start mb-1">
        <span class="kpi-title text-emerald-400">🌙 Noite (1º Escolha)</span>
        <span class="badge bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Líder Absoluto</span>
      </div>
      <div class="text-lg font-bold text-white truncate" id="kpi-noi-course">ADS (Análise e Desenv. Sist.)</div>
      <div class="flex items-baseline gap-2 mt-2">
        <span class="kpi-value text-emerald-400" id="kpi-noi-dem">11.61</span>
        <span class="text-xs text-slate-400">C/V (Candidatos/Vaga)</span>
      </div>
      <div class="mt-2 text-xs text-slate-300 flex justify-between border-t border-slate-800 pt-2" id="kpi-noi-sub">
        <span>2º Opção: <b class="text-white" id="kpi-noi-opt2">GTI (6.01 C/V)</b></span>
        <span class="text-amber-400 font-bold">Recorde de Demanda</span>
      </div>
    </div>

    <div class="pbi-card p-4 border-l-4 border-l-purple-500 relative overflow-hidden">
      <div class="flex justify-between items-start mb-1">
        <span class="kpi-title text-purple-400">📊 Portfólio do Campus</span>
        <span class="badge bg-purple-500/20 text-purple-300 border border-purple-500/30">3 Cursos</span>
      </div>
      <div class="text-lg font-bold text-white truncate" id="kpi-tot-course">Capacidade Plena</div>
      <div class="flex items-baseline gap-2 mt-2">
        <span class="kpi-value text-purple-400" id="kpi-tot-dem">16.21</span>
        <span class="text-xs text-slate-400">C/V Acumulados</span>
      </div>
      <div class="mt-2 text-xs text-slate-300 flex justify-between border-t border-slate-800 pt-2">
        <span>Ociosidade de Vagas: <b class="text-emerald-400">0%</b></span>
        <span>Retenção: <b class="text-emerald-400">Máxima</b></span>
      </div>
    </div>
  </div>

  <!-- DICIONÁRIO DE TERMOS & GLOSSÁRIO (O QUE É C/V?) -->
  <div class="pbi-card p-3.5 mb-4 border-l-4 border-l-cyan-500 bg-slate-900/90">
    <div class="flex items-center justify-between mb-1 cursor-pointer" onclick="toggleGlossary()">
      <div class="flex items-center gap-2">
        <span class="text-base text-cyan-400">📚</span>
        <h3 class="text-xs font-bold text-white uppercase tracking-wider">
          Dicionário de Indicadores: O que significam C/V, Qtd e População de Rio Preto?
        </h3>
      </div>
      <span class="text-[11px] text-cyan-400 font-semibold" id="glossary-toggle-btn">[Clique para recolher/expandir]</span>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs pt-2 border-t border-slate-800" id="glossary-content">
      <div class="bg-slate-800/60 p-2.5 rounded border border-slate-700/60">
        <div class="font-bold text-cyan-300 text-xs mb-1">🎯 C/V (Candidatos por Vaga)</div>
        <p class="text-slate-300 leading-relaxed text-[11px]">
          Relação de concorrência: <b>Inscritos ÷ Vagas</b>.
          <br><b>Exemplo em Rio Preto:</b> Em ADS Noite, a demanda é de <b>11,61 C/V</b>. Significa que para 40 vagas, inscrevem-se <b>464 candidatos</b> (quase 12 concorrentes por cadeira!).
        </p>
      </div>

      <div class="bg-slate-800/60 p-2.5 rounded border border-slate-700/60">
        <div class="font-bold text-emerald-300 text-xs mb-1">📍 São José do Rio Preto (População)</div>
        <p class="text-slate-300 leading-relaxed text-[11px]">
          Com <b>~480 mil habitantes</b> (IBGE), Rio Preto é classificada no Excel nas abas <b>"200 a 600"</b> e <b>"Até 500"</b>. É um polo regional de comércio, saúde e serviços com fortíssima demanda por TI e Gestão.
        </p>
      </div>

      <div class="bg-slate-800/60 p-2.5 rounded border border-slate-700/60">
        <div class="font-bold text-amber-300 text-xs mb-1">🏫 Cidades Pequenas (&lt;200k hab.)</div>
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

  <!-- SEÇÃO PRINCIPAL DE GRÁFICOS: RANKING CLARO (PODIUM) + SÉRIE TEMPORAL DINÂMICA -->
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">
    
    <!-- VISUAL 1: RANKING CLARO DE ABERTURA DE CURSOS (1º, 2º, 3º LUGAR) -->
    <div class="pbi-card p-4 flex flex-col justify-between">
      <div class="flex justify-between items-start mb-2 border-b border-slate-800 pb-2">
        <div>
          <h3 class="text-sm font-bold text-white flex items-center gap-1.5" id="ranking-title">
            🏆 Ranking de Abertura: Quais cursos abrir?
          </h3>
          <p class="text-[11px] text-slate-400" id="ranking-subtitle">
            Ordem prioritária de abertura baseada na demanda C/V e sustentabilidade
          </p>
        </div>
        <span class="text-xs bg-slate-800 text-cyan-400 px-2 py-0.5 rounded border border-slate-700 font-mono font-bold">Visual: Pódio/Ranking</span>
      </div>

      <!-- Container do Ranking com Pódio Interativo -->
      <div class="space-y-2 py-1" id="ranking-list-container">
        <!-- Renderizado dinamicamente via JS -->
      </div>

      <div class="text-[11px] text-slate-400 bg-slate-900/60 p-2 rounded border border-slate-800/80 mt-2 flex items-center justify-between">
        <span id="ranking-footer-hint">👉 <b>Clique em qualquer curso acima</b> para destacar sua curva histórica ao lado!</span>
        <button class="text-cyan-400 font-semibold hover:underline" onclick="clearSelection()">Limpar Seleção</button>
      </div>
    </div>

    <!-- VISUAL 2: GRÁFICO DE LINHAS 100% DINÂMICO E REATIVO -->
    <div class="pbi-card p-4 flex flex-col justify-between">
      <div class="flex justify-between items-start mb-2 border-b border-slate-800 pb-2">
        <div>
          <h3 class="text-sm font-bold text-white" id="line-chart-title">
            📈 Série Histórica Semestral (2022.1 a 2024.2)
          </h3>
          <p class="text-[11px] text-slate-400" id="line-chart-subtitle">
            Curvas de concorrência C/V semestre a semestre da população e turno ativos
          </p>
        </div>
        <span class="text-xs bg-slate-800 text-emerald-400 px-2 py-0.5 rounded border border-slate-700 font-mono font-bold">Visual: Linhas Reativas</span>
      </div>

      <!-- SVG do Gráfico de Linhas -->
      <div class="relative w-full h-64" id="line-chart-wrapper">
        <!-- SVG desenhado e recalculado dinamicamente via JS -->
      </div>

      <!-- Legenda Interativa do Gráfico de Linhas -->
      <div class="flex flex-wrap items-center justify-center gap-2.5 mt-2 text-[10px] text-slate-300" id="line-chart-legend">
        <!-- Legenda atualizada via JS -->
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
          <span class="text-[11px] text-emerald-400 bg-slate-800 px-2 py-0.5 rounded font-mono" id="just-tar-badge">1,78 C/V</span>
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

  <!-- TABELA MATRIZ COM BARRAS DE DADOS -->
  <div class="pbi-card p-4 mb-4">
    <div class="flex justify-between items-center mb-2">
      <div>
        <h3 class="text-sm font-bold text-white">Matriz de Indicadores dos Cursos (Faixa Populacional Ativa)</h3>
        <p class="text-[11px] text-slate-400">Dados oficiais validados do arquivo Excel da FATEC</p>
      </div>
      <span class="text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded border border-slate-700 font-mono">Visual: Tabela Matriz</span>
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
            <th class="py-2.5 px-3">Prioridade de Abertura</th>
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
    const allPopData = __POP_DATA_JSON__;

    let currentPopTier = 'rio_preto';
    let currentShift = 'todos';
    let selectedCourseKey = null; // Para interação cruzada!

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
      selectedCourseKey = null; // Reset seleção de curso
      document.querySelectorAll('#pop-filters .pop-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const tierInfo = allPopData[tierKey];
      document.getElementById('active-sheet-indicator').innerText = tierInfo.sheet;
      document.getElementById('footer-sheet').innerText = tierInfo.sheet;

      // Alerta para cidades pequenas
      const alertSmall = document.getElementById('alert-small-cities');
      if (tierKey === 'pequenas_ate_200') {
        alertSmall.classList.remove('hidden');
        document.getElementById('header-pop-name').innerText = 'Até 100k e 200k hab.';
        document.getElementById('header-badge-pop').innerText = 'CIDADES PEQUENAS / AGRO';
      } else {
        alertSmall.classList.add('hidden');
        if (tierKey === 'rio_preto') {
          document.getElementById('header-pop-name').innerText = 'Rio Preto (200k-600k)';
          document.getElementById('header-badge-pop').innerText = 'SÃO JOSÉ DO RIO PRETO (~480k hab.)';
        } else if (tierKey === 'ate_500') {
          document.getElementById('header-pop-name').innerText = 'Até 500k hab.';
          document.getElementById('header-badge-pop').innerText = 'MUNICÍPIOS ATÉ 500k';
        } else if (tierKey === 'faixa_100_600') {
          document.getElementById('header-pop-name').innerText = '100k a 600k hab.';
          document.getElementById('header-badge-pop').innerText = 'CIDADES MÉDIAS (100k-600k)';
        } else {
          document.getElementById('header-pop-name').innerText = 'Estado Geral (Todos)';
          document.getElementById('header-badge-pop').innerText = 'TODOS OS MUNICÍPIOS';
        }
      }

      updateKpis();
      updateJustifications();
      renderRankingPodium();
      renderDynamicLineChart();
      renderTable();
    }

    function setShift(shift, btn) {
      currentShift = shift;
      selectedCourseKey = null;
      document.querySelectorAll('#shift-filters .slicer-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      renderRankingPodium();
      renderDynamicLineChart();
      renderTable();
    }

    function selectCourse(key) {
      selectedCourseKey = key;
      renderRankingPodium();
      renderDynamicLineChart();
      renderTable();
    }

    function clearSelection() {
      selectedCourseKey = null;
      renderRankingPodium();
      renderDynamicLineChart();
      renderTable();
    }

    // ATUALIZAÇÃO DOS KPIS
    function updateKpis() {
      const tier = allPopData[currentPopTier];
      const courses = tier.courses;

      const kpiManCourse = document.getElementById('kpi-man-course');
      const kpiManDem = document.getElementById('kpi-man-dem');
      const kpiManOpt2 = document.getElementById('kpi-man-opt2');

      const kpiTarCourse = document.getElementById('kpi-tar-course');
      const kpiTarDem = document.getElementById('kpi-tar-dem');
      const kpiTarOpt2 = document.getElementById('kpi-tar-opt2');

      const kpiNoiCourse = document.getElementById('kpi-noi-course');
      const kpiNoiDem = document.getElementById('kpi-noi-dem');
      const kpiNoiOpt2 = document.getElementById('kpi-noi-opt2');

      const kpiTotDem = document.getElementById('kpi-tot-dem');

      const findCourse = (turno, name) => courses.find(c => c.turno === turno && c.curso.includes(name));

      let adsNoite = findCourse('Noite', 'Análise e Desenvolvimento');
      let gtiNoite = findCourse('Noite', 'Gestão da Tecnologia');
      let dsmNoite = findCourse('Noite', 'Desenvolvimento de Software');

      let adsManha = findCourse('Manhã', 'Análise e Desenvolvimento');
      let dsmManha = findCourse('Manhã', 'Desenvolvimento de Software');
      let gtiManha = findCourse('Manhã', 'Gestão da Tecnologia');
      let mecaManha = findCourse('Manhã', 'Mecanização em Agricultura');

      let adsTarde = findCourse('Tarde', 'Análise e Desenvolvimento');
      let gestaoTarde = findCourse('Tarde', 'Gestão Empresarial');
      let dsmTarde = findCourse('Tarde', 'Desenvolvimento de Software');
      let agroTarde = findCourse('Tarde', 'Big Data no Agronegócio');

      if (currentPopTier === 'pequenas_ate_200') {
        kpiManCourse.innerText = mecaManha ? 'Mecanização Agrícola (Manhã)' : 'ADS (Manhã)';
        kpiManDem.innerText = mecaManha ? mecaManha.media.toFixed(2) : '2.40';
        kpiManOpt2.innerText = dsmManha ? `DSM (${dsmManha.media.toFixed(2)} C/V)` : 'DSM (2.19 C/V)';

        kpiTarCourse.innerText = agroTarde ? 'Big Data no Agro (Tarde)' : 'Gestão Empresarial';
        kpiTarDem.innerText = agroTarde ? agroTarde.media.toFixed(2) : '1.96';
        kpiTarOpt2.innerText = gestaoTarde ? `Gestão (${gestaoTarde.media.toFixed(2)} C/V)` : 'Gestão (1.86 C/V)';

        kpiNoiCourse.innerText = 'ADS (Noite)';
        kpiNoiDem.innerText = adsNoite ? adsNoite.media.toFixed(2) : '4.50';
        kpiNoiOpt2.innerText = 'Mecanização (4.38 C/V)';

        let m = mecaManha ? mecaManha.media : 2.40;
        let t = agroTarde ? agroTarde.media : 1.96;
        let n = adsNoite ? adsNoite.media : 4.50;
        kpiTotDem.innerText = (m + t + n).toFixed(2);
      } else {
        // Rio Preto e cidades médias
        kpiManCourse.innerText = dsmManha ? 'DSM (Software Multiplataforma)' : 'ADS (Manhã)';
        kpiManDem.innerText = dsmManha ? dsmManha.media.toFixed(2) : '2.82';
        kpiManOpt2.innerText = gtiManha ? `GTI (${gtiManha.media.toFixed(2)} C/V)` : 'GTI (4.77 C/V)';

        kpiTarCourse.innerText = gestaoTarde ? 'Gestão Empresarial (Tarde)' : 'DSM (Tarde)';
        kpiTarDem.innerText = gestaoTarde ? gestaoTarde.media.toFixed(2) : '1.78';
        kpiTarOpt2.innerText = dsmTarde ? `DSM (${dsmTarde.media.toFixed(2)} C/V)` : 'DSM (2.82 C/V)';

        kpiNoiCourse.innerText = 'ADS (Análise e Desenv. Sist.)';
        kpiNoiDem.innerText = adsNoite ? adsNoite.media.toFixed(2) : '11.61';
        kpiNoiOpt2.innerText = gtiNoite ? `GTI (${gtiNoite.media.toFixed(2)} C/V)` : (dsmNoite ? `DSM (${dsmNoite.media.toFixed(2)} C/V)` : 'GTI (6.01 C/V)');

        let m = dsmManha ? dsmManha.media : 2.82;
        let t = gestaoTarde ? gestaoTarde.media : 1.78;
        let n = adsNoite ? adsNoite.media : 11.61;
        kpiTotDem.innerText = (m + t + n).toFixed(2);
      }
    }

    // ATUALIZAÇÃO DOS TEXTOS DE JUSTIFICATIVA
    function updateJustifications() {
      const header = document.getElementById('justification-header');
      const textMan = document.getElementById('just-man-text');
      const textTar = document.getElementById('just-tar-text');
      const textNoi = document.getElementById('just-noi-text');
      const badgeMan = document.getElementById('just-man-badge');
      const badgeTar = document.getElementById('just-tar-badge');
      const badgeNoi = document.getElementById('just-noi-badge');

      if (currentPopTier === 'rio_preto') {
        header.innerText = 'JUSTIFICATIVAS: SÃO JOSÉ DO RIO PRETO (~480k hab. / FAIXA 200k a 600k)';
        badgeMan.innerText = '2,82 C/V (GTI: 4,77)';
        badgeTar.innerText = '1,78 C/V (Pico: 2,35)';
        badgeNoi.innerText = '11,61 C/V (Pico: 14,01)';
        textMan.innerHTML = '<b>Polo de Serviços e Tecnologia:</b> Em cidades do porte de Rio Preto (480k hab.), a procura por tecnologia matutina é expressiva. DSM (2,82 C/V) e Gestão da TI (4,77 C/V) aproveitam integralmente os laboratórios de ADS instalados para a noite, atendendo o público jovem do Ensino Médio que busca estágios à tarde.';
        textTar.innerHTML = '<b>Estabilidade no Turno Vespertino:</b> Gestão Empresarial sustenta a tarde de Rio Preto com 1,78 C/V (com picos de 2,35 C/V). Atende o forte setor terciário, hospitalar e de franquias da cidade sem risco de salas vazias. (Opção alternativa em TI: DSM Vespertino com 2,82 C/V).';
        textNoi.innerHTML = '<b>Demanda Noturna Recorde:</b> Na faixa de Rio Preto, ADS Noite salta de 9,90 para impressionantes <b>11,61 C/V</b> com pico de 14,01 C/V em 2024.1. Rio Preto é centro de serviços médicos, comerciais e startups, tornando ADS o curso de maior prestígio e garantia total de preenchimento.';
      } else if (currentPopTier === 'pequenas_ate_200') {
        header.innerText = 'JUSTIFICATIVAS: CIDADES PEQUENAS (ATÉ 100k E 200k HABITANTES)';
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

    // RENDERIZAR O RANKING DE ABERTURA CLARO (PÓDIO 1º, 2º, 3º LUGAR)
    function renderRankingPodium() {
      const container = document.getElementById('ranking-list-container');
      const titleEl = document.getElementById('ranking-title');
      const subtitleEl = document.getElementById('ranking-subtitle');
      container.innerHTML = '';

      const tier = allPopData[currentPopTier];
      let courses = [...tier.courses];

      // Título e filtro
      if (currentShift === 'todos') {
        titleEl.innerHTML = `🏆 Pódio de Abertura do Campus: 1 Curso por Período (${tier.sheet})`;
        subtitleEl.innerHTML = `Recomendação oficial e alternativas para compor os 3 turnos da faculdade`;

        // Montar os líderes de cada turno
        const getTopForShift = (turno) => {
          let cList = courses.filter(c => c.turno === turno && c.semestres >= 3).sort((a,b) => b.media - a.media);
          return cList;
        };

        const topNoite = getTopForShift('Noite');
        const topManha = getTopForShift('Manhã');
        const topTarde = getTopForShift('Tarde');

        // Itens estruturados do pódio
        const podiumItems = [
          { rankLabel: '🥇 1º ESCOLHA (NOITE)', item: topNoite[0], role: 'Abertura Noturna (Flagship)', badgeBg: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40' },
          { rankLabel: '🥇 1º ESCOLHA (MANHÃ)', item: (topManha[1] && currentPopTier !== 'pequenas_ate_200') ? topManha[1] : topManha[0], role: 'Abertura Matutina (Sinergia)', badgeBg: 'bg-blue-500/20 text-blue-300 border-blue-500/40' },
          { rankLabel: '🥇 1º ESCOLHA (TARDE)', item: (currentPopTier === 'pequenas_ate_200' ? (courses.find(c => c.turno === 'Tarde' && c.curso.includes('Agronegócio')) || topTarde[0]) : (courses.find(c => c.turno === 'Tarde' && c.curso.includes('Gestão')) || topTarde[1])), role: 'Abertura Vespertina (Proteção)', badgeBg: 'bg-amber-500/20 text-amber-300 border-amber-500/40' },
          { rankLabel: '🥈 2º Opção Noite', item: topNoite[1], role: 'Alternativa Noturna', badgeBg: 'bg-slate-800 text-slate-300 border-slate-700' },
          { rankLabel: '🥈 2º Opção Manhã', item: (topManha[2] || topManha[1]), role: 'Alternativa Matutina', badgeBg: 'bg-slate-800 text-slate-300 border-slate-700' },
          { rankLabel: '🥈 2º Opção Tarde', item: (topTarde[1] || topTarde[0]), role: 'Alternativa Vespertina', badgeBg: 'bg-slate-800 text-slate-300 border-slate-700' },
        ];

        podiumItems.forEach(p => {
          if (!p.item) return;
          const isSelected = (selectedCourseKey === p.item.key);
          const el = document.createElement('div');
          el.className = `rank-item p-2.5 rounded-lg border border-slate-800 flex items-center justify-between gap-3 ${isSelected ? 'selected' : ''}`;
          el.onclick = () => selectCourse(p.item.key);

          const pct = Math.min(100, (p.item.media / 12.0) * 100);
          const color = p.item.turno === 'Noite' ? '#10b981' : p.item.turno === 'Manhã' ? '#38bdf8' : '#f59e0b';

          el.innerHTML = `
            <div class="flex items-center gap-2.5 flex-1 min-w-0">
              <span class="text-xs font-bold px-2 py-0.5 rounded border ${p.badgeBg} whitespace-nowrap">
                ${p.rankLabel}
              </span>
              <div class="truncate">
                <div class="text-xs font-bold text-white truncate flex items-center gap-1.5">
                  ${p.item.curso} <span class="text-[10px] text-slate-400 font-normal">(${p.item.turno})</span>
                </div>
                <div class="text-[10px] text-slate-400">${p.role}</div>
              </div>
            </div>
            <div class="w-32 flex flex-col items-end gap-1">
              <span class="text-xs font-bold text-white font-mono">${p.item.media.toFixed(2)} C/V</span>
              <div class="data-bar-container">
                <div class="data-bar" style="width: ${pct}%; background-color: ${color};"></div>
              </div>
            </div>
          `;
          container.appendChild(el);
        });

      } else {
        // Turno Específico (Manhã, Tarde ou Noite)
        titleEl.innerHTML = `🏆 Ranking Específico: Qual curso abrir no turno da ${currentShift.toUpperCase()}?`;
        subtitleEl.innerHTML = `Ordem de classificação para o turno selecionado na faixa: ${tier.sheet}`;

        courses = courses.filter(c => c.turno === currentShift && c.semestres >= 3);
        courses.sort((a,b) => b.media - a.media);

        const rankLabels = ['🥇 1º LUGAR (Abertura Recomendada)', '🥈 2º LUGAR (Forte Alternativa)', '🥉 3º LUGAR (Opção de Reserva)', '4º Lugar', '5º Lugar', '6º Lugar'];
        const badgeColors = [
          'bg-amber-500/20 text-amber-300 border-amber-500/50 font-bold',
          'bg-slate-300/20 text-slate-200 border-slate-400/40 font-bold',
          'bg-amber-700/20 text-amber-400 border-amber-700/40 font-semibold',
          'bg-slate-800 text-slate-400 border-slate-700',
          'bg-slate-800 text-slate-400 border-slate-700',
          'bg-slate-800 text-slate-400 border-slate-700'
        ];

        courses.slice(0, 6).forEach((item, idx) => {
          const isSelected = (selectedCourseKey === item.key);
          const el = document.createElement('div');
          el.className = `rank-item p-2.5 rounded-lg border border-slate-800 flex items-center justify-between gap-3 ${isSelected ? 'selected' : ''}`;
          el.onclick = () => selectCourse(item.key);

          const pct = Math.min(100, (item.media / (courses[0].media * 1.1)) * 100);
          const color = currentShift === 'Noite' ? '#10b981' : currentShift === 'Manhã' ? '#38bdf8' : '#f59e0b';

          el.innerHTML = `
            <div class="flex items-center gap-2.5 flex-1 min-w-0">
              <span class="text-[11px] px-2 py-0.5 rounded border ${badgeColors[idx] || badgeColors[3]} whitespace-nowrap">
                ${rankLabels[idx] || (idx+1 + 'º Lugar')}
              </span>
              <div class="truncate">
                <div class="text-xs font-bold text-white truncate">
                  ${item.curso}
                </div>
                <div class="text-[10px] text-slate-400">${item.eixo} • ${item.qtd.toFixed(1)} un. FATEC</div>
              </div>
            </div>
            <div class="w-28 flex flex-col items-end gap-1">
              <span class="text-xs font-bold text-white font-mono">${item.media.toFixed(2)} C/V</span>
              <div class="data-bar-container">
                <div class="data-bar" style="width: ${pct}%; background-color: ${color};"></div>
              </div>
            </div>
          `;
          container.appendChild(el);
        });
      }
    }

    // RENDERIZAR O GRÁFICO DE LINHAS DINÂMICO
    function renderDynamicLineChart() {
      const wrapper = document.getElementById('line-chart-wrapper');
      const legendDiv = document.getElementById('line-chart-legend');
      const titleEl = document.getElementById('line-chart-title');
      const subtitleEl = document.getElementById('line-chart-subtitle');

      const tier = allPopData[currentPopTier];
      const seriesDict = tier.series;

      let activeKeys = [];

      if (selectedCourseKey && seriesDict[selectedCourseKey]) {
        // Modo Curso Selecionado
        const sel = seriesDict[selectedCourseKey];
        titleEl.innerHTML = `📈 Foco no Curso: <span class="text-cyan-400 font-bold">${sel.curso} (${sel.turno})</span>`;
        subtitleEl.innerHTML = `Comparando a trajetória semestral do curso selecionado contra a média do turno`;
        activeKeys = [selectedCourseKey];
        // Adicionar um ou dois benchmarks do mesmo turno
        Object.keys(seriesDict).forEach(k => {
          if (seriesDict[k].turno === sel.turno && k !== selectedCourseKey && activeKeys.length < 3) {
            activeKeys.push(k);
          }
        });
      } else if (currentShift === 'todos') {
        titleEl.innerText = `Série Histórica Semestral: Cursos em Destaque (${tier.sheet})`;
        subtitleEl.innerText = `Trajetória dos cursos líderes dos 3 turnos (2022.1 a 2024.2)`;
        // Pegar os cursos recomendados
        activeKeys = Object.keys(seriesDict).filter(k => {
          return k.includes('Análise e Desenvolvimento') || k.includes('Desenvolvimento de Software') || k.includes('Gestão Empresarial') || k.includes('Gestão da Tecnologia');
        }).slice(0, 5);
      } else {
        titleEl.innerText = `Série Histórica: Top Cursos do Turno ${currentShift.toUpperCase()} (${tier.sheet})`;
        subtitleEl.innerText = `Curvas de concorrência semestrais (Início de ano .1 vs. Meio de ano .2)`;
        activeKeys = Object.keys(seriesDict).filter(k => seriesDict[k].turno === currentShift);
        activeKeys.sort((a,b) => seriesDict[b].media - seriesDict[a].media);
        activeKeys = activeKeys.slice(0, 5);
      }

      if (activeKeys.length === 0) {
        wrapper.innerHTML = '<div class="text-xs text-slate-400 p-4">Sem dados semestrais suficientes para esta combinação.</div>';
        legendDiv.innerHTML = '';
        return;
      }

      let maxVal = 0;
      activeKeys.forEach(k => {
        if (seriesDict[k]) {
          seriesDict[k].vals.forEach(v => {
            if (v !== null && v !== undefined) maxVal = Math.max(maxVal, v);
          });
        }
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

      // Rótulos X com marcação de sazonalidade
      semesters.forEach((sem, idx) => {
        const xPos = padLeft + idx * xStep;
        svgHtml += `<text x="${xPos}" y="${height - 8}" fill="#94a3b8" font-size="9.5" font-weight="600" text-anchor="middle">${sem}</text>`;
      });

      // Desenhar curvas
      let legendHtml = '';
      activeKeys.forEach((key, colorIdx) => {
        const s = seriesDict[key];
        if (!s) return;
        const isHighlight = (key === selectedCourseKey);
        const lineColor = isHighlight ? '#38bdf8' : colorsPalette[colorIdx % colorsPalette.length];
        const lineWidth = isHighlight ? 3.5 : 2.2;

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
          svgHtml += `<polyline fill="none" stroke="${lineColor}" stroke-width="${lineWidth}" points="${points.join(' ')}" opacity="0.9" />`;
        }

        pointsCoords.forEach(pt => {
          svgHtml += `
            <circle cx="${pt.x}" cy="${pt.y}" r="${isHighlight ? 5 : 3.5}" fill="${lineColor}" stroke="#0b111e" stroke-width="1.5"
                    class="cursor-pointer hover:r-6 transition-all"
                    onmouseover="showLineTooltip(event, '${s.curso} (${s.turno})', '${pt.sem}', ${pt.val})"
                    onmouseout="hideLineTooltip()" />
            <text x="${pt.x}" y="${pt.y - 5}" fill="${lineColor}" font-size="8" font-weight="bold" text-anchor="middle"
                  style="paint-order: stroke; stroke: #0b111e; stroke-width: 2px;">
              ${pt.val.toFixed(1)}
            </text>
          `;
        });

        legendHtml += `
          <span class="flex items-center gap-1.5 cursor-pointer hover:text-white ${isHighlight ? 'font-bold text-white underline' : ''}" onclick="selectCourse('${key}')">
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
      tt.innerHTML = `<b>${name}</b><br>Semestre: <span class="text-amber-300 font-bold">${sem}</span><br>Demanda: <span class="text-emerald-400 font-bold">${val.toFixed(2)} C/V</span>`;
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
      let courses = [...tier.courses];

      if (currentShift !== 'todos') {
        courses = courses.filter(d => d.turno === currentShift);
      }

      courses.sort((a,b) => b.media - a.media);

      courses.slice(0, 15).forEach((d, idx) => {
        const isRec = (d.status === 'RECOMENDADO' || (d.curso.includes('Análise e Desenvolvimento') && d.turno === 'Noite'));
        const isSelected = (selectedCourseKey === d.key);
        const pctBar = Math.min(100, (d.media / 12.0) * 100);
        const tr = document.createElement('tr');
        tr.className = `cursor-pointer hover:bg-slate-800/50 transition-colors ${isSelected ? 'bg-slate-800 border-l-2 border-l-cyan-400 font-bold' : ''}`;
        tr.onclick = () => selectCourse(d.key);

        let badgeText = `${idx + 1}º Lugar`;
        let badgeClass = 'bg-slate-800 text-slate-400 border border-slate-700';

        if (idx === 0) {
          badgeText = '🥇 1º Lugar (Prioritário)';
          badgeClass = 'bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold';
        } else if (idx === 1) {
          badgeText = '🥈 2º Lugar (Alternativa)';
          badgeClass = 'bg-blue-500/20 text-blue-300 border border-blue-500/40';
        } else if (idx === 2) {
          badgeText = '🥉 3º Lugar';
          badgeClass = 'bg-slate-700 text-slate-300 border border-slate-600';
        }

        const color = d.turno === 'Noite' ? '#10b981' : d.turno === 'Manhã' ? '#38bdf8' : '#f59e0b';

        tr.innerHTML = `
          <td class="py-2.5 px-3">
            <span class="inline-flex items-center gap-1.5 font-bold ${d.turno === 'Manhã' ? 'text-blue-400' : d.turno === 'Tarde' ? 'text-amber-400' : 'text-emerald-400'}">
              ${d.turno === 'Manhã' ? '🌅' : d.turno === 'Tarde' ? '☀️' : '🌙'} ${d.turno}
            </span>
          </td>
          <td class="py-2.5 px-3 text-white font-semibold flex items-center gap-1.5">
            ${isRec ? '<span title="Recomendação Oficial">⭐</span>' : ''} ${d.curso}
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
            <span class="badge ${badgeClass}">${badgeText}</span>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    // Inicialização
    updateKpis();
    updateJustifications();
    renderRankingPodium();
    renderDynamicLineChart();
    renderTable();
  </script>
</body>
</html>
"""

final_html = html_code.replace('__POP_DATA_JSON__', json_str)

out_proj = r'C:\Users\PICHAU\.gemini\antigravity\scratch\trabalho_vestibular\painel_powerbi.html'
out_art = r'C:\Users\PICHAU\.gemini\antigravity\brain\fede3023-63c1-42db-824f-ab771fa6007a\painel_powerbi.html'

with open(out_proj, 'w', encoding='utf-8') as f:
    f.write(final_html)

with open(out_art, 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Painel Power BI V4 (Interativo com Pódio e Cross-filtering) gerado com sucesso!")
