import webview
import time
import json
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.ids import ids
from algorithms.ucs import ucs
from algorithms.astar import astar
from algorithms.greedy import greedy
from algorithms.ida_star import ida_star
from algorithms.simple_hill_climbing import hill_climbing_solve as simple_hc_solve
from algorithms.steepest_hill_climbing import hill_climbing_solve as steepest_hc_solve
from algorithms.stochastic_hill_climbing import stochastic_hill_climbing_solve
from algorithms.simulated_annealing import simulated_annealing_solve
from algorithms.random_restart_hc import random_restart_hill_climbing_solve
from algorithms.local_beam_search import local_beam_search_solve
from algorithms.complex_environmental_search import (
    and_or_graph_search_solve,
    sensorless_search_solve,
    partial_observable_search_solve,
    get_one_alternate_state
)
from algorithms.csp_search import (
    ac3_search,
    backtracking_search,
    forward_tracking_search,
    min_conflicts_search
)
from algorithms.adversarial_search import adversarial_solve

html_content = """<!DOCTYPE html><html class="light" lang="en" style="width: 100%; height: 100%; overflow: hidden;"><head>
<meta charset="utf-8">
<meta content="width=device-width, initial-scale=1.0" name="viewport">
<title>8-Puzzle Solver Simulator</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            "colors": {
                    "secondary-fixed": "#d3e4fe",
                    "on-secondary-fixed": "#0b1c30",
                    "surface-container-highest": "#dce2f7",
                    "surface-variant": "#dce2f7",
                    "on-tertiary": "#ffffff",
                    "background": "#f5f6f8",
                    "tertiary-fixed-dim": "#ffb596",
                    "on-background": "#141b2b",
                    "tertiary-fixed": "#ffdbcd",
                    "inverse-primary": "#b4c5ff",
                    "primary": "#004ac6",
                    "surface-bright": "#f9f9ff",
                    "primary-container": "#2563eb",
                    "surface": "#f9f9ff",
                    "surface-container": "#e9edff",
                    "secondary": "#505f76",
                    "on-primary-fixed": "#00174b",
                    "primary-fixed": "#dbe1ff",
                    "on-tertiary-container": "#ffede6",
                    "inverse-on-surface": "#edf0ff",
                    "surface-dim": "#d3daef",
                    "error-container": "#ffdad6",
                    "outline": "#737686",
                    "on-secondary": "#ffffff",
                    "on-error-container": "#93000a",
                    "on-tertiary-fixed-variant": "#7d2d00",
                    "on-primary-fixed-variant": "#003ea8",
                    "surface-container-high": "#e1e8fd",
                    "on-secondary-fixed-variant": "#38485d",
                    "error": "#ba1a1a",
                    "on-tertiary-fixed": "#360f00",
                    "on-surface-variant": "#434655",
                    "secondary-fixed-dim": "#b7c8e1",
                    "tertiary": "#943700",
                    "secondary-container": "#d0e1fb",
                    "on-surface": "#141b2b",
                    "primary-fixed-dim": "#b4c5ff",
                    "surface-container-low": "#f1f3ff",
                    "surface-container-lowest": "#ffffff",
                    "on-secondary-container": "#54647a",
                    "on-primary-container": "#eeefff",
                    "on-primary": "#ffffff",
                    "tertiary-container": "#bc4800",
                    "surface-tint": "#0053db",
                    "on-error": "#ffffff",
                    "outline-variant": "#c3c6d7",
                    "inverse-surface": "#293040"
            },
            "borderRadius": {
                    "DEFAULT": "0.25rem",
                    "lg": "0.5rem",
                    "xl": "0.75rem",
                    "full": "9999px"
            },
            "fontFamily": {
                    "headline-md": ["Inter"],
                    "label-sm": ["Inter"],
                    "headline-lg": ["Inter"],
                    "body-lg": ["Inter"],
                    "body-md": ["Inter"],
                    "label-md": ["Inter"],
                    "headline-sm": ["Inter"],
                    "mono": ["JetBrains Mono"]
            },
            "fontSize": {
                    "headline-md": ["16px", {"lineHeight": "22px", "fontWeight": "600"}],
                    "label-sm": ["10px", {"lineHeight": "13px", "fontWeight": "600"}],
                    "headline-lg": ["21px", {"lineHeight": "26px", "letterSpacing": "-0.01em", "fontWeight": "700"}],
                    "body-lg": ["14px", {"lineHeight": "20px", "fontWeight": "400"}],
                    "body-md": ["12px", {"lineHeight": "17px", "fontWeight": "400"}],
                    "label-md": ["12px", {"lineHeight": "15px", "fontWeight": "600"}],
                    "headline-sm": ["15px", {"lineHeight": "21px", "fontWeight": "600"}]
            }
          },
        },
      }
    </script>
<style>
        body { font-family: 'Inter', sans-serif; background-color: #f5f6f8; margin: 0; }
        .material-symbols-outlined { font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 18; }
        .custom-scrollbar::-webkit-scrollbar { width: 5px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(0, 74, 198, 0.15); border-radius: 10px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(0, 74, 198, 0.3); }
        input[type="number"]::-webkit-inner-spin-button, input[type="number"]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
        input[type="number"] { -moz-appearance: textfield; }

        .cell-wrapper { position: relative; }
        .cell-wrapper input { width: 100%; }
        .spinner-btns {
            position: absolute; right: 5px; top: 50%; transform: translateY(-50%);
            display: flex; flex-direction: column; gap: 1px; opacity: 0;
            transition: opacity 0.2s ease; pointer-events: none;
        }
        .cell-wrapper:hover .spinner-btns { opacity: 1; pointer-events: auto; }
        .spinner-btns button {
            width: 18px; height: 14px; display: flex; align-items: center; justify-content: center;
            background: rgba(255, 255, 255, 0.95); border: 1px solid #c3c6d7; border-radius: 4px;
            cursor: pointer; color: #434655; font-size: 8px; line-height: 1; padding: 0; transition: background 0.15s;
        }
        .spinner-btns button:hover { background: #d3daef; }

        /* Algorithm dropdown */
        .algo-dropdown { position: relative; }
        .algo-dropdown-btn {
            display: flex; align-items: center; gap: 6px; padding: 5px 14px;
            background: white; border: 1.5px solid #004ac6; border-radius: 8px;
            cursor: pointer; font-weight: 700; font-size: 13px; color: #004ac6;
            transition: all 0.2s; font-family: 'Inter', sans-serif;
        }
        .algo-dropdown-btn:hover { background: #e1e8fd; }
        .algo-dropdown-btn .arrow { font-size: 10px; transition: transform 0.2s; }
        .algo-dropdown-btn.open .arrow { transform: rotate(180deg); }
        .algo-dropdown-menu {
            display: none; position: absolute; top: calc(100% + 6px); right: 0;
            background: white; border: 1px solid #c3c6d7; border-radius: 10px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.12); z-index: 999; min-width: 220px;
            padding: 6px 0; max-height: 340px; overflow-y: auto;
        }
        .algo-dropdown-menu.show { display: block; animation: dropIn 0.15s ease-out; }
        @keyframes dropIn { from { opacity: 0; transform: translateY(-6px); } to { opacity: 1; transform: translateY(0); } }
        .algo-group-label {
            padding: 8px 14px 4px; font-size: 10px; font-weight: 700;
            text-transform: uppercase; letter-spacing: 0.08em; color: #737686;
        }
        .algo-item {
            padding: 7px 14px; font-size: 13px; font-weight: 500; color: #141b2b;
            cursor: pointer; transition: background 0.12s; display: flex; align-items: center; gap: 8px;
        }
        .algo-item:hover { background: #e9edff; }
        .algo-item.active { background: #dbe1ff; color: #004ac6; font-weight: 700; }
        .algo-item .check { font-size: 14px; color: #004ac6; visibility: hidden; }
        .algo-item.active .check { visibility: visible; }
    </style>
</head>
<body class="bg-background text-on-surface text-sm flex flex-col h-screen w-screen overflow-hidden">

<header class="flex justify-between items-center px-6 h-12 w-full bg-surface-container-lowest border-b border-outline-variant shrink-0 z-50">
    <div class="flex items-center gap-3">
        <span class="font-headline-sm text-[17px] font-bold text-on-surface">8-Puzzle Solver Simulator</span>
    </div>
    <nav class="hidden md:flex items-center gap-4">
        <div class="algo-dropdown">
            <button class="algo-dropdown-btn" id="algo-toggle" onclick="toggleDropdown()">
                <span id="algo-label">BFS (Uninformed)</span>
                <span class="arrow">&#9660;</span>
            </button>
            <div class="algo-dropdown-menu custom-scrollbar" id="algo-menu">
                <div class="algo-group-label">Uninformed Search</div>
                <div class="algo-item active" data-algo="bfs" data-category="Uninformed" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Breadth-First Search (BFS)
                </div>
                <div class="algo-item" data-algo="dfs" data-category="Uninformed" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Depth-First Search (DFS)
                </div>
                <div class="algo-item" data-algo="ids" data-category="Uninformed" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Iterative Deepening (IDS)
                </div>
                <div class="algo-item" data-algo="ucs" data-category="Uninformed" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Uniform Cost Search (UCS)
                </div>
                <div class="algo-group-label" style="border-top:1px solid #e1e8fd; margin-top:4px; padding-top:10px;">Informed Search</div>
                <div class="algo-item" data-algo="astar" data-category="Informed" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    A* Search
                </div>
                <div class="algo-item" data-algo="greedy" data-category="Informed" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Greedy Best-First
                </div>
                <div class="algo-item" data-algo="ida_star" data-category="Informed" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    IDA* Search
                </div>
                <div class="algo-group-label" style="border-top:1px solid #e1e8fd; margin-top:4px; padding-top:10px;">Local Search</div>
                <div class="algo-item" data-algo="simple_hc" data-category="Local Search" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Simple Hill Climbing
                </div>
                <div class="algo-item" data-algo="steepest_hc" data-category="Local Search" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Steepest-Ascent HC
                </div>
                <div class="algo-item" data-algo="stochastic_hc" data-category="Local Search" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Stochastic Hill Climbing
                </div>
                <div class="algo-item" data-algo="simulated_annealing" data-category="Local Search" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Simulated Annealing
                </div>
                <div class="algo-item" data-algo="random_restart_hc" data-category="Local Search" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Random Restart HC
                </div>
                <div class="algo-item" data-algo="local_beam" data-category="Local Search" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Local Beam Search
                </div>
                <div class="algo-group-label" style="border-top:1px solid #e1e8fd; margin-top:4px; padding-top:10px;">Complex Environments</div>
                <div class="algo-item" data-algo="and_or" data-category="Complex Environments" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    AND-OR Graph Search
                </div>
                <div class="algo-item" data-algo="sensorless" data-category="Complex Environments" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Belief State
                </div>
                <div class="algo-item" data-algo="partial_observable" data-category="Complex Environments" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Belief State & Goal
                </div>
                <div class="algo-group-label" style="border-top:1px solid #e1e8fd; margin-top:4px; padding-top:10px;">CSP</div>
                <div class="algo-item" data-algo="ac3" data-category="CSP" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    AC-3
                </div>
                <div class="algo-item" data-algo="backtracking" data-category="CSP" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Backtracking
                </div>
                <div class="algo-item" data-algo="forward_tracking" data-category="CSP" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Forward Tracking
                </div>
                <div class="algo-item" data-algo="min_conflicts" data-category="CSP" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Min-Conflicts
                </div>
                <div class="algo-group-label" style="border-top:1px solid #e1e8fd; margin-top:4px; padding-top:10px;">Đối Kháng (Caro)</div>
                <div class="algo-item" data-algo="minimax" data-category="Đối Kháng" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Minimax
                </div>
                <div class="algo-item" data-algo="alpha_beta" data-category="Đối Kháng" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Alpha-Beta
                </div>
                <div class="algo-item" data-algo="expectimax" data-category="Đối Kháng" onclick="selectAlgo(this)">
                    <span class="material-symbols-outlined check">check</span>
                    Expectimax
                </div>
            </div>
        </div>
    </nav>
</header>

<main class="flex-1 w-full p-4 overflow-hidden flex items-center justify-center">
<div class="grid grid-cols-1 lg:grid-cols-12 gap-4 w-full max-w-[1180px] mx-auto items-start">
    
    <div id="left-parent" class="lg:col-span-7 flex flex-col gap-4">
        <div id="grids-container" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <section class="bg-surface-container-lowest border border-outline-variant rounded-xl p-4 shadow-sm">
                <div class="flex items-center justify-between mb-2.5 border-b border-outline-variant pb-2">
                    <h3 id="initial-state-title" class="font-headline-sm text-headline-sm text-on-surface">1. Initial State</h3>
                    <span class="material-symbols-outlined text-outline text-[16px]">tune</span>
                </div>
                <div class="grid grid-cols-3 gap-2 mb-3.5" id="initial-grid"></div>
                <div class="flex gap-2">
                    <button id="btn-random" class="flex-1 py-1.5 bg-[#e1e8fd] text-primary border border-primary/20 rounded-lg font-semibold text-label-md hover:bg-[#d3daef] transition-colors">Random</button>
                    <button id="btn-reset" class="flex-1 py-1.5 bg-[#e1e8fd] text-primary border border-primary/20 rounded-lg font-semibold text-label-md hover:bg-[#d3daef] transition-colors">Reset</button>
                    <button id="btn-load" class="flex-1 py-1.5 bg-[#e1e8fd] text-primary border border-primary/20 rounded-lg font-semibold text-label-md hover:bg-[#d3daef] transition-colors">Load Example</button>
                </div>
            </section>
            
            <section id="goal-section" class="bg-surface-container-lowest border border-outline-variant rounded-xl p-4 shadow-sm">
                <div class="flex items-center justify-between mb-2.5 border-b border-outline-variant pb-2">
                    <h3 class="font-headline-sm text-headline-sm text-on-surface">Goal State</h3>
                    <span class="material-symbols-outlined text-primary text-[16px]">check_circle</span>
                </div>
                <div class="grid grid-cols-3 gap-2 mb-3.5" id="goal-grid"></div>
            </section>
        </div>
        
        <section id="visual-section" class="bg-surface-container-lowest border border-outline-variant rounded-xl p-4 shadow-sm flex flex-col items-center">
            <div class="flex items-center justify-between border-b border-outline-variant pb-2 mb-2 w-full">
                <h3 class="font-headline-sm text-headline-sm text-on-surface">3. Visual Simulation</h3>
                <div id="step-wrapper">
                    <span id="step-label" class="px-2.5 py-0.5 bg-surface-container-high text-on-surface-variant rounded font-semibold text-label-md">Ready</span>
                </div>
            </div>
            <div class="w-full flex items-center justify-center py-1">
                <div id="anim-board" class="w-full max-w-[210px] aspect-square bg-surface-container-low rounded-xl p-2 grid grid-cols-3 gap-2 relative overflow-hidden"></div>
            </div>
        </section>
    </div>
    
    <div class="lg:col-span-5 flex flex-col gap-4">
        <div class="grid grid-cols-2 gap-2">
            <div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-3 shadow-sm">
                <span class="font-label-sm text-label-sm text-outline uppercase block mb-0.5">Steps</span>
                <div id="stat-steps" class="font-headline-md text-headline-md text-on-surface">-</div>
            </div>
            <div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-3 shadow-sm">
                <span class="font-label-sm text-label-sm text-outline uppercase block mb-0.5">Nodes</span>
                <div id="stat-nodes" class="font-headline-md text-headline-md text-on-surface">-</div>
            </div>
            <div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-3 shadow-sm">
                <span class="font-label-sm text-label-sm text-outline uppercase block mb-0.5">Time</span>
                <div id="stat-time" class="font-headline-md text-headline-md text-on-surface">-</div>
            </div>
            <div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-3 shadow-sm">
                <span class="font-label-sm text-label-sm text-outline uppercase block mb-0.5">Max Depth</span>
                <div id="stat-depth" class="font-headline-md text-headline-md text-on-surface">-</div>
            </div>
        </div>
        
        <section class="bg-surface-container-lowest border border-outline-variant rounded-xl px-4 py-5 shadow-sm min-h-[135px] flex flex-col justify-center">
            <div class="flex items-center justify-between mb-2 border-b border-outline-variant pb-1.5 w-full">
                <h3 id="config-title" class="font-headline-sm text-headline-sm text-on-surface">2. BFS Configuration</h3>
            </div>
            <div id="config-body" class="w-full flex-1 flex flex-col justify-center"></div>
        </section>
        
        <section class="bg-surface-container-high border border-outline-variant rounded-xl flex flex-col shadow-sm h-[250px]">
            <div class="flex items-center justify-between px-3 py-1.5 bg-surface-container-highest border-b border-outline-variant rounded-t-xl">
                <div class="flex items-center gap-2">
                    <span class="material-symbols-outlined text-primary text-[15px]">terminal</span>
                    <span class="font-label-md text-[12px] font-bold text-on-surface uppercase tracking-wider">Execution Log</span>
                </div>
            </div>
            <div id="execution-log" class="flex-1 p-3 font-mono text-[11px] leading-relaxed overflow-y-auto custom-scrollbar text-[#0f172a]">
                <span class="text-outline">Waiting for execution...</span>
            </div>
        </section>
    </div>
</div>
</main>

<script>
let animationTimeout;
const defaultValues = [1,8,3,2,6,4,7,0,5];
const adversarialAlgos = ['minimax', 'alpha_beta', 'expectimax'];
let caroBoard = [0,0,0,0,0,0,0,0,0];
let caroGameOver = false;
let caroTurn = 'player';

function buildInitialGrid(values1, values2 = null) {
    const grid = document.getElementById('initial-grid');
    grid.innerHTML = '';
    
    const titleEl = document.getElementById('initial-state-title');
    const goalSection = document.getElementById('goal-section');
    const gridsContainer = document.getElementById('grids-container');
    const leftParent = document.getElementById('left-parent');
    const visualSection = document.getElementById('visual-section');
    
    if (adversarialAlgos.includes(currentAlgo)) {
        if (titleEl) titleEl.textContent = "1. Bàn cờ Caro (3x3)";
        if (goalSection) goalSection.style.display = 'none';
        if (gridsContainer && visualSection && visualSection.parentNode !== gridsContainer) {
            gridsContainer.appendChild(visualSection);
        }
        
        grid.className = "grid grid-cols-3 gap-2 mb-3.5";
        for (let i = 0; i < 9; i++) {
            const cell = document.createElement('div');
            cell.className = 'aspect-square flex items-center justify-center rounded-xl font-bold text-[28px] border border-outline-variant shadow-sm transition-all duration-200 select-none ';
            
            const val = caroBoard[i];
            if (val === 0) {
                cell.className += 'bg-surface-container-high hover:bg-surface-container-highest cursor-pointer text-transparent';
                cell.textContent = '.';
                cell.addEventListener('click', () => makeCaroPlayerMove(i));
            } else if (val === 1) {
                cell.className += 'bg-blue-50 text-blue-600 border-blue-200';
                cell.textContent = 'X';
            } else if (val === 2) {
                cell.className += 'bg-red-50 text-red-600 border-red-200';
                cell.textContent = 'O';
            }
            grid.appendChild(cell);
        }
        return;
    }
    
    if (titleEl) titleEl.textContent = "1. Initial State";
    if (goalSection) goalSection.style.display = 'block';
    if (leftParent && visualSection && visualSection.parentNode !== leftParent) {
        leftParent.appendChild(visualSection);
    }
    
    const isDual = currentAlgo === 'sensorless' || currentAlgo === 'partial_observable';
    
    if (isDual) {
        grid.className = "flex gap-4 w-full justify-between mb-3.5";
        
        // Render Ma Trận 1
        const wrapper1 = document.createElement('div');
        wrapper1.className = 'flex-1';
        wrapper1.innerHTML = '<div class="text-[11px] font-bold text-secondary mb-1">Ma Trận 1</div>';
        const subGrid1 = document.createElement('div');
        subGrid1.className = 'grid grid-cols-3 gap-1.5';
        for(let i = 0; i < 9; i++) {
            subGrid1.appendChild(createCellElement(i, values1[i]));
        }
        wrapper1.appendChild(subGrid1);
        grid.appendChild(wrapper1);
        
        // Render Ma Trận 2
        const wrapper2 = document.createElement('div');
        wrapper2.className = 'flex-1';
        wrapper2.innerHTML = '<div class="text-[11px] font-bold text-secondary mb-1">Ma Trận 2</div>';
        const subGrid2 = document.createElement('div');
        subGrid2.className = 'grid grid-cols-3 gap-1.5';
        const v2 = values2 || [2,8,3,1,0,4,7,6,5];
        for(let i = 0; i < 9; i++) {
            subGrid2.appendChild(createCellElement(i + 9, v2[i]));
        }
        wrapper2.appendChild(subGrid2);
        grid.appendChild(wrapper2);
    } else {
        grid.className = "grid grid-cols-3 gap-2 mb-3.5";
        for(let i = 0; i < 9; i++) {
            grid.appendChild(createCellElement(i, values1[i]));
        }
    }
}

function createCellElement(i, val) {
    const wrapper = document.createElement('div');
    wrapper.className = 'cell-wrapper';
    
    const input = document.createElement('input');
    input.type = 'number';
    input.id = `cell-${i}`;
    input.className = 'h-11 w-full text-center bg-surface-container-high rounded-lg font-headline-sm text-[16px] font-bold text-primary border border-primary/20 focus:outline-none focus:ring-2 focus:ring-primary';
    input.value = val;
    input.min = 0;
    input.max = 8;
    input.dataset.prev = val;
    
    input.addEventListener('change', function() { handleCellChange(i); });
    
    const spinBtns = document.createElement('div');
    spinBtns.className = 'spinner-btns';
    
    const btnUp = document.createElement('button');
    btnUp.innerHTML = '&#9650;';
    btnUp.addEventListener('click', (e) => { e.preventDefault(); spinCell(i, 1); });
    
    const btnDown = document.createElement('button');
    btnDown.innerHTML = '&#9660;';
    btnDown.addEventListener('click', (e) => { e.preventDefault(); spinCell(i, -1); });
    
    spinBtns.appendChild(btnUp);
    spinBtns.appendChild(btnDown);
    wrapper.appendChild(input);
    wrapper.appendChild(spinBtns);
    return wrapper;
}

function getCellValue(idx) { return parseInt(document.getElementById(`cell-${idx}`).value) || 0; }
function setCellValue(idx, val) {
    const el = document.getElementById(`cell-${idx}`);
    el.value = val; el.dataset.prev = val;
}

function handleCellChange(changedIdx) {
    const el = document.getElementById(`cell-${changedIdx}`);
    let newVal = parseInt(el.value);
    const oldVal = parseInt(el.dataset.prev);
    if(isNaN(newVal) || newVal < 0) newVal = 0;
    if(newVal > 8) newVal = 8;
    el.value = newVal;
    if(newVal === oldVal) { el.dataset.prev = newVal; return; }
    
    const startIdx = changedIdx < 9 ? 0 : 9;
    const endIdx = changedIdx < 9 ? 9 : 18;
    
    for(let i = startIdx; i < endIdx; i++) {
        if(i === changedIdx) continue;
        if(getCellValue(i) === newVal) { setCellValue(i, oldVal); break; }
    }
    el.dataset.prev = newVal;
    updateBoardPreview();
}

function spinCell(idx, delta) {
    const oldVal = getCellValue(idx);
    let newVal = oldVal + delta;
    if(newVal < 0) newVal = 8;
    if(newVal > 8) newVal = 0;
    
    const startIdx = idx < 9 ? 0 : 9;
    const endIdx = idx < 9 ? 9 : 18;
    
    for(let i = startIdx; i < endIdx; i++) {
        if(i === idx) continue;
        if(getCellValue(i) === newVal) { setCellValue(i, oldVal); break; }
    }
    setCellValue(idx, newVal);
    updateBoardPreview();
}

function updateBoardPreview() {
    if (adversarialAlgos.includes(currentAlgo)) {
        renderBoard(caroBoard);
    } else if (currentAlgo === 'sensorless' || currentAlgo === 'partial_observable') {
        const state1 = [];
        const state2 = [];
        for(let i = 0; i < 9; i++) state1.push(getCellValue(i));
        for(let i = 9; i < 18; i++) state2.push(getCellValue(i));
        renderBoard([state1, state2]);
    } else {
        const state = [];
        for(let i = 0; i < 9; i++) state.push(getCellValue(i));
        renderBoard(state);
    }
}

function renderBoard(state) {
    const board = document.getElementById('anim-board');
    if (adversarialAlgos.includes(currentAlgo)) {
        board.className = "w-full max-w-[210px] aspect-square bg-surface-container-low rounded-xl p-2 grid grid-cols-3 gap-2 relative overflow-hidden";
        board.innerHTML = '';
        state.forEach(val => {
            if(val === 0) {
                board.innerHTML += `<div class="aspect-square bg-surface-container-highest/20 rounded-lg border-2 border-dashed border-outline-variant"></div>`;
            } else if (val === 1) {
                board.innerHTML += `<div class="aspect-square bg-blue-50 text-blue-600 border border-blue-200 rounded-lg flex items-center justify-center font-bold text-[24px]">X</div>`;
            } else if (val === 2) {
                board.innerHTML += `<div class="aspect-square bg-red-50 text-red-600 border border-red-200 rounded-lg flex items-center justify-center font-bold text-[24px]">O</div>`;
            }
        });
    } else if (Array.isArray(state) && state.length === 2 && Array.isArray(state[0])) {
        // Dual state rendering (conformant or PO search)
        board.className = "w-full max-w-[320px] aspect-auto bg-surface-container-low rounded-xl p-2 flex gap-4 justify-center relative overflow-hidden";
        board.innerHTML = '';
        state.forEach((s, boardIdx) => {
            let label = boardIdx === 0 ? "Mô hình 1" : "Mô hình 2";
            if (currentAlgo === 'partial_observable') {
                label = boardIdx === 0 ? "Thực tế" : "Niềm tin";
            }
            let boardHtml = `<div class="flex flex-col items-center gap-1">
                <span class="text-[9px] font-bold text-secondary uppercase">${label}</span>
                <div class="grid grid-cols-3 gap-1 w-[120px] aspect-square bg-white/60 p-1.5 rounded-lg border border-outline-variant">`;
            s.forEach(val => {
                if(val === 0) {
                    boardHtml += `<div class="aspect-square bg-surface-container-highest/20 rounded border border-dashed border-outline-variant"></div>`;
                } else {
                    boardHtml += `<div class="aspect-square bg-white shadow-sm border border-outline-variant rounded flex items-center justify-center font-bold text-[13px] text-primary">${val}</div>`;
                }
            });
            boardHtml += `</div></div>`;
            board.innerHTML += boardHtml;
        });
    } else {
        board.className = "w-full max-w-[210px] aspect-square bg-surface-container-low rounded-xl p-2 grid grid-cols-3 gap-2 relative overflow-hidden";
        board.innerHTML = '';
        state.forEach(val => {
            if(val === 0) {
                board.innerHTML += `<div class="aspect-square bg-surface-container-highest/20 rounded-lg border-2 border-dashed border-outline-variant"></div>`;
            } else {
                board.innerHTML += `<div class="aspect-square bg-white shadow-sm border border-outline-variant rounded-lg flex items-center justify-center font-headline-lg text-headline-lg text-primary">${val}</div>`;
            }
        });
    }
}

function getGoalForAlgo(algo) {
    if (localSearchAlgos.includes(algo) || complexEnvAlgos.includes(algo)) {
        return [1, 2, 3, 8, 0, 4, 7, 6, 5];
    }
    return [1, 2, 3, 4, 5, 6, 7, 8, 0];
}

function renderGoalGrid(goalState) {
    const grid = document.getElementById('goal-grid');
    if (!grid) return;
    grid.innerHTML = '';
    
    if (currentAlgo === 'partial_observable') {
        grid.className = "flex gap-4 w-full justify-between mb-3.5";
        
        const goal1 = [1, 2, 3, 8, 0, 4, 7, 6, 5];
        const goal2 = [1, 2, 3, 4, 5, 6, 7, 8, 0];
        
        // Render Đích 1
        const wrapper1 = document.createElement('div');
        wrapper1.className = 'flex-1';
        wrapper1.innerHTML = '<div class="text-[11px] font-bold text-secondary mb-1">Đích 1</div>';
        const subGrid1 = document.createElement('div');
        subGrid1.className = 'grid grid-cols-3 gap-1.5';
        goal1.forEach(val => {
            const cell = document.createElement('div');
            if (val === 0) {
                cell.className = "h-8 flex items-center justify-center bg-surface-container-lowest rounded-lg text-outline-variant border border-dashed border-outline-variant";
            } else {
                cell.className = "h-8 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-[13px] font-bold text-on-surface border border-outline-variant/20";
                cell.innerText = val;
            }
            subGrid1.appendChild(cell);
        });
        wrapper1.appendChild(subGrid1);
        grid.appendChild(wrapper1);
        
        // Render Đích 2
        const wrapper2 = document.createElement('div');
        wrapper2.className = 'flex-1';
        wrapper2.innerHTML = '<div class="text-[11px] font-bold text-secondary mb-1">Đích 2</div>';
        const subGrid2 = document.createElement('div');
        subGrid2.className = 'grid grid-cols-3 gap-1.5';
        goal2.forEach(val => {
            const cell = document.createElement('div');
            if (val === 0) {
                cell.className = "h-8 flex items-center justify-center bg-surface-container-lowest rounded-lg text-outline-variant border border-dashed border-outline-variant";
            } else {
                cell.className = "h-8 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-[13px] font-bold text-on-surface border border-outline-variant/20";
                cell.innerText = val;
            }
            subGrid2.appendChild(cell);
        });
        wrapper2.appendChild(subGrid2);
        grid.appendChild(wrapper2);
    } else {
        grid.className = "grid grid-cols-3 gap-2 mb-3.5";
        goalState.forEach(val => {
            if(val === 0) {
                grid.innerHTML += `<div class="h-12 flex items-center justify-center bg-surface-container-lowest rounded-lg text-outline-variant border border-dashed border-outline-variant"></div>`;
            } else {
                grid.innerHTML += `<div class="h-12 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-[17px] font-bold text-on-surface border border-outline-variant/20">${val}</div>`;
            }
        });
    }
}

function getSolvableNeighborJS(state) {
    const pos = state.indexOf(0);
    const r = Math.floor(pos / 3), c = pos % 3;
    const neighbors = [];
    const swap = (s, i, j) => {
        let n = [...s];
        [n[i], n[j]] = [n[j], n[i]];
        return n;
    };
    if (c > 0) neighbors.push(swap(state, pos, pos - 1));
    if (c < 2) neighbors.push(swap(state, pos, pos + 1));
    if (r > 0) neighbors.push(swap(state, pos, pos - 3));
    if (r < 2) neighbors.push(swap(state, pos, pos + 3));
    return neighbors[Math.floor(Math.random() * neighbors.length)];
}

function randomBoard() {
    if (adversarialAlgos.includes(currentAlgo)) {
        caroBoard = [0,0,0,0,0,0,0,0,0];
        caroGameOver = false;
        caroTurn = 'player';
        document.getElementById('execution-log').innerHTML = '<span class="text-outline">Waiting for execution...</span>';
        
        // Randomly assign one X (1) and one O (2)
        const emptyIndices = [0, 1, 2, 3, 4, 5, 6, 7, 8];
        const idxX = emptyIndices.splice(Math.floor(Math.random() * emptyIndices.length), 1)[0];
        const idxO = emptyIndices.splice(Math.floor(Math.random() * emptyIndices.length), 1)[0];
        caroBoard[idxX] = 1;
        caroBoard[idxO] = 2;
        
        buildInitialGrid();
        updateBoardPreview();
        return;
    }
    const isDual = currentAlgo === 'sensorless' || currentAlgo === 'partial_observable';
    let nums1 = (localSearchAlgos.includes(currentAlgo) || complexEnvAlgos.includes(currentAlgo)) ? [1, 2, 3, 8, 0, 4, 7, 6, 5] : [1, 2, 3, 4, 5, 6, 7, 8, 0];
    for(let i=nums1.length-1; i>0; i--){
        const j = Math.floor(Math.random()*(i+1));
        [nums1[i], nums1[j]] = [nums1[j], nums1[i]];
    }
    
    if (isDual) {
        let nums2 = getSolvableNeighborJS(nums1);
        buildInitialGrid(nums1, nums2);
        renderBoard([nums1, nums2]);
    } else {
        buildInitialGrid(nums1);
        renderBoard(nums1);
    }
}

function resetBoard() {
    if (adversarialAlgos.includes(currentAlgo)) {
        caroBoard = [0,0,0,0,0,0,0,0,0];
        caroGameOver = false;
        caroTurn = 'player';
        document.getElementById('execution-log').innerHTML = '<span class="text-outline">Waiting for execution...</span>';
        document.getElementById('stat-steps').innerText = "-";
        document.getElementById('stat-nodes').innerText = "-";
        document.getElementById('stat-time').innerText = "-";
        document.getElementById('stat-depth').innerText = "-";
        buildInitialGrid();
        updateBoardPreview();
        return;
    }
    const isDual = currentAlgo === 'sensorless' || currentAlgo === 'partial_observable';
    const nums1 = (localSearchAlgos.includes(currentAlgo) || complexEnvAlgos.includes(currentAlgo)) ? [1, 2, 3, 8, 0, 4, 7, 6, 5] : [1, 2, 3, 4, 5, 6, 7, 8, 0];
    if (isDual) {
        const nums2 = [1, 2, 3, 8, 4, 0, 7, 6, 5];
        buildInitialGrid(nums1, nums2);
        renderBoard([nums1, nums2]);
    } else {
        buildInitialGrid(nums1);
        renderBoard(nums1);
    }
}

function loadExample() {
    if (adversarialAlgos.includes(currentAlgo)) {
        caroBoard = [1, 1, 0, 2, 0, 0, 0, 0, 0];
        caroGameOver = false;
        caroTurn = 'player';
        document.getElementById('execution-log').innerHTML = '<span class="text-outline">Cờ thế đã tải! Nhấp vào ô hàng 1 cột 3 (ô chỉ số 2) để chặn AI hoặc đi tiếp.</span>';
        document.getElementById('stat-steps').innerText = "-";
        document.getElementById('stat-nodes').innerText = "-";
        document.getElementById('stat-time').innerText = "-";
        document.getElementById('stat-depth').innerText = "-";
        buildInitialGrid();
        updateBoardPreview();
        return;
    }
    const isDual = currentAlgo === 'sensorless' || currentAlgo === 'partial_observable';
    const nums1 = (localSearchAlgos.includes(currentAlgo) || complexEnvAlgos.includes(currentAlgo)) ? [2, 8, 3, 1, 6, 4, 7, 0, 5] : [1, 8, 3, 2, 6, 4, 7, 0, 5];
    if (isDual) {
        const nums2 = [2, 8, 3, 1, 0, 4, 7, 6, 5];
        buildInitialGrid(nums1, nums2);
        renderBoard([nums1, nums2]);
    } else {
        buildInitialGrid(nums1);
        renderBoard(nums1);
    }
}

function formatLogState(title, state, action=null) {
    let stateStr = "";
    for(let i=0; i<9; i+=3) {
        let row = state.slice(i, i+3).map(x => (x===0 || x==='0') ? "[ ]" : ("  "+x+"  ")).join("");
        stateStr += " " + row + "\\n";
    }
    let titleHtml;
    if (action) {
        if (action.includes("Gán") || action.includes("gan") || action.includes("Assign")) {
            titleHtml = `<p class="mb-1 font-semibold" style="font-size:12px;">Bước ${title}: <span class="text-primary">${action}</span></p>`;
        } else {
            titleHtml = `<p class="mb-1 font-semibold" style="font-size:12px;">Bước ${title}: Di chuyển ô trống sang <span class="text-primary">${action}</span></p>`;
        }
    } else {
        titleHtml = `<p class="mb-1 font-semibold" style="font-size:12px;">${title}</p>`;
    }
                           
    return `
    <div class="mb-2">
        ${titleHtml}
        <div class="bg-surface-container-low p-1.5 rounded border border-outline-variant/30 inline-block">
            <pre class="leading-tight text-[11px] font-bold text-on-surface">${stateStr}</pre>
        </div>
    </div>
    <div class="border-t border-outline-variant/20 pt-1 opacity-50 mt-1 mb-1"></div>
    `;
}

async function animatePath(start_state, path, start_dual=null) {
    clearTimeout(animationTimeout);
    if (start_dual) {
        renderBoard(start_dual);
    } else {
        renderBoard(start_state);
    }
    
    document.getElementById('step-wrapper').innerHTML = `<span id="step-label" class="px-2.5 py-0.5 bg-surface-container-high text-on-surface-variant rounded font-semibold text-label-md">Step 0/${path.length}</span>`;
    
    await new Promise(r => { animationTimeout = setTimeout(r, 800); });
    for(let i=0; i<path.length; i++) {
        renderBoard(path[i][1]);
        document.getElementById('step-label').textContent = `Step ${i+1}/${path.length}`;
        await new Promise(r => { animationTimeout = setTimeout(r, 500); });
    }
    document.getElementById('step-wrapper').innerHTML = `<span style="background:#0d9488; color:white; padding:3px 10px; border-radius:6px; font-size:11px; font-weight:600; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">Finished</span>`;
}

let currentAlgo = 'bfs';
let currentCategory = 'Uninformed';

const algoNames = {
    bfs: 'BFS', dfs: 'DFS', ids: 'IDS', ucs: 'UCS',
    astar: 'A*', greedy: 'Greedy Best-First', ida_star: 'IDA*',
    simple_hc: 'Simple Hill Climbing', steepest_hc: 'Steepest-Ascent HC',
    stochastic_hc: 'Stochastic HC', simulated_annealing: 'Simulated Annealing',
    random_restart_hc: 'Random Restart HC', local_beam: 'Local Beam Search',
    and_or: 'AND-OR Graph Search',
    sensorless: 'Belief State',
    partial_observable: 'Belief State & Goal',
    ac3: 'AC-3',
    backtracking: 'Backtracking',
    forward_tracking: 'Forward Tracking',
    min_conflicts: 'Min-Conflicts',
    minimax: 'Minimax',
    alpha_beta: 'Alpha-Beta',
    expectimax: 'Expectimax'
};

const hasEarlyLate = ['bfs', 'dfs'];
const hasDepthLimit = ['ids'];
const localSearchAlgos = ['simple_hc', 'steepest_hc', 'stochastic_hc', 'simulated_annealing', 'random_restart_hc', 'local_beam'];
const complexEnvAlgos = ['and_or', 'sensorless', 'partial_observable'];
const cspAlgos = ['ac3', 'backtracking', 'forward_tracking', 'min_conflicts'];

function toggleDropdown() {
    const menu = document.getElementById('algo-menu');
    const btn = document.getElementById('algo-toggle');
    menu.classList.toggle('show');
    btn.classList.toggle('open');
}

function renderConfigUI() {
    const body = document.getElementById('config-body');
    const title = document.getElementById('config-title');
    
    if (adversarialAlgos.includes(currentAlgo)) {
        title.textContent = '2. Caro Game Control';
        title.className = 'font-bold text-[15px] text-on-surface';
        body.innerHTML = `
            <div class="flex flex-col items-center justify-center w-full mt-1">
                <p class="text-center italic text-secondary mb-2.5 text-[12.5px] leading-tight">
                    Nhấp vào các ô trống trên lưới để đi quân X.<br>AI sẽ dùng thuật toán <strong>${algoNames[currentAlgo]}</strong> để trả lời.
                </p>
                <div class="flex gap-2 w-full justify-center">
                    <button onclick="resetBoard()" class="px-4 h-8 bg-surface-container-low border border-outline-variant/30 rounded-full flex items-center justify-center transition-all hover:bg-surface-container-highest cursor-pointer">
                        <span class="font-bold text-on-surface-variant text-[12px]">Reset Game</span>
                    </button>
                    <button onclick="loadExample()" class="px-4 h-8 bg-surface-container-low border border-outline-variant/30 rounded-full flex items-center justify-center transition-all hover:bg-surface-container-highest cursor-pointer">
                        <span class="font-bold text-on-surface-variant text-[12px]">Tải Mẫu Đấu</span>
                    </button>
                </div>
            </div>`;
        return;
    }
    
    if (currentAlgo === 'ucs') {
        title.textContent = '2. UCS Configuration';
        title.className = 'font-bold text-[15px] text-on-surface';
        body.innerHTML = `
            <div class="flex flex-col items-center justify-center w-full mt-1">
                <p class="text-center italic text-secondary mb-2.5 text-[12.5px] leading-tight">
                    Chi phí hành động = Giá trị của ô số di chuyển
                </p>
                <button onclick="callSolve('late')" class="w-full max-w-[240px] h-9 bg-primary text-white rounded-full flex items-center justify-center transition-all hover:bg-primary/90 cursor-pointer shadow-sm">
                    <span class="font-bold text-[13px]">Run Uniform Cost Search</span>
                </button>
            </div>`;
        return;
    }
    
    if (currentAlgo === 'greedy') {
        title.textContent = '2. Greedy Best-First Configuration';
        title.className = 'font-bold text-[15px] text-on-surface';
        body.innerHTML = `
            <div class="flex flex-col items-center justify-center w-full mt-1">
                <p class="text-center italic text-secondary mb-2.5 text-[12.5px] leading-tight">
                    f(n) = h(n) = Khoảng cách Manhattan
                </p>
                <button onclick="callSolve('none')" class="w-full max-w-[240px] h-9 bg-primary text-white rounded-full flex items-center justify-center transition-all hover:bg-primary/90 cursor-pointer shadow-sm">
                    <span class="font-bold text-[13px]">Run Greedy Best-First</span>
                </button>
            </div>`;
        return;
    }
    
    if (currentAlgo === 'astar') {
        title.textContent = '2. A* Configuration';
        title.className = 'font-bold text-[15px] text-on-surface';
        body.innerHTML = `
            <div class="flex flex-col items-center justify-center w-full mt-1">
                <p class="text-center italic text-secondary mb-2.5 text-[12.5px] leading-tight">
                    f(n) = g(n) + h(n)<br>
                    g(n) = Nghịch thế rời rạc | h(n) = Số ô sai vị trí
                </p>
                <button onclick="callSolve('late')" class="w-full max-w-[240px] h-9 bg-primary text-white rounded-full flex items-center justify-center transition-all hover:bg-primary/90 cursor-pointer shadow-sm">
                    <span class="font-bold text-[13px]">Run A* Search</span>
                </button>
            </div>`;
        return;
    }
    
    if (localSearchAlgos.includes(currentAlgo)) {
        title.textContent = '2. ' + algoNames[currentAlgo] + ' Configuration';
        title.className = 'font-bold text-[15px] text-on-surface';
        let configHtml = '<div class="flex flex-col items-center justify-center w-full mt-1">';
        
        if (currentAlgo === 'simple_hc' || currentAlgo === 'steepest_hc' || currentAlgo === 'stochastic_hc') {
            configHtml += `<p class="text-center italic text-secondary mb-2 text-[12.5px] leading-tight">Chọn heuristic:</p>
                <div class="flex gap-2 mb-2.5 w-full max-w-[280px]">
                    <label class="flex-1 flex items-center gap-1.5 cursor-pointer px-2 py-1.5 rounded-lg border border-outline-variant hover:bg-surface-container-low transition-colors">
                        <input type="radio" name="hc-heuristic" value="misplaced" checked class="accent-primary"> <span class="text-[11.5px] font-semibold">Số ô sai</span>
                    </label>
                    <label class="flex-1 flex items-center gap-1.5 cursor-pointer px-2 py-1.5 rounded-lg border border-outline-variant hover:bg-surface-container-low transition-colors">
                        <input type="radio" name="hc-heuristic" value="manhattan" class="accent-primary"> <span class="text-[11.5px] font-semibold">Manhattan</span>
                    </label>
                </div>`;
        } else if (currentAlgo === 'simulated_annealing') {
            configHtml += `<p class="text-center italic text-secondary mb-2 text-[12.5px] leading-tight">h(n) = Số ô sai vị trí<br>T₀ = 1000, α = 0.95</p>`;
        } else if (currentAlgo === 'random_restart_hc') {
            configHtml += `<p class="text-center italic text-secondary mb-2 text-[12.5px] leading-tight">h(n) = Manhattan | Max restarts = 20</p>`;
        } else if (currentAlgo === 'local_beam') {
            configHtml += `<p class="text-center italic text-secondary mb-1.5 text-[12.5px] leading-tight">h(n) = Manhattan</p>
                <div class="flex items-center gap-3 mb-2.5">
                    <span class="font-label-md text-[12px] text-on-surface-variant font-semibold">Beam k:</span>
                    <div class="flex items-center border border-outline-variant rounded-lg overflow-hidden">
                        <button onclick="adjustBeamK(-1)" class="w-7 h-8 flex items-center justify-center bg-surface-container-low hover:bg-surface-container-highest transition-colors cursor-pointer border-r border-outline-variant"><span class="text-primary font-bold text-[14px]">−</span></button>
                        <input type="number" id="beam-k" value="3" min="1" max="20" class="w-12 h-8 text-center font-headline-sm text-[14px] font-bold text-primary bg-white border-none focus:outline-none focus:ring-0">
                        <button onclick="adjustBeamK(1)" class="w-7 h-8 flex items-center justify-center bg-surface-container-low hover:bg-surface-container-highest transition-colors cursor-pointer border-l border-outline-variant"><span class="text-primary font-bold text-[14px]">+</span></button>
                    </div>
                </div>`;
        }
        
        configHtml += `<button onclick="callSolve('none')" class="w-full max-w-[240px] h-9 bg-primary text-white rounded-full flex items-center justify-center transition-all hover:bg-primary/90 cursor-pointer shadow-sm">
            <span class="font-bold text-[13px]">Run ${algoNames[currentAlgo]}</span>
        </button></div>`;
        body.innerHTML = configHtml;
        return;
    }
    
    if (complexEnvAlgos.includes(currentAlgo)) {
        title.textContent = '2. ' + algoNames[currentAlgo] + ' Configuration';
        title.className = 'font-bold text-[15px] text-on-surface';
        let configHtml = '<div class="flex flex-col items-center justify-center w-full mt-1">';
        
        if (currentAlgo === 'and_or') {
            configHtml += `<p class="text-center italic text-secondary mb-1.5 text-[12.5px] leading-tight">Môi trường phức tạp, tìm kiếm dưới dạng AND-OR</p>
                <div class="flex items-center gap-3 mb-2.5">
                    <span class="font-label-md text-[12px] text-on-surface-variant font-semibold">Giới hạn:</span>
                    <div class="flex items-center border border-outline-variant rounded-lg overflow-hidden">
                        <button onclick="adjustDepth(-1)" class="w-7 h-8 flex items-center justify-center bg-surface-container-low hover:bg-surface-container-highest transition-colors cursor-pointer border-r border-outline-variant"><span class="text-primary font-bold text-[14px]">−</span></button>
                        <input type="number" id="depth-limit" value="15" min="1" max="50" class="w-12 h-8 text-center font-headline-sm text-[14px] font-bold text-primary bg-white border-none focus:outline-none focus:ring-0">
                        <input type="hidden" id="beam-k" value="3">
                        <button onclick="adjustDepth(1)" class="w-7 h-8 flex items-center justify-center bg-surface-container-low hover:bg-surface-container-highest transition-colors cursor-pointer border-l border-outline-variant"><span class="text-primary font-bold text-[14px]">+</span></button>
                    </div>
                </div>`;
        }
        
        configHtml += `<button onclick="callSolve('none')" class="w-full max-w-[240px] h-9 bg-primary text-white rounded-full flex items-center justify-center transition-all hover:bg-primary/90 cursor-pointer shadow-sm">
            <span class="font-bold text-[13px]">Run ${algoNames[currentAlgo]}</span>
        </button></div>`;
        body.innerHTML = configHtml;
        return;
    }
    
    title.className = 'font-headline-sm text-headline-sm text-on-surface';
    title.textContent = '2. ' + algoNames[currentAlgo] + ' Configuration';
    
    if (hasEarlyLate.includes(currentAlgo)) {
        body.innerHTML = `
            <div class="flex gap-3 justify-center w-full mt-3">
                <button id="btn-early" onclick="callSolve('early')" class="flex-1 h-9 px-4 bg-white shadow-sm border border-outline-variant rounded-full flex items-center justify-center transition-all hover:bg-surface-container-low cursor-pointer">
                    <span class="font-bold text-primary text-[13px]">Early Goal Test</span>
                </button>
                <button id="btn-late" onclick="callSolve('late')" class="flex-1 h-9 px-4 bg-surface-container-low border border-outline-variant/30 rounded-full flex items-center justify-center transition-all hover:bg-surface-container-highest/50 cursor-pointer">
                    <span class="font-bold text-on-surface-variant text-[13px]">Late Goal Test</span>
                </button>
            </div>`;
    } else if (hasDepthLimit.includes(currentAlgo) || cspAlgos.includes(currentAlgo)) {
        const limitLabel = cspAlgos.includes(currentAlgo) ? "Limit" : "Depth Limit";
        body.innerHTML = `
            <div class="flex flex-col gap-2 items-center justify-center w-full mt-1">
                <div class="flex items-center gap-3">
                    <span class="font-label-md text-[12px] text-on-surface-variant font-semibold">${limitLabel}:</span>
                    <div class="flex items-center border border-outline-variant rounded-lg overflow-hidden">
                        <button onclick="adjustDepth(-1)" class="w-7 h-8 flex items-center justify-center bg-surface-container-low hover:bg-surface-container-highest transition-colors cursor-pointer border-r border-outline-variant">
                            <span class="text-primary font-bold text-[14px]">−</span>
                        </button>
                        <input type="number" id="depth-limit" value="50" min="1" max="200" class="w-12 h-8 text-center font-headline-sm text-[14px] font-bold text-primary bg-white border-none focus:outline-none focus:ring-0">
                        <button onclick="adjustDepth(1)" class="w-7 h-8 flex items-center justify-center bg-surface-container-low hover:bg-surface-container-highest transition-colors cursor-pointer border-l border-outline-variant">
                            <span class="text-primary font-bold text-[14px]">+</span>
                        </button>
                    </div>
                </div>
                <button onclick="callSolve('none')" class="w-full h-9 bg-primary text-white rounded-full flex items-center justify-center transition-all hover:bg-primary/90 cursor-pointer shadow-sm">
                    <span class="font-bold text-[13px]">Run ${algoNames[currentAlgo]}</span>
                </button>
            </div>`;
    } else {
        body.innerHTML = `
            <div class="flex justify-center w-full mt-3">
                <button onclick="callSolve('none')" class="w-full h-9 bg-primary text-white rounded-full flex items-center justify-center transition-all hover:bg-primary/90 cursor-pointer shadow-sm">
                    <span class="font-bold text-[13px]">Run ${algoNames[currentAlgo]}</span>
                </button>
            </div>`;
    }
}

function adjustDepth(delta) {
    const input = document.getElementById('depth-limit');
    let val = parseInt(input.value) || 50;
    val = Math.max(1, Math.min(200, val + delta));
    input.value = val;
}

function adjustBeamK(delta) {
    const input = document.getElementById('beam-k');
    let val = parseInt(input.value) || 3;
    val = Math.max(1, Math.min(20, val + delta));
    input.value = val;
}

function selectAlgo(el) {
    document.querySelectorAll('.algo-item').forEach(x => x.classList.remove('active'));
    el.classList.add('active');
    currentAlgo = el.dataset.algo;
    currentCategory = el.dataset.category;
    document.getElementById('algo-label').textContent = algoNames[currentAlgo] + ' (' + currentCategory + ')';
    document.getElementById('algo-menu').classList.remove('show');
    document.getElementById('algo-toggle').classList.remove('open');
    renderConfigUI();
    renderGoalGrid(getGoalForAlgo(currentAlgo));
    loadExample();
}

async function makeCaroPlayerMove(idx) {
    if (caroGameOver || caroTurn !== 'player') return;
    if (caroBoard[idx] !== 0) return;
    
    caroBoard[idx] = 1; // Player plays X
    buildInitialGrid();
    updateBoardPreview();
    
    const logEl = document.getElementById('execution-log');
    if (logEl.innerHTML.includes("Waiting for execution...") || logEl.innerHTML.includes("Đang chạy")) {
        logEl.innerHTML = "";
    }
    
    const stepNum = caroBoard.filter(x => x !== 0).length;
    const r = Math.floor(idx / 3) + 1;
    const c = (idx % 3) + 1;
    logEl.innerHTML += `<div class="mb-1 font-semibold text-blue-600 text-[12px]">Bước ${stepNum}: Người chơi (X) -> ô (Hàng ${r}, Cột ${c})</div>`;
    logEl.scrollTop = logEl.scrollHeight;
    
    caroTurn = 'ai';
    
    // Call the Python solve api for the AI move
    document.getElementById('stat-steps').innerText = "-";
    document.getElementById('stat-nodes').innerText = "Đang tính...";
    document.getElementById('stat-time').innerText = "...";
    
    const result = await pywebview.api.solve(caroBoard, 'none', currentAlgo, 50, 'misplaced', 3, null);
    
    if (result.success) {
        caroBoard = result.board;
        caroGameOver = result.game_over;
        
        document.getElementById('stat-steps').innerText = caroBoard.filter(x => x !== 0).length;
        document.getElementById('stat-nodes').innerText = result.nodes.toLocaleString();
        document.getElementById('stat-time').innerText = result.time + "ms";
        document.getElementById('stat-depth').innerText = caroBoard.filter(x => x !== 0).length;
        
        buildInitialGrid();
        updateBoardPreview();
        
        const aiMove = result.move;
        if (aiMove !== null && aiMove !== undefined) {
            const aiR = Math.floor(aiMove / 3) + 1;
            const aiC = (aiMove % 3) + 1;
            const nextStepNum = caroBoard.filter(x => x !== 0).length;
            logEl.innerHTML += `<div class="mb-1 font-semibold text-red-600 text-[12px]">Bước ${nextStepNum}: AI (O) [${algoNames[currentAlgo]}] -> ô (Hàng ${aiR}, Cột ${aiC})</div>`;
        }
        
        if (caroGameOver) {
            let winMsg = "";
            if (result.winner === 1) {
                winMsg = `<div class="mt-2 p-2 bg-blue-100 text-blue-800 rounded font-bold text-center text-[13px]">🎉 Người chơi (X) THẮNG! 🎉</div>`;
            } else if (result.winner === 2) {
                winMsg = `<div class="mt-2 p-2 bg-red-100 text-red-800 rounded font-bold text-center text-[13px]">🤖 AI (O) THẮNG! 🤖</div>`;
            } else {
                winMsg = `<div class="mt-2 p-2 bg-slate-100 text-slate-800 rounded font-bold text-center text-[13px]">🤝 Trận đấu HÒA! 🤝</div>`;
            }
            logEl.innerHTML += winMsg;
        } else {
            caroTurn = 'player';
        }
        logEl.scrollTop = logEl.scrollHeight;
    } else {
        logEl.innerHTML += `<div class="text-red-500 font-bold">Lỗi khi AI tính toán nước đi.</div>`;
        caroTurn = 'player';
    }
}

document.addEventListener('click', function(e) {
    if(!e.target.closest('.algo-dropdown')) {
        document.getElementById('algo-menu').classList.remove('show');
        document.getElementById('algo-toggle').classList.remove('open');
    }
});

function removeIcons(text) {
    if (text === undefined || text === null) return '';
    const str = String(text);
    const pattern = "\\uD83D\\uDC49|\\uD83C\\uDF89|\\u274C|\\u2705|\\uD83D\\uDE80|\\uD83D\\uDD04|\\uD83D\\uDCCC|\\u2794";
    const regex = new RegExp(pattern, "g");
    return str.replace(regex, '').trim();
}

function formatLocalSearchLog(logData) {
    let html = '';
    logData.forEach(entry => {
        html += `<div class="mb-2">`;
        html += `<p class="mb-1 font-semibold" style="font-size:12px;">Bước ${removeIcons(entry.step)}: ${removeIcons(entry.action_html)}</p>`;
        if (entry.frontier_str) {
            html += `
            <div class="bg-surface-container-low p-1.5 rounded border border-outline-variant/30 inline-block font-mono">
                <pre class="leading-tight text-[11px] font-bold text-on-surface">${removeIcons(entry.frontier_str)}</pre>
            </div>`;
        }
        html += `</div>`;
        html += `<div class="border-t border-outline-variant/20 pt-1 opacity-50 mt-1 mb-1"></div>`;
    });
    return html;
}

async function callSolve(mode) {
    document.getElementById('execution-log').innerHTML = '<span class="text-outline">Đang chạy thuật toán ' + algoNames[currentAlgo] + '...</span>';
    const start_state = [];
    for(let i=0; i<9; i++) {
        let val = parseInt(document.getElementById(`cell-${i}`).value);
        if(isNaN(val)) val = 0;
        start_state.push(val);
    }
    
    let start_state_2 = null;
    if (currentAlgo === 'sensorless' || currentAlgo === 'partial_observable') {
        start_state_2 = [];
        for(let i=9; i<18; i++) {
            let val = parseInt(document.getElementById(`cell-${i}`).value);
            if(isNaN(val)) val = 0;
            start_state_2.push(val);
        }
    }
    
    let depthLimit = 50;
    const depthInput = document.getElementById('depth-limit');
    if(depthInput) depthLimit = parseInt(depthInput.value) || 50;
    
    let heuristic = 'misplaced';
    const hRadio = document.querySelector('input[name="hc-heuristic"]:checked');
    if(hRadio) heuristic = hRadio.value;
    
    let beamK = 3;
    const beamInput = document.getElementById('beam-k');
    if(beamInput) beamK = parseInt(beamInput.value) || 3;
    
    const result = await pywebview.api.solve(start_state, mode, currentAlgo, depthLimit, heuristic, beamK, start_state_2);
    const modeLabel = mode === 'none' ? '' : ' — ' + mode.toUpperCase() + ' GOAL TEST';
    
    if (result.success) {
        document.getElementById('stat-steps').innerText = result.depth;
        document.getElementById('stat-nodes').innerText = result.nodes.toLocaleString();
        document.getElementById('stat-time').innerText = result.time + "ms";
        document.getElementById('stat-depth').innerText = result.depth;
        
        let logHtml = `<div class="text-primary font-bold mb-2" style="font-size:12px;">ĐANG GIẢI BẰNG: ${algoNames[currentAlgo].toUpperCase()}${modeLabel}</div>`;
        if (result.log_data && result.log_data.length > 0) {
            logHtml += formatLocalSearchLog(result.log_data);
        } else {
            logHtml += formatLogState("Trạng thái bắt đầu:", start_state);
            result.path.forEach((step, idx) => { logHtml += formatLogState(idx+1, step[1], step[0]); });
        }
        document.getElementById('execution-log').innerHTML = logHtml;
        animatePath(start_state, result.path, result.start_dual);
    } else {
        let failHtml = '<div class="text-red-600 font-bold" style="font-size:12px;">Không tìm thấy giải pháp!</div>';
        if (result.log_data && result.log_data.length > 0) {
            failHtml += formatLocalSearchLog(result.log_data);
        }
        document.getElementById('execution-log').innerHTML = failHtml;
        document.getElementById('stat-steps').innerText = "-";
        document.getElementById('stat-nodes').innerText = result.nodes.toLocaleString();
        document.getElementById('stat-time').innerText = result.time + "ms";
        document.getElementById('stat-depth').innerText = "-";
        renderBoard(start_state);
        document.getElementById('step-wrapper').innerHTML = `<span style="background:#dc2626; color:white; padding:3px 10px; border-radius:6px; font-size:11px; font-weight:600; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">No Solution</span>`;
    }
}

window.addEventListener('pywebviewready', function() {
    document.getElementById('btn-random').onclick = randomBoard;
    document.getElementById('btn-reset').onclick = resetBoard;
    document.getElementById('btn-load').onclick = loadExample;
    renderGoalGrid(getGoalForAlgo(currentAlgo));
    loadExample();
    renderConfigUI();
});
</script>
</body></html>"""

