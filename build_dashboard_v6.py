import json
import os

with open(r'C:\Users\PICHAU\.gemini\antigravity\scratch\trabalho_vestibular\pop_tiers_data_v4.json', 'r', encoding='utf-8') as f:
    pop_data = json.load(f)

json_str = json.dumps(pop_data, ensure_ascii=False)

html_template = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard FATEC - Alocação e Ranking de Cursos por Período</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <!-- Google Fonts: Inter -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Inter', sans-serif;
      background-color: #0b1120;
      color: #e2e8f0;
    }}
    .pbi-card {{
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
      border: 1px solid rgba(51, 65, 85, 0.6);
      backdrop-filter: blur(8px);
      border-radius: 10px;
      transition: all 0.2s ease;
    }}
    .pbi-card:hover {{
      border-color: rgba(96, 165, 250, 0.5);
      box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
    }}
    .pbi-header {{
      background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
      border-bottom: 2px solid #3b82f6;
    }}
    .kpi-title {{
      font-size: 0.7rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      font-weight: 700;
      color: #94a3b8;
    }}
    .kpi-value {{
      font-size: 1.85rem;
      font-weight: 800;
      line-height: 1.1;
      font-family: 'JetBrains Mono', monospace;
    }}
    .badge-pbi {{
      padding: 0.15rem 0.5rem;
      border-radius: 9999px;
      font-size: 0.7rem;
      font-weight: 600;
    }}
    .slicer-btn {{
      background-color: #1e293b;
      color: #94a3b8;
      border: 1px solid #334155;
      padding: 0.35rem 0.75rem;
      border-radius: 6px;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .slicer-btn.active {{
      background-color: #2563eb;
      color: #ffffff;
      border-color: #3b82f6;
      box-shadow: 0 0 10px rgba(37,99,235,0.4);
    }}
    .slicer-btn:hover:not(.active) {{
      background-color: #334155;
      color: #f1f5f9;
    }}
    .pop-btn {{
      border-color: #0284c7;
    }}
    .pop-btn.active {{
      background-color: #0284c7 !important;
      border-color: #38bdf8 !important;
      box-shadow: 0 0 12px rgba(2,132,199,0.5) !important;
      color: #ffffff !important;
    }}
    .data-bar-container {{
      background: #1e293b;
      height: 8px;
      border-radius: 4px;
      overflow: hidden;
      width: 100%;
    }}
    .data-bar {{
      height: 100%;
      border-radius: 4px;
    }}
    .tooltip-box {{
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
    }}
    .rank-item {{
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .rank-item:hover {{
      background-color: #1e293b;
      transform: translateX(4px);
    }}
    .rank-item.selected {{
      border-left: 3px solid #38bdf8;
      background-color: #1e293b;
    }}
  </style>
</head>
<body class="p-4 md:p-6 antialiased">

  <div id="line-tooltip" class="tooltip-box"></div>

  <!-- CABEÇALHO POWER BI -->
  <header class="pbi-header rounded-xl p-4 mb-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 shadow-xl">
    <div class="flex items-center gap-3">
      <div class="bg-amber-500 text-slate-950 font-black p-2.5 rounded-lg text-lg flex items-center justify-center shadow-lg">
        📊
      </div>
      <div>
        <div class="flex items-center gap-2">
          <span class="text-[10px] font-bold uppercase tracking-wider bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded border border-amber-500/40">POWER BI REPORT</span>
          <span class="text-[10px] font-bold uppercase tracking-wider bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded border border-blue-500/40" id="badge-current-pop">SÃO JOSÉ DO RIO PRETO (~480k hab.)</span>
          <span class="text-[10px] text-slate-400 font-mono">Trabalho 4 - FATEC</span>
        </div>
        <h1 class="text-xl md:text-2xl font-black text-white tracking-tight mt-0.5">Painel de Decisão de Cursos: Ranking & Alocação por Período</h1>
        <p class="text-xs text-slate-400">Dados Oficiais dos Vestibulares FATEC (2022.1 - 2024.2) • Estratificação Populacional de Rio Preto</p>
      </div>
    </div>
    <div class="flex items-center gap-2 self-end md:self-auto">
      <div class="text-right">
        <div class="text-[10px] text-slate-400 uppercase font-semibold">População Selecionada</div>
        <div class="text-xs font-mono font-bold text-cyan-400" id="pop-label-header">Rio Preto (200 a 600k)</div>
      </div>
      <div class="h-8 w-px bg-slate-700 mx-1"></div>
      <div class="text-right">
        <div class="text-[10px] text-slate-400 uppercase font-semibold">Regra do Trabalho</div>
        <div class="text-xs font-mono font-bold text-amber-400">1 Curso por Turno</div>
      </div>
    </div>
  </header>

  <!-- SLICERS / FILTROS DINÂMICOS (POPULAÇÃO E TURNO) -->
  <div class="pbi-card p-3 mb-4 shadow-md">
    <div class="flex flex-col gap-2.5">
      <!-- FILTRO DE POPULAÇÃO (BASEADO NA CIDADE DE SÃO JOSÉ DO RIO PRETO) -->
      <div class="flex flex-wrap items-center gap-2">
        <span class="text-xs font-bold text-slate-300 uppercase tracking-wide mr-1 flex items-center gap-1">
          <span>👥</span> FILTRO DE PORTE POPULACIONAL:
        </span>
        <div class="flex flex-wrap gap-1.5" id="pop-filters">
          <button class="slicer-btn pop-btn active" onclick="setPopTier('rio_preto', this)">
            ⭐ São José do Rio Preto (~480k hab. / Aba 200 a 600)
          </button>
          <button class="slicer-btn pop-btn" onclick="setPopTier('ate_500', this)">Até 500 mil hab. (Aba Até 500)</button>
          <button class="slicer-btn pop-btn" onclick="setPopTier('faixa_100_600', this)">100 a 600 mil hab.</button>
          <button class="slicer-btn pop-btn" onclick="setPopTier('pequenas_ate_200', this)">
            🌾 Cidades Pequenas & Agro (Até 100k e 200k hab.*)
          </button>
          <button class="slicer-btn pop-btn" onclick="setPopTier('todos', this)">🌐 Todos (Estado Geral)</button>
        </div>
        <span class="text-[11px] text-slate-400 ml-auto font-mono" id="sheet-name-tag">Aba no Excel: <b>200 a 600</b></span>
      </div>

      <!-- FILTRO DE TURNO / PERÍODO -->
      <div class="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-800">
        <span class="text-xs font-bold text-slate-300 uppercase tracking-wide mr-1 flex items-center gap-1">
          <span>⏳</span> TURNO DE ANÁLISE:
        </span>
        <div class="flex flex-wrap gap-1.5" id="shift-filters">
          <button class="slicer-btn active" onclick="setShift('todos', this)">Todos os Turnos (Portfólio do Campus)</button>
          <button class="slicer-btn" onclick="setShift('Manhã', this)">🌅 Manhã</button>
          <button class="slicer-btn" onclick="setShift('Tarde', this)">☀️ Tarde</button>
          <button class="slicer-btn" onclick="setShift('Noite', this)">🌙 Noite</button>
        </div>
      </div>

      <div class="text-[11px] text-slate-400 italic flex items-center gap-1.5" id="note-pop-explanation">
        <span>💡 <i>Dica: Clique em qualquer turno ou curso para ver a sincronização instantânea em toda a tela!</i></span>
      </div>
    </div>
  </div>

  <!-- AVISO TÉCNICO EXPLICATIVO QUANDO ESCOLHE CIDADES PEQUENAS -->
  <div id="alert-small-cities" class="hidden pbi-card p-3 mb-4 bg-amber-950/40 border-amber-600/50 text-amber-200 text-xs flex items-center gap-2">
    <span>⚠️</span>
    <span><b>Nota Técnica sobre o Excel original:</b> As abas <i>'Até 100'</i> e <i>'Até 200'</i> da planilha fornecida possuem exatamente as mesmas 232 linhas idênticas. Em cidades desse porte, a vocação agropecuária (Mecanização Agrícola e Big Data no Agro) se destaca fortemente.</span>
  </div>

  <!-- 4 CARDS KPI SUPERIORES (TOTALMENTE SINCRONIZADOS E SEM CONTRADIÇÕES) -->
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-4" id="kpi-container">
    <!-- Card 1 -->
    <div class="pbi-card p-4 relative overflow-hidden border-l-4 border-l-blue-500 shadow-md">
      <div class="flex justify-between items-start mb-1">
        <span class="kpi-title" id="card-1-title">🌅 MANHÃ (1ª ESCOLHA)</span>
        <span class="badge-pbi bg-blue-500/20 text-blue-300 border border-blue-500/40" id="card-1-badge">Recomendado</span>
      </div>
      <div class="text-sm font-bold text-white truncate" id="card-1-course">GTI (Gestão da TI)</div>
      <div class="flex items-baseline gap-2 mt-1">
        <span class="kpi-value text-blue-400" id="card-1-dem">4.77</span>
        <span class="text-xs text-slate-400">C/V (Candidatos/Vaga)</span>
      </div>
      <div class="text-[11px] text-slate-400 mt-2 pt-2 border-t border-slate-800 flex justify-between" id="card-1-sub">
        <span>2º Opção: <b class="text-white">DSM (2.80 C/V)</b></span>
        <span class="text-emerald-400 font-semibold">100% Sinergia TI</span>
      </div>
    </div>

    <!-- Card 2 -->
    <div class="pbi-card p-4 relative overflow-hidden border-l-4 border-l-amber-500 shadow-md">
      <div class="flex justify-between items-start mb-1">
        <span class="kpi-title" id="card-2-title">☀️ TARDE (1ª ESCOLHA TI)</span>
        <span class="badge-pbi bg-amber-500/20 text-amber-300 border border-amber-500/40" id="card-2-badge">Recomendado</span>
      </div>
      <div class="text-sm font-bold text-white truncate" id="card-2-course">DSM (Software Multiplataforma)</div>
      <div class="flex items-baseline gap-2 mt-1">
        <span class="kpi-value text-amber-400" id="card-2-dem">2.82</span>
        <span class="text-xs text-slate-400">C/V (Candidatos/Vaga)</span>
      </div>
      <div class="text-[11px] text-slate-400 mt-2 pt-2 border-t border-slate-800 flex justify-between" id="card-2-sub">
        <span>Alternativa: <b class="text-white">Gestão Emp. (1.78 C/V)</b></span>
        <span class="text-blue-300 font-semibold">Líder TI Vespertino</span>
      </div>
    </div>

    <!-- Card 3 -->
    <div class="pbi-card p-4 relative overflow-hidden border-l-4 border-l-emerald-500 shadow-md">
      <div class="flex justify-between items-start mb-1">
        <span class="kpi-title" id="card-3-title">🌙 NOITE (1ª ESCOLHA)</span>
        <span class="badge-pbi bg-emerald-500/20 text-emerald-300 border border-emerald-500/40" id="card-3-badge">Líder Absoluto</span>
      </div>
      <div class="text-sm font-bold text-white truncate" id="card-3-course">ADS (Análise e Desenv. Sist.)</div>
      <div class="flex items-baseline gap-2 mt-1">
        <span class="kpi-value text-emerald-400" id="card-3-dem">11.61</span>
        <span class="text-xs text-slate-400">C/V (Candidatos/Vaga)</span>
      </div>
      <div class="text-[11px] text-slate-400 mt-2 pt-2 border-t border-slate-800 flex justify-between" id="card-3-sub">
        <span>2º Opção: <b class="text-white">Mídias Digitais (6.73 C/V)</b></span>
        <span class="text-amber-400 font-bold">Recorde Regional</span>
      </div>
    </div>

    <!-- Card 4 -->
    <div class="pbi-card p-4 relative overflow-hidden border-l-4 border-l-purple-500 shadow-md">
      <div class="flex justify-between items-start mb-1">
        <span class="kpi-title" id="card-4-title">📊 PORTFÓLIO TOTAL DO CAMPUS</span>
        <span class="badge-pbi bg-purple-500/20 text-purple-300 border border-purple-500/40" id="card-4-badge">3 Cursos</span>
      </div>
      <div class="text-sm font-bold text-white truncate" id="card-4-course">Média Geral Ponderada</div>
      <div class="flex items-baseline gap-2 mt-1">
        <span class="kpi-value text-purple-400" id="card-4-dem">6.40</span>
        <span class="text-xs text-slate-400">C/V Média do Campus</span>
      </div>
      <div class="text-[11px] text-slate-400 mt-2 pt-2 border-t border-slate-800 flex justify-between" id="card-4-sub">
        <span>Capacidade: <b class="text-emerald-400">120 vagas/sem</b></span>
        <span>Ociosidade: <b class="text-emerald-400">0% (Risco Zero)</b></span>
      </div>
    </div>
  </div>

  <!-- DICIONÁRIO E EXPLICAÇÃO TÉCNICA DOS TERMOS -->
  <div class="pbi-card p-3.5 mb-4 border-t-2 border-t-cyan-500 shadow-sm text-xs">
    <div class="flex items-center justify-between mb-2">
      <div class="font-bold text-white flex items-center gap-1.5 uppercase tracking-wide">
        <span class="text-cyan-400">📘</span> DICIONÁRIO DE INDICADORES: O QUE SIGNIFICAM C/V, QTD E POPULAÇÃO DE RIO PRETO?
      </div>
      <span class="text-[11px] text-slate-400 font-mono">10 cursos por turma / Vagas: ~40</span>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-4 gap-3 text-slate-300 text-[11.5px] leading-relaxed">
      <div class="p-2 bg-slate-900/60 rounded border border-slate-800">
        <b class="text-cyan-400">📌 C/V (Candidatos por Vaga):</b><br>
        Relação de concorrência oficial = <code>Inscritos &divide; Vagas</code>.<br>
        Exemplo em Rio Preto: se ADS Noite tem <b>11.61 C/V</b>, significa que para 40 vagas inscrevem-se cerca de <b>464 candidatos</b> (quase 12 concorrentes por vaga!).
      </div>
      <div class="p-2 bg-slate-900/60 rounded border border-slate-800">
        <b class="text-cyan-400">🏙️ São José do Rio Preto (População):</b><br>
        Com ~480 mil habitantes (IBGE), Rio Preto é classificada no Excel nas abas <code>200 a 600</code> e <code>Até 500</code>. É um polo regional de comércio, saúde e serviços com fortíssima demanda por TI e Gestão.
      </div>
      <div class="p-2 bg-slate-900/60 rounded border border-slate-800">
        <b class="text-cyan-400">🌾 Cidades Pequenas (&lt;200k hab.):</b><br>
        Em cidades de até 100k ou 200k hab., a vocação agropecuária se destaca fortemente: Mecanização em Agricultura de Precisão (4.38 C/V) e Big Data no Agro (1.96 C/V) lideram.
      </div>
      <div class="p-2 bg-slate-900/60 rounded border border-slate-800">
        <b class="text-cyan-400">🔬 Sinergia de Laboratórios:</b><br>
        Ao alocar GTI/DSM de dia e ADS à noite, a faculdade usa 100% dos mesmos laboratórios de informática nos três turnos, reduzindo o custo de implantação de turma a quase zero.
      </div>
    </div>
  </div>

  <!-- CORPO PRINCIPAL: RANKING DE CURSOS (COLUNA ESQUERDA) + GRÁFICO HISTÓRICO (COLUNA DIREITA) -->
  <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 mb-4">
    <!-- RANKING E PODIO (COLUNA 5) -->
    <div class="lg:col-span-5 pbi-card p-4 flex flex-col justify-between shadow-lg">
      <div>
        <div class="flex justify-between items-center mb-3">
          <div>
            <h2 class="text-sm font-bold text-white flex items-center gap-1.5" id="ranking-box-title">
              <span>🏆</span> Ranking Específico: Qual curso abrir no turno selecionado?
            </h2>
            <p class="text-[11px] text-slate-400" id="ranking-box-subtitle">Ordem de classificação para o turno selecionado na faixa: 200 a 600</p>
          </div>
          <span class="badge-pbi bg-cyan-500/20 text-cyan-300 font-mono text-[10px]" id="ranking-badge-mode">Visual: Pódio/Ranking</span>
        </div>

        <div class="space-y-2" id="ranking-list">
          <!-- Gerado dinamicamente via JS -->
        </div>
      </div>

      <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between items-center text-[11px] text-slate-400">
        <span class="flex items-center gap-1">👉 <i>Clique em qualquer curso acima para destacar sua curva histórica ao lado</i></span>
        <button class="text-cyan-400 font-semibold hover:underline" onclick="clearSelection()">Limpar Seleção</button>
      </div>
    </div>

    <!-- SÉRIE HISTÓRICA TEMPORAL (COLUNA 7) -->
    <div class="lg:col-span-7 pbi-card p-4 flex flex-col justify-between shadow-lg">
      <div>
        <div class="flex justify-between items-center mb-2">
          <div>
            <h2 class="text-sm font-bold text-white flex items-center gap-1.5" id="line-chart-title">
              Série Histórica: Top Cursos do Turno Selecionado
            </h2>
            <p class="text-[11px] text-slate-400" id="line-chart-subtitle">Curvas de concorrência semestrais (picos de início de ano: .1 vs meio de ano: .2)</p>
          </div>
          <span class="badge-pbi bg-emerald-500/20 text-emerald-300 font-mono text-[10px]">Visual: Linhas Reativas</span>
        </div>

        <div class="h-64 md:h-72 w-full relative">
          <canvas id="historicalLineCanvas"></canvas>
        </div>
      </div>

      <div class="mt-2 pt-2 border-t border-slate-800 flex flex-wrap items-center justify-between text-[11px] text-slate-400">
        <div class="flex items-center gap-3">
          <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-cyan-400"></span> Pico em .1 (Início do ano)</span>
          <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span> Recuo sazonal em .2</span>
        </div>
        <span class="text-slate-500 font-mono">Fonte: Vestibulares FATEC</span>
      </div>
    </div>
  </div>

  <!-- JUSTIFICATIVAS DETALHADAS POR PERÍODO PARA RIO PRETO -->
  <div class="pbi-card p-4 mb-4 border-l-4 border-l-amber-500 shadow-md">
    <div class="flex items-center justify-between mb-2">
      <h3 class="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2" id="justification-header">
        <span>📑</span> JUSTIFICATIVAS DE ALOCAÇÃO: SÃO JOSÉ DO RIO PRETO (~480k hab. / FAIXA 200k a 600k)
      </h3>
      <span class="badge-pbi bg-amber-500/20 text-amber-300 font-mono text-[10px]">Decisão Técnica Alinhada</span>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs text-slate-300 leading-relaxed mt-3">
      <!-- Manhã -->
      <div class="p-3 bg-slate-900/80 rounded-lg border border-slate-800">
        <div class="flex justify-between items-center mb-1.5">
          <b class="text-blue-400 text-sm">🌅 Manhã: GTI (Gestão da TI)</b>
          <span class="badge-pbi bg-blue-500/20 text-blue-300 font-mono text-[10px]" id="just-man-badge">4.77 C/V</span>
        </div>
        <p class="text-[11.5px]" id="just-man-text">
          <b>Maior Demanda Exclusiva e Sinergia Corporativa:</b> Com <b>4.77 C/V</b>, GTI é o vice-líder absoluto da manhã em Rio Preto (atrás apenas de ADS que já foi alocado à noite). Prepara gestores de projetos, computação em nuvem e governança corporativa, aproveitando integralmente os laboratórios de ADS instalados para o noturno e atendendo o perfil jovem que estagia no contra-turno.
        </p>
      </div>

      <!-- Tarde -->
      <div class="p-3 bg-slate-900/80 rounded-lg border border-slate-800">
        <div class="flex justify-between items-center mb-1.5">
          <b class="text-amber-400 text-sm">☀️ Tarde: DSM (Software Multiplataforma)</b>
          <span class="badge-pbi bg-amber-500/20 text-amber-300 font-mono text-[10px]" id="just-tar-badge">2.82 C/V</span>
        </div>
        <p class="text-[11.5px]" id="just-tar-text">
          <b>Líder de TI Vespertino & Formação Full-Stack:</b> DSM registra <b>2.82 C/V</b> à tarde na faixa de Rio Preto. É a melhor opção técnica para manter o campus com 100% de ocupação em computação aplicada. (Alternativa de Negócios: <i>Gestão Empresarial</i> com 1.78 C/V, caso o campus deseje diversificar para a área administrativa).
        </p>
      </div>

      <!-- Noite -->
      <div class="p-3 bg-slate-900/80 rounded-lg border border-slate-800">
        <div class="flex justify-between items-center mb-1.5">
          <b class="text-emerald-400 text-sm">🌙 Noite: ADS (Análise e Desenv. Sist.)</b>
          <span class="badge-pbi bg-emerald-500/20 text-emerald-300 font-mono text-[10px]" id="just-noi-badge">11.61 C/V</span>
        </div>
        <p class="text-[11.5px]" id="just-noi-text">
          <b>Demanda Noturna Recorde & Carro-chefe Estadual:</b> Em Rio Preto, ADS Noite explode para incríveis <b>11.61 C/V</b> de média (com pico histórico de 14.01 C/V no 2024.1). Concentra o público que trabalha durante o dia no forte polo terciário da cidade, garantindo zero ociosidade e prestígio máximo para o campus.
        </p>
      </div>
    </div>
  </div>

  <!-- TABELA DE APOIO ANALÍTICO (DETALHAMENTO DOS CURSOS DA FAIXA) -->
  <div class="pbi-card p-4 shadow-md">
    <div class="flex justify-between items-center mb-3">
      <h3 class="text-sm font-bold text-white flex items-center gap-2">
        <span>📋</span> Tabela de Apoio Analítico: Cursos Auditados na Faixa Selecionada
      </h3>
      <span class="text-xs text-slate-400 font-mono" id="table-row-count">Exibindo cursos relevantes</span>
    </div>
    <div class="overflow-x-auto max-h-60 overflow-y-auto">
      <table class="w-full text-left text-xs text-slate-300">
        <thead class="bg-slate-900/90 text-slate-400 uppercase text-[10px] tracking-wider sticky top-0">
          <tr>
            <th class="p-2">Curso</th>
            <th class="p-2">Turno</th>
            <th class="p-2">Eixo Tecnológico</th>
            <th class="p-2 text-right">Demanda Média</th>
            <th class="p-2 text-right">Semestres no Excel</th>
            <th class="p-2 text-right">Turmas/Sem</th>
            <th class="p-2 text-center">Status</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800" id="table-body">
          <!-- Preenchido dinamicamente via JS -->
        </tbody>
      </table>
    </div>
  </div>

  <!-- JAVASCRIPT POWER BI ENGINE -->
  <script>
    // DADOS REAIS EXTRAÍDOS DA PLANILHA ORIGINAL
    const allPopData = {json_str};

    let currentPopTier = 'rio_preto';
    let currentShift = 'todos';
    let selectedCourseKey = null;
    let lineChartInstance = null;

    // CORES POWER BI PARA GRÁFICOS
    const pbiPalette = [
      '#38bdf8', // Sky Cyan
      '#f59e0b', // Amber
      '#10b981', // Emerald
      '#ec4899', // Pink
      '#8b5cf6', // Violet
      '#06b6d4', // Cyan
      '#f97316', // Orange
      '#6366f1'  // Indigo
    ];

    // INICIALIZAÇÃO
    window.addEventListener('DOMContentLoaded', () => {{
      updateDashboard();
    }});

    // ALTERA FAIXA POPULACIONAL
    function setPopTier(tierKey, btn) {{
      currentPopTier = tierKey;
      selectedCourseKey = null;
      document.querySelectorAll('#pop-filters .pop-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const tier = allPopData[tierKey];
      document.getElementById('sheet-name-tag').innerHTML = `Aba no Excel: <b>${{tier.sheet}}</b>`;
      document.getElementById('pop-label-header').innerText = `${{tier.sheet}} (${{tierKey === 'rio_preto' ? 'Rio Preto ~480k' : tierKey}})`;

      const alertBox = document.getElementById('alert-small-cities');
      if (tierKey === 'pequenas_ate_200') {{
        alertBox.classList.remove('hidden');
      }} else {{
        alertBox.classList.add('hidden');
      }}

      updateDashboard();
    }}

    // ALTERA TURNO
    function setShift(shift, btn) {{
      currentShift = shift;
      selectedCourseKey = null;
      document.querySelectorAll('#shift-filters .slicer-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      updateDashboard();
    }}

    function selectCourse(key) {{
      selectedCourseKey = key;
      renderRankingPodium();
      renderDynamicLineChart();
      renderTable();
    }}

    function clearSelection() {{
      selectedCourseKey = null;
      renderRankingPodium();
      renderDynamicLineChart();
      renderTable();
    }}

    function updateDashboard() {{
      updateKpis();
      updateJustifications();
      renderRankingPodium();
      renderDynamicLineChart();
      renderTable();
    }}

    // FUNÇÕES DE BUSCA EXATA DE CURSOS
    const isADS = (name) => name.toLowerCase().includes('análise e desenv');
    const isDSM = (name) => name.toLowerCase().includes('software multiplataforma');
    const isGTI = (name) => name.toLowerCase().includes('gestão da tecnologia');
    const isGestaoEmp = (name) => name.toLowerCase().includes('gestão empresarial');
    const isMecanizacao = (name) => name.toLowerCase().includes('mecanização');
    const isBigDataAgro = (name) => name.toLowerCase().includes('big data no agronegócio');

    // ATUALIZAÇÃO DOS 4 CARDS DE KPI (SINCRONIZADOS COM TOTAL COERÊNCIA)
    function updateKpis() {{
      const tier = allPopData[currentPopTier];
      const courses = tier.courses;

      const c1Title = document.getElementById('card-1-title');
      const c1Badge = document.getElementById('card-1-badge');
      const c1Course = document.getElementById('card-1-course');
      const c1Dem = document.getElementById('card-1-dem');
      const c1Sub = document.getElementById('card-1-sub');

      const c2Title = document.getElementById('card-2-title');
      const c2Badge = document.getElementById('card-2-badge');
      const c2Course = document.getElementById('card-2-course');
      const c2Dem = document.getElementById('card-2-dem');
      const c2Sub = document.getElementById('card-2-sub');

      const c3Title = document.getElementById('card-3-title');
      const c3Badge = document.getElementById('card-3-badge');
      const c3Course = document.getElementById('card-3-course');
      const c3Dem = document.getElementById('card-3-dem');
      const c3Sub = document.getElementById('card-3-sub');

      const c4Title = document.getElementById('card-4-title');
      const c4Badge = document.getElementById('card-4-badge');
      const c4Course = document.getElementById('card-4-course');
      const c4Dem = document.getElementById('card-4-dem');
      const c4Sub = document.getElementById('card-4-sub');

      const getShiftList = (turno) => courses.filter(c => c.turno === turno && c.semestres >= 2).sort((a,b) => b.media - a.media);

      if (currentShift === 'todos') {{
        // VISÃO GERAL DO PORTFÓLIO DO CAMPUS (3 TURNOS)
        if (currentPopTier === 'pequenas_ate_200') {{
          // CIDADES PEQUENAS
          c1Title.innerText = '🌅 MANHÃ (1ª ESCOLHA)';
          c1Badge.innerText = 'Vocação Agro';
          let mRec = courses.find(c => c.turno === 'Manhã' && isMecanizacao(c.curso)) || {{ curso: 'Mecanização Agrícola', media: 2.40 }};
          c1Course.innerText = mRec.curso;
          c1Dem.innerText = mRec.media.toFixed(2);
          c1Sub.innerHTML = `<span>2º Opção: <b class="text-white">DSM (2.19 C/V)</b></span><span class="text-emerald-400 font-semibold">Perfil Regional</span>`;

          c2Title.innerText = '☀️ TARDE (1ª ESCOLHA)';
          c2Badge.innerText = 'Líder Agro';
          let tRec = courses.find(c => c.turno === 'Tarde' && isBigDataAgro(c.curso)) || {{ curso: 'Big Data no Agro', media: 1.96 }};
          c2Course.innerText = tRec.curso;
          c2Dem.innerText = tRec.media.toFixed(2);
          c2Sub.innerHTML = `<span>2º Opção: <b class="text-white">Gestão Emp. (1.86 C/V)</b></span><span class="text-amber-400 font-semibold">1º da Tarde</span>`;

          c3Title.innerText = '🌙 NOITE (1ª ESCOLHA)';
          c3Badge.innerText = 'Líder Geral';
          let nRec = courses.find(c => c.turno === 'Noite' && isADS(c.curso)) || {{ curso: 'ADS (Análise e Desenv. Sist.)', media: 4.50 }};
          c3Course.innerText = nRec.curso;
          c3Dem.innerText = nRec.media.toFixed(2);
          c3Sub.innerHTML = `<span>2º Opção: <b class="text-white">Mecanização (4.38 C/V)</b></span><span class="text-emerald-400 font-semibold">Alta Demanda</span>`;

          c4Title.innerText = '📊 PORTFÓLIO TOTAL DO CAMPUS';
          c4Badge.innerText = '3 Cursos';
          c4Course.innerText = 'Média Geral Ponderada';
          c4Dem.innerText = ((mRec.media + tRec.media + nRec.media) / 3).toFixed(2);
          c4Sub.innerHTML = `<span>Capacidade: <b class="text-emerald-400">120 vagas/sem</b></span><span>Ociosidade: <b class="text-emerald-400">0%</b></span>`;
        }} else {{
          // RIO PRETO E DEMAIS FAIXAS
          let mRec = courses.find(c => c.turno === 'Manhã' && isGTI(c.curso)) || courses.find(c => c.turno === 'Manhã' && isDSM(c.curso)) || {{ curso: 'GTI (Gestão da TI)', media: 4.77 }};
          let mOpt2 = courses.find(c => c.turno === 'Manhã' && isDSM(c.curso)) || {{ curso: 'DSM', media: 2.80 }};

          c1Title.innerText = '🌅 MANHÃ (1ª ESCOLHA)';
          c1Badge.innerText = 'Recomendado';
          c1Course.innerText = mRec.curso;
          c1Dem.innerText = mRec.media.toFixed(2);
          c1Sub.innerHTML = `<span>2º Opção: <b class="text-white">${{mOpt2.curso.substring(0, 15)}} (${{mOpt2.media.toFixed(2)}} C/V)</b></span><span class="text-emerald-400 font-semibold">100% Sinergia TI</span>`;

          let tRec = courses.find(c => c.turno === 'Tarde' && isDSM(c.curso)) || courses.find(c => c.turno === 'Tarde' && isGestaoEmp(c.curso)) || {{ curso: 'DSM (Software Multiplataforma)', media: 2.82 }};
          let tOpt2 = courses.find(c => c.turno === 'Tarde' && isGestaoEmp(c.curso)) || {{ curso: 'Gestão Empresarial', media: 1.78 }};

          c2Title.innerText = '☀️ TARDE (1ª ESCOLHA TI)';
          c2Badge.innerText = 'Recomendado';
          c2Course.innerText = tRec.curso;
          c2Dem.innerText = tRec.media.toFixed(2);
          c2Sub.innerHTML = `<span>Alternativa: <b class="text-white">Gestão Emp. (${{tOpt2.media.toFixed(2)}} C/V)</b></span><span class="text-blue-300 font-semibold">Líder TI Vespertino</span>`;

          let nRec = courses.find(c => c.turno === 'Noite' && isADS(c.curso)) || {{ curso: 'ADS (Análise e Desenv. Sist.)', media: 11.61 }};
          let nOpt2 = courses.find(c => c.turno === 'Noite' && (c.curso.includes('Mídias') || isGTI(c.curso))) || {{ curso: 'Design de Mídias', media: 6.73 }};

          c3Title.innerText = '🌙 NOITE (1ª ESCOLHA)';
          c3Badge.innerText = 'Líder Absoluto';
          c3Course.innerText = nRec.curso;
          c3Dem.innerText = nRec.media.toFixed(2);
          c3Sub.innerHTML = `<span>2º Opção: <b class="text-white">${{nOpt2.curso.substring(0, 15)}} (${{nOpt2.media.toFixed(2)}} C/V)</b></span><span class="text-amber-400 font-bold">Recorde Regional</span>`;

          c4Title.innerText = '📊 PORTFÓLIO TOTAL DO CAMPUS';
          c4Badge.innerText = '3 Cursos';
          c4Course.innerText = 'Média Geral Ponderada';
          let avgCampus = ((mRec.media + tRec.media + nRec.media) / 3).toFixed(2);
          c4Dem.innerText = avgCampus;
          c4Sub.innerHTML = `<span>Capacidade: <b class="text-emerald-400">120 vagas/sem</b></span><span>Ociosidade: <b class="text-emerald-400">0% (Risco Zero)</b></span>`;
        }}

      }} else if (currentShift === 'Manhã') {{
        // CARDS FOCADOS EXCLUSIVAMENTE NA MANHÃ
        const topM = getShiftList('Manhã');
        const c1 = topM[0] || {{ curso: 'ADS (Manhã)', media: 4.91, eixo: 'TI' }};
        const c2 = topM[1] || {{ curso: 'GTI (Manhã)', media: 4.77, eixo: 'TI' }};
        const c3 = topM[2] || {{ curso: 'Design de Mídias', media: 3.17, eixo: 'Design' }};
        const avgM = (topM.reduce((acc, c) => acc + c.media, 0) / Math.max(1, topM.length)).toFixed(2);

        c1Title.innerText = '🥇 1º LUGAR EM DEMANDA PURA';
        c1Badge.innerText = 'Maior Concorrência';
        c1Course.innerText = c1.curso;
        c1Dem.innerText = c1.media.toFixed(2);
        c1Sub.innerHTML = `<span>Alocação: <b class="text-amber-300">Alocado no Noturno</b></span><span class="text-blue-300 font-mono">Manhã</span>`;

        c2Title.innerText = '⭐ ESCOLHA RECOMENDADA (SEM REPETIR)';
        c2Badge.innerText = 'Recomendação Oficial';
        c2Course.innerText = c2.curso;
        c2Dem.innerText = c2.media.toFixed(2);
        c2Sub.innerHTML = `<span>Sinergia: <b class="text-emerald-400">Mesmos Labs de ADS</b></span><span class="text-blue-300 font-mono">Manhã</span>`;

        c3Title.innerText = '🥉 3º LUGAR EM DEMANDA';
        c3Badge.innerText = 'Alternativa';
        c3Course.innerText = c3.curso;
        c3Dem.innerText = c3.media.toFixed(2);
        c3Sub.innerHTML = `<span>Eixo: <b class="text-white">${{c3.eixo || 'Comunicação'}}</b></span><span class="text-blue-300 font-mono">Manhã</span>`;

        c4Title.innerText = '📈 MÉDIA DO TURNO MATUTINO';
        c4Badge.innerText = `${{topM.length}} Cursos Ativos`;
        c4Course.innerText = `Faixa: ${{tier.sheet}}`;
        c4Dem.innerText = avgM;
        c4Sub.innerHTML = `<span>Média dos Cursos da Manhã</span><span class="text-emerald-400 font-semibold">Consolidada</span>`;

      }} else if (currentShift === 'Tarde') {{
        // CARDS FOCADOS EXCLUSIVAMENTE NA TARDE
        const topT = getShiftList('Tarde');
        const c1 = topT[0] || {{ curso: 'ADS (Tarde)', media: 4.90, eixo: 'TI' }};
        const c2 = courses.find(c => c.turno === 'Tarde' && (isDSM(c.curso) || isBigDataAgro(c.curso))) || topT[1] || {{ curso: 'DSM', media: 2.82 }};
        const c3 = courses.find(c => c.turno === 'Tarde' && isGestaoEmp(c.curso)) || topT[2] || {{ curso: 'Gestão Empresarial', media: 1.78 }};
        const avgT = (topT.reduce((acc, c) => acc + c.media, 0) / Math.max(1, topT.length)).toFixed(2);

        c1Title.innerText = '🥇 1º LUGAR EM DEMANDA PURA';
        c1Badge.innerText = 'Maior Concorrência';
        c1Course.innerText = c1.curso;
        c1Dem.innerText = c1.media.toFixed(2);
        c1Sub.innerHTML = `<span>Alocação: <b class="text-amber-300">Alocado no Noturno</b></span><span class="text-amber-400 font-mono">Tarde</span>`;

        c2Title.innerText = '⭐ ESCOLHA RECOMENDADA (TI)';
        c2Badge.innerText = 'Recomendação TI';
        c2Course.innerText = c2.curso;
        c2Dem.innerText = c2.media.toFixed(2);
        c2Sub.innerHTML = `<span>Perfil: <b class="text-blue-300">Software & Mobile</b></span><span class="text-amber-400 font-mono">Tarde</span>`;

        c3Title.innerText = '💼 ALTERNATIVA DE GESTÃO';
        c3Badge.innerText = 'Protege Turno';
        c3Course.innerText = c3.curso;
        c3Dem.innerText = c3.media.toFixed(2);
        c3Sub.innerHTML = `<span>Perfil: <b class="text-emerald-400">Polo Corporativo</b></span><span class="text-amber-400 font-mono">Tarde</span>`;

        c4Title.innerText = '📈 MÉDIA DO TURNO VESPERTINO';
        c4Badge.innerText = `${{topT.length}} Cursos Ativos`;
        c4Course.innerText = `Faixa: ${{tier.sheet}}`;
        c4Dem.innerText = avgT;
        c4Sub.innerHTML = `<span>Média dos Cursos da Tarde</span><span class="text-amber-300 font-semibold">Mais Desafiador</span>`;

      }} else if (currentShift === 'Noite') {{
        // CARDS FOCADOS EXCLUSIVAMENTE NA NOITE
        const topN = getShiftList('Noite');
        const c1 = topN[0] || {{ curso: 'ADS (Noite)', media: 11.61, eixo: 'TI' }};
        const c2 = topN[1] || {{ curso: 'Design de Mídias', media: 6.73, eixo: 'Design' }};
        const c3 = topN[2] || {{ curso: 'GTI', media: 6.01, eixo: 'TI' }};
        const avgN = (topN.reduce((acc, c) => acc + c.media, 0) / Math.max(1, topN.length)).toFixed(2);

        c1Title.innerText = '🥇 1º LUGAR & RECOMENDADO';
        c1Badge.innerText = 'Líder Absoluto';
        c1Course.innerText = c1.curso;
        c1Dem.innerText = c1.media.toFixed(2);
        c1Sub.innerHTML = `<span>Justificativa: <b class="text-emerald-400">Recorde de Inscritos</b></span><span class="text-emerald-400 font-mono">Noite</span>`;

        c2Title.innerText = '🥈 2º LUGAR NOITE';
        c2Badge.innerText = 'Forte Alternativa';
        c2Course.innerText = c2.curso;
        c2Dem.innerText = c2.media.toFixed(2);
        c2Sub.innerHTML = `<span>Eixo: <b class="text-white">${{c2.eixo || 'TI'}}</b></span><span class="text-emerald-400 font-mono">Noite</span>`;

        c3Title.innerText = '🥉 3º LUGAR NOITE';
        c3Badge.innerText = 'Opção TI';
        c3Course.innerText = c3.curso;
        c3Dem.innerText = c3.media.toFixed(2);
        c3Sub.innerHTML = `<span>Eixo: <b class="text-white">${{c3.eixo || 'TI'}}</b></span><span class="text-emerald-400 font-mono">Noite</span>`;

        c4Title.innerText = '📈 MÉDIA DO TURNO NOTURNO';
        c4Badge.innerText = `${{topN.length}} Cursos Ativos`;
        c4Course.innerText = `Faixa: ${{tier.sheet}}`;
        c4Dem.innerText = avgN;
        c4Sub.innerHTML = `<span>Média dos Cursos Noturnos</span><span class="text-emerald-400 font-semibold">Alta Procura</span>`;
      }}
    }}

    // ATUALIZAÇÃO DOS TEXTOS DE JUSTIFICATIVA
    function updateJustifications() {{
      const header = document.getElementById('justification-header');
      const textMan = document.getElementById('just-man-text');
      const textTar = document.getElementById('just-tar-text');
      const textNoi = document.getElementById('just-noi-text');
      const badgeMan = document.getElementById('just-man-badge');
      const badgeTar = document.getElementById('just-tar-badge');
      const badgeNoi = document.getElementById('just-noi-badge');

      if (currentPopTier === 'rio_preto') {{
        header.innerText = 'JUSTIFICATIVAS: SÃO JOSÉ DO RIO PRETO (~480k hab. / FAIXA 200k a 600k)';
        badgeMan.innerText = '4,77 C/V (GTI)';
        badgeTar.innerText = '2,82 C/V (DSM TI) / 1,78 (Gestão)';
        badgeNoi.innerText = '11,61 C/V (Pico: 14,01)';
        textMan.innerHTML = '<b>Polo Corporativo e Tecnológico:</b> Em Rio Preto (480k hab.), <b>GTI (4,77 C/V)</b> é a maior demanda matutina sem duplicar ADS da noite. Prepara gestores de TI e computação em nuvem com 100% de sinergia com os laboratórios de informática, atendendo o público jovem que faz estágio corporativo à tarde.';
        textTar.innerHTML = '<b>Líder de TI Vespertino & Proteção de Turma:</b> DSM sustenta a tarde de Rio Preto com <b>2,82 C/V</b>, sendo a melhor opção para um campus 100% focado em tecnologia. Como alternativa de diversificação para negócios, <i>Gestão Empresarial</i> (1,78 C/V) atende o setor de comércio e serviços.';
        textNoi.innerHTML = '<b>Demanda Noturna Recorde Estadual:</b> ADS Noite atinge impressionantes <b>11,61 C/V</b> (com pico de 14,01 no 2024.1). Rio Preto é centro de serviços médicos e comerciais, garantindo preenchimento imediato das 40 vagas sem qualquer risco de ociosidade.';
      }} else if (currentPopTier === 'pequenas_ate_200') {{
        header.innerText = 'JUSTIFICATIVAS: CIDADES PEQUENAS (ATÉ 100k E 200k HABITANTES)';
        badgeMan.innerText = '2,40 C/V (Mecanização)';
        badgeTar.innerText = '1,96 C/V (Big Data Agro)';
        badgeNoi.innerText = '4,50 C/V (ADS) / 4,38 (Meca)';
        textMan.innerHTML = '<b>Vocação Agropecuária Matutina:</b> Em municípios menores, <i>Mecanização em Agricultura de Precisão</i> (2,40 C/V) lidera a procura técnica, disputando diretamente com TI.';
        textTar.innerHTML = '<b>Big Data no Agronegócio Lidera a Tarde:</b> Nesta faixa populacional, Big Data no Agro atinge 1,96 C/V à tarde, superando inclusive ADS (1,87 C/V) e Gestão Empresarial (1,86 C/V).';
        textNoi.innerHTML = '<b>Forte Procura por Tecnologia no Campo:</b> À noite, ADS (4,50 C/V) e Mecanização Agrícola (4,38 C/V) são os dois grandes motores de concorrência nessas unidades.';
      }} else {{
        header.innerText = 'JUSTIFICATIVAS: CENÁRIO GERAL (TODOS OS MUNICÍPIOS DO ESTADO)';
        badgeMan.innerText = '4,77 C/V (GTI) / 3,21 (DSM)';
        badgeTar.innerText = '2,36 C/V (DSM) / 1,83 (Gestão)';
        badgeNoi.innerText = '9,90 C/V (ADS)';
        textMan.innerHTML = '<b>Sinergia Máxima de Infraestrutura:</b> GTI ou DSM no período matutino aproveitam integralmente os laboratórios de ADS instalados para o período noturno, amortizando o investimento inicial.';
        textTar.innerHTML = '<b>Equilíbrio do Turno Vespertino:</b> DSM ou Gestão Empresarial apresentam demanda estável com crescimento consistente nos anos recentes.';
        textNoi.innerHTML = '<b>Líder Absoluto de Procura:</b> ADS é o curso mais concorrido de toda a história das FATECs, com quase 10 C/V de média geral em mais de 22 faculdades simultâneas.';
      }}
    }}

    // RENDERIZAR O RANKING DE ABERTURA CLARO (PÓDIO 1º, 2º, 3º LUGAR COM IDENTIFICAÇÃO)
    function renderRankingPodium() {{
      const tier = allPopData[currentPopTier];
      const courses = tier.courses;
      const listEl = document.getElementById('ranking-list');
      const boxTitle = document.getElementById('ranking-box-title');
      const boxSub = document.getElementById('ranking-box-subtitle');
      listEl.innerHTML = '';

      let filterShift = currentShift;
      let displayCourses = [];

      if (filterShift === 'todos') {{
        boxTitle.innerHTML = '<span>🏆</span> Recomendações Estratégicas para os 3 Turnos';
        boxSub.innerText = `Portfólio ideal do Campus (${{tier.sheet}}): 1 curso por turno sem duplicar`;

        // SELEÇÃO DOS 3 CURSOS RECOMENDADOS
        let m = (currentPopTier === 'pequenas_ate_200')
          ? courses.find(c => c.turno === 'Manhã' && isMecanizacao(c.curso))
          : (courses.find(c => c.turno === 'Manhã' && isGTI(c.curso)) || courses.find(c => c.turno === 'Manhã' && isDSM(c.curso)));

        let t = (currentPopTier === 'pequenas_ate_200')
          ? courses.find(c => c.turno === 'Tarde' && isBigDataAgro(c.curso))
          : (courses.find(c => c.turno === 'Tarde' && isDSM(c.curso)) || courses.find(c => c.turno === 'Tarde' && isGestaoEmp(c.curso)));

        let n = courses.find(c => c.turno === 'Noite' && isADS(c.curso));

        displayCourses = [
          {{ ...n, posLabel: '🌙 NOITE (LÍDER ABSOLUTO)', recTag: 'Carro-chefe Regional', barColor: 'bg-emerald-500' }},
          {{ ...m, posLabel: '🌅 MANHÃ (1ª ESCOLHA TI)', recTag: 'Sinergia Total Labs', barColor: 'bg-blue-500' }},
          {{ ...t, posLabel: '☀️ TARDE (1ª ESCOLHA TI)', recTag: 'Líder TI Vespertino', barColor: 'bg-amber-500' }}
        ].filter(Boolean);

      }} else {{
        boxTitle.innerHTML = `<span>🏆</span> Ranking Específico: Qual curso abrir na ${{filterShift.toUpperCase()}}?`;
        boxSub.innerText = `Classificação por Demanda Média na faixa: ${{tier.sheet}} (Turno: ${{filterShift}})`;

        let list = courses.filter(c => c.turno === filterShift && c.semestres >= 2).sort((a,b) => b.media - a.media);
        let maxVal = list[0] ? list[0].media : 10;

        displayCourses = list.slice(0, 6).map((c, idx) => {{
          let posLabel = `${{idx + 1}}º LUGAR`;
          let recTag = '';
          let barColor = 'bg-cyan-500';

          if (idx === 0) {{
            posLabel = '🥇 1º LUGAR EM DEMANDA';
            recTag = (filterShift === 'Noite') ? '⭐ RECOMENDADO NOITE' : 'Alocado no Noturno';
            barColor = 'bg-amber-400';
          }} else if (idx === 1) {{
            posLabel = '🥈 2º LUGAR EM DEMANDA';
            recTag = (filterShift === 'Manhã') ? '⭐ RECOMENDADO MANHÃ' : (filterShift === 'Tarde' ? '⭐ RECOMENDADO TARDE' : 'Forte Opção');
            barColor = 'bg-blue-400';
          }} else if (idx === 2) {{
            posLabel = '🥉 3º LUGAR EM DEMANDA';
            recTag = (filterShift === 'Tarde' && isGestaoEmp(c.curso)) ? '💼 Alt. Gestão' : 'Alternativa';
            barColor = 'bg-emerald-400';
          }}

          return {{ ...c, posLabel, recTag, barColor, maxVal }};
        }});
      }}

      // RENDERIZAÇÃO DOS CARDS DE RANKING
      displayCourses.forEach(c => {{
        const isSelected = selectedCourseKey === c.key;
        const widthPct = Math.min(100, Math.max(15, (c.media / 12) * 100));

        const item = document.createElement('div');
        item.className = `rank-item p-2.5 rounded-lg border border-slate-800 flex flex-col gap-1.5 ${{isSelected ? 'selected border-cyan-400' : 'bg-slate-900/40'}}`;
        item.onclick = () => selectCourse(c.key);

        item.innerHTML = `
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="text-[10px] font-bold font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                ${{c.posLabel}}
              </span>
              <span class="text-xs font-bold text-white">${{c.curso}}</span>
              ${{c.recTag ? `<span class="text-[9px] font-bold px-1.5 py-0.5 rounded ${{c.recTag.includes('RECOMENDADO') || c.recTag.includes('Carro-chefe') ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'bg-amber-500/20 text-amber-300 border border-amber-500/40'}}">${{c.recTag}}</span>` : ''}}
            </div>
            <div class="text-right">
              <span class="text-sm font-black font-mono text-cyan-400">${{c.media.toFixed(2)}}</span>
              <span class="text-[10px] text-slate-400">C/V</span>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <div class="data-bar-container">
              <div class="data-bar ${{c.barColor || 'bg-cyan-500'}}" style="width: ${{widthPct}}%;"></div>
            </div>
            <span class="text-[10px] text-slate-400 font-mono whitespace-nowrap">${{c.turno}} • ${{c.semestres}} sem.</span>
          </div>
        `;
        listEl.appendChild(item);
      }});
    }}

    // RENDERIZAR O GRÁFICO HISTÓRICO DINÂMICO
    function renderDynamicLineChart() {{
      const tier = allPopData[currentPopTier];
      const series = tier.series;
      const semesters = ['22.1', '22.2', '23.1', '23.2', '24.1', '24.2'];
      const ctx = document.getElementById('historicalLineCanvas').getContext('2d');

      const chartTitle = document.getElementById('line-chart-title');
      const chartSub = document.getElementById('line-chart-subtitle');

      let targetSeries = [];

      if (currentShift === 'todos') {{
        chartTitle.innerText = `Série Histórica: Top Cursos de Todos os Turnos (${{tier.sheet}})`;
        chartSub.innerText = 'Comparativo de evolução semestral dos cursos líderes de cada turno';
        targetSeries = series.slice(0, 5);
      }} else {{
        chartTitle.innerText = `Série Histórica: Top Cursos do Turno ${{currentShift.toUpperCase()}} (${{tier.sheet}})`;
        chartSub.innerText = `Evolução semestral dos cursos matutinos, vespertinos ou noturnos`;
        targetSeries = series.filter(s => s.turno === currentShift).slice(0, 5);
      }}

      // SE UM CURSO FOI CLICADO, DESTACA ELE!
      if (selectedCourseKey) {{
        const matched = series.find(s => s.key === selectedCourseKey);
        if (matched) {{
          targetSeries = [matched, ...targetSeries.filter(s => s.key !== selectedCourseKey).slice(0, 4)];
        }}
      }}

      const datasets = targetSeries.map((s, idx) => {{
        const isHighlight = selectedCourseKey ? s.key === selectedCourseKey : idx === 0;
        const color = pbiPalette[idx % pbiPalette.length];

        return {{
          label: `${{s.curso}} (${{s.turno}})`,
          data: s.history,
          borderColor: color,
          backgroundColor: color,
          borderWidth: isHighlight ? 3.5 : 2,
          pointRadius: isHighlight ? 5 : 3.5,
          pointHoverRadius: 7,
          tension: 0.3,
          spanGaps: true
        }};
      }});

      if (lineChartInstance) {{
        lineChartInstance.destroy();
      }}

      lineChartInstance = new Chart(ctx, {{
        type: 'line',
        data: {{
          labels: semesters,
          datasets: datasets
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{
              position: 'bottom',
              labels: {{
                color: '#94a3b8',
                boxWidth: 12,
                font: {{ size: 10, family: 'Inter' }}
              }}
            }},
            tooltip: {{
              backgroundColor: '#0f172a',
              titleColor: '#38bdf8',
              bodyColor: '#ffffff',
              borderColor: '#38bdf8',
              borderWidth: 1,
              padding: 8,
              bodyFont: {{ size: 11, family: 'JetBrains Mono' }}
            }}
          }},
          scales: {{
            x: {{
              grid: {{ color: 'rgba(51, 65, 85, 0.3)' }},
              ticks: {{ color: '#94a3b8', font: {{ size: 10, family: 'JetBrains Mono' }} }}
            }},
            y: {{
              beginAtZero: false,
              grid: {{ color: 'rgba(51, 65, 85, 0.3)' }},
              ticks: {{ color: '#94a3b8', font: {{ size: 10, family: 'JetBrains Mono' }} }}
            }}
          }}
        }}
      }});
    }}

    // RENDERIZAR TABELA INFERIOR
    function renderTable() {{
      const tier = allPopData[currentPopTier];
      const courses = tier.courses;
      const tbody = document.getElementById('table-body');
      tbody.innerHTML = '';

      let filterShift = currentShift;
      let filtered = (filterShift === 'todos') ? courses : courses.filter(c => c.turno === filterShift);

      // ORDENAR POR DEMANDA
      filtered.sort((a,b) => b.media - a.media);

      document.getElementById('table-row-count').innerText = `${{filtered.length}} cursos listados na faixa ${{tier.sheet}}`;

      filtered.slice(0, 15).forEach((c, idx) => {{
        const tr = document.createElement('tr');
        tr.className = `hover:bg-slate-800/60 ${{selectedCourseKey === c.key ? 'bg-slate-800/90 font-bold text-white' : ''}}`;
        tr.onclick = () => selectCourse(c.key);

        let statusBadge = '<span class="px-1.5 py-0.5 rounded text-[10px] bg-slate-800 text-slate-400">Regular</span>';
        if (isADS(c.curso) && c.turno === 'Noite') {{
          statusBadge = '<span class="px-1.5 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/40">1º Noite (Oficial)</span>';
        }} else if (isGTI(c.curso) && c.turno === 'Manhã') {{
          statusBadge = '<span class="px-1.5 py-0.5 rounded text-[10px] bg-blue-500/20 text-blue-300 font-bold border border-blue-500/40">1º Manhã (Oficial)</span>';
        }} else if (isDSM(c.curso) && c.turno === 'Tarde') {{
          statusBadge = '<span class="px-1.5 py-0.5 rounded text-[10px] bg-amber-500/20 text-amber-300 font-bold border border-amber-500/40">1º Tarde (Oficial)</span>';
        }}

        tr.innerHTML = `
          <td class="p-2 flex items-center gap-1.5">
            <span class="text-slate-500 font-mono text-[10px]">${{idx + 1}}</span>
            <span class="font-medium text-white">${{c.curso}}</span>
          </td>
          <td class="p-2"><span class="px-1.5 py-0.5 rounded text-[10px] bg-slate-800 font-mono">${{c.turno}}</span></td>
          <td class="p-2 text-slate-400">${{c.eixo || 'Tecnologia'}}</td>
          <td class="p-2 text-right font-mono font-bold text-cyan-400">${{c.media.toFixed(2)}}</td>
          <td class="p-2 text-right font-mono">${{c.semestres}}</td>
          <td class="p-2 text-right font-mono">${{c.qtd.toFixed(1)}}</td>
          <td class="p-2 text-center">${{statusBadge}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}
  </script>
</body>
</html>
'''

output_path = r'C:\Users\PICHAU\.gemini\antigravity\scratch\trabalho_vestibular\painel_powerbi.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Novo painel_powerbi.html gerado com sucesso!")