class Api:
    def solve(self, start_state, mode, algorithm='bfs', depth_limit=50, heuristic='misplaced', beam_k=3, start_state_2=None):
        if algorithm in ['minimax', 'alpha_beta', 'expectimax']:
            return adversarial_solve(start_state, algorithm)
            
        start_time = time.time()
        if algorithm in ['simple_hc', 'steepest_hc', 'stochastic_hc', 'simulated_annealing', 'random_restart_hc', 'local_beam', 'and_or', 'sensorless', 'partial_observable']:
            goal_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]
        else:
            goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        log_data = None
        
        if algorithm == 'bfs':
            path, nodes_generated = bfs(start_state, goal_state, mode)
        elif algorithm == 'dfs':
            path, nodes_generated = dfs(start_state, goal_state, mode)
        elif algorithm == 'ids':
            path, nodes_generated = ids(start_state, goal_state, max_depth=depth_limit)
        elif algorithm == 'ucs':
            path, nodes_generated = ucs(start_state, goal_state, mode)
        elif algorithm == 'astar':
            path, nodes_generated = astar(start_state, goal_state, mode)
        elif algorithm == 'greedy':
            path, nodes_generated = greedy(start_state, goal_state)
        elif algorithm == 'ida_star':
            path, nodes_generated = ida_star(start_state, goal_state)
        elif algorithm == 'simple_hc':
            path, nodes_generated, log_data = simple_hc_solve(start_state, goal_state, heuristic)
        elif algorithm == 'steepest_hc':
            path, nodes_generated, log_data = steepest_hc_solve(start_state, goal_state, heuristic)
        elif algorithm == 'stochastic_hc':
            path, nodes_generated, log_data = stochastic_hill_climbing_solve(start_state, goal_state, heuristic)
        elif algorithm == 'simulated_annealing':
            path, nodes_generated, log_data = simulated_annealing_solve(start_state, goal_state)
        elif algorithm == 'random_restart_hc':
            result = random_restart_hill_climbing_solve(start_state, goal_state)
            path, nodes_generated, log_data = result[0], result[1], result[2]
        elif algorithm == 'local_beam':
            path, nodes_generated, log_data = local_beam_search_solve(start_state, goal_state, k=beam_k)
        elif algorithm == 'and_or':
            path, nodes_generated, log_data = and_or_graph_search_solve(start_state, goal_state, limit=depth_limit)
        elif algorithm == 'sensorless':
            path, nodes_generated, log_data = sensorless_search_solve(start_state, goal_state, start_state_2)
        elif algorithm == 'partial_observable':
            path, nodes_generated, log_data = partial_observable_search_solve(start_state, goal_state, start_state_2)
        elif algorithm == 'ac3':
            path, nodes_generated = ac3_search(start_state, goal_state, depth_limit)
        elif algorithm == 'backtracking':
            path, nodes_generated = backtracking_search(start_state, goal_state, depth_limit)
        elif algorithm == 'forward_tracking':
            path, nodes_generated = forward_tracking_search(start_state, goal_state, depth_limit)
        elif algorithm == 'min_conflicts':
            path, nodes_generated = min_conflicts_search(start_state, goal_state, depth_limit)
        else:
            path, nodes_generated = bfs(start_state, goal_state, mode)
        
        end_time = time.time()
        elapsed_ms = int((end_time - start_time) * 1000)
        
        if path is not None:
            result = {"success": True, "path": path, "nodes": nodes_generated, "time": elapsed_ms, "depth": len(path)}
        else:
            result = {"success": False, "nodes": nodes_generated, "time": elapsed_ms}
        
        if algorithm in ['sensorless', 'partial_observable']:
            alt = start_state_2 if start_state_2 is not None else get_one_alternate_state(start_state)
            result["start_dual"] = [start_state, alt]
        
        if log_data is not None:
            result["log_data"] = log_data
            if path is not None and len(path) == 0 and log_data:
                # Local search may return empty path but not None when stuck
                last_log = log_data[-1] if log_data else {}
                action_html = last_log.get('action_html', '')
                if 'THÀNH CÔNG' not in action_html and 'Đã đạt đích' not in action_html:
                    result["success"] = False
        
        return result

if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        '8-Puzzle Solver Simulator', 
        html=html_content, 
        js_api=api,
        width=1180,  
        height=700,  
        resizable=True
    )
    webview.start()