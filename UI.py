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
            </div>
        </div>
    </nav>
</header>

<main class="flex-1 w-full p-4 overflow-hidden flex items-center justify-center">
<div class="grid grid-cols-1 lg:grid-cols-12 gap-4 w-full max-w-[1180px] mx-auto items-start">
    
    <div class="lg:col-span-7 flex flex-col gap-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <section class="bg-surface-container-lowest border border-outline-variant rounded-xl p-4 shadow-sm">
                <div class="flex items-center justify-between mb-2.5 border-b border-outline-variant pb-2">
                    <h3 class="font-headline-sm text-headline-sm text-on-surface">1. Initial State</h3>
                    <span class="material-symbols-outlined text-outline text-[16px]">tune</span>
                </div>
                <div class="grid grid-cols-3 gap-2 mb-3.5" id="initial-grid"></div>
                <div class="flex gap-2">
                    <button id="btn-random" class="flex-1 py-1.5 bg-[#e1e8fd] text-primary border border-primary/20 rounded-lg font-semibold text-label-md hover:bg-[#d3daef] transition-colors">Random</button>
                    <button id="btn-reset" class="flex-1 py-1.5 bg-[#e1e8fd] text-primary border border-primary/20 rounded-lg font-semibold text-label-md hover:bg-[#d3daef] transition-colors">Reset</button>
                    <button id="btn-load" class="flex-1 py-1.5 bg-[#e1e8fd] text-primary border border-primary/20 rounded-lg font-semibold text-label-md hover:bg-[#d3daef] transition-colors">Load Example</button>
                </div>
            </section>
            
            <section class="bg-surface-container-lowest border border-outline-variant rounded-xl p-4 shadow-sm">
                <div class="flex items-center justify-between mb-2.5 border-b border-outline-variant pb-2">
                    <h3 class="font-headline-sm text-headline-sm text-on-surface">Goal State</h3>
                    <span class="material-symbols-outlined text-primary text-[16px]">check_circle</span>
                </div>
                <div class="grid grid-cols-3 gap-2 mb-3.5">
                    <div class="h-12 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-[17px] font-bold text-on-surface border border-outline-variant/20">1</div>
                    <div class="h-12 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-[17px] font-bold text-on-surface border border-outline-variant/20">2</div>
                    <div class="h-12 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-[17px] font-bold text-on-surface border border-outline-variant/20">3</div>
                    <div class="h-12 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-[17px] font-bold text-on-surface border border-outline-variant/20">4</div>
                    <div class="h-12 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-[17px] font-bold text-on-surface border border-outline-variant/20">5</div>
                    <div class="h-12 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-[17px] font-bold text-on-surface border border-outline-variant/20">6</div>
                    <div class="h-12 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-[17px] font-bold text-on-surface border border-outline-variant/20">7</div>
                    <div class="h-12 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-[17px] font-bold text-on-surface border border-outline-variant/20">8</div>
                    <div class="h-12 flex items-center justify-center bg-surface-container-lowest rounded-lg text-outline-variant border border-dashed border-outline-variant"></div>
                </div>
            </section>
        </div>
        
        <section class="bg-surface-container-lowest border border-outline-variant rounded-xl p-4 shadow-sm flex flex-col items-center">
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
        
        <section class="bg-surface-container-lowest border border-outline-variant rounded-xl p-4 shadow-sm">
            <div class="flex items-center justify-between mb-2 border-b border-outline-variant pb-1.5">
                <h3 id="config-title" class="font-headline-sm text-headline-sm text-on-surface">2. BFS Configuration</h3>
            </div>
            <div id="config-body"></div>
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

function buildInitialGrid(values) {
    const grid = document.getElementById('initial-grid');
    grid.innerHTML = '';
    for(let i = 0; i < 9; i++) {
        const wrapper = document.createElement('div');
        wrapper.className = 'cell-wrapper';
        
        const input = document.createElement('input');
        input.type = 'number';
        input.id = `cell-${i}`;
        input.className = 'h-12 w-full text-center bg-surface-container-high rounded-lg font-headline-sm text-[18px] font-bold text-primary border border-primary/20 focus:outline-none focus:ring-2 focus:ring-primary';
        input.value = values[i];
        input.min = 0;
        input.max = 8;
        input.dataset.prev = values[i];
        
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
        grid.appendChild(wrapper);
    }
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
    for(let i = 0; i < 9; i++) {
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
    for(let i = 0; i < 9; i++) {
        if(i === idx) continue;
        if(getCellValue(i) === newVal) { setCellValue(i, oldVal); break; }
    }
    setCellValue(idx, newVal);
    updateBoardPreview();
}

function updateBoardPreview() {
    const state = [];
    for(let i = 0; i < 9; i++) state.push(getCellValue(i));
    renderBoard(state);
}

function renderBoard(state) {
    const board = document.getElementById('anim-board');
    board.innerHTML = '';
    state.forEach(val => {
        if(val === 0) {
            board.innerHTML += `<div class="aspect-square bg-surface-container-highest/20 rounded-lg border-2 border-dashed border-outline-variant"></div>`;
        } else {
            board.innerHTML += `<div class="aspect-square bg-white shadow-sm border border-outline-variant rounded-lg flex items-center justify-center font-headline-lg text-headline-lg text-primary">${val}</div>`;
        }
    });
}

function randomBoard() {
    let nums = [1,2,3,4,5,6,7,8,0];
    for(let i=nums.length-1; i>0; i--){
        const j = Math.floor(Math.random()*(i+1));
        [nums[i], nums[j]] = [nums[j], nums[i]];
    }
    buildInitialGrid(nums); renderBoard(nums);
}

function resetBoard() {
    const nums = [1,2,3,4,5,6,7,8,0];
    buildInitialGrid(nums); renderBoard(nums);
}

function loadExample() {
    const nums = [1, 8, 3, 2, 6, 4, 7, 0, 5];
    buildInitialGrid(nums); renderBoard(nums);
}

function formatLogState(title, state, action=null) {
    let stateStr = "";
    for(let i=0; i<9; i+=3) {
        let row = state.slice(i, i+3).map(x => (x===0 || x==='0') ? "[ ]" : ("  "+x+"  ")).join("");
        stateStr += " " + row + "\\n";
    }
    let titleHtml = action ? `<p class="mb-1 font-semibold" style="font-size:12px;">Bước ${title}: Di chuyển ô trống sang <span class="text-primary">${action}</span></p>` 
                           : `<p class="mb-1 font-semibold" style="font-size:12px;">${title}</p>`;
                           
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

async function animatePath(start_state, path) {
    clearTimeout(animationTimeout);
    renderBoard(start_state);
    
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
    astar: 'A*', greedy: 'Greedy Best-First', ida_star: 'IDA*'
};

const hasEarlyLate = ['bfs', 'dfs', 'astar'];
const hasDepthLimit = ['ids'];

function toggleDropdown() {
    const menu = document.getElementById('algo-menu');
    const btn = document.getElementById('algo-toggle');
    menu.classList.toggle('show');
    btn.classList.toggle('open');
}

function renderConfigUI() {
    const body = document.getElementById('config-body');
    const title = document.getElementById('config-title');
    
    if (currentAlgo === 'ucs') {
        title.textContent = '2. UCS Configuration';
        title.className = 'font-bold text-[14px] text-on-surface';
        body.parentElement.className = 'bg-surface-container-lowest border border-outline-variant rounded-xl px-3 py-3 shadow-sm';
        body.innerHTML = `
            <div class="flex flex-col items-center">
                <p class="text-center italic text-secondary mt-2 mb-3 text-[13px] leading-normal">
                    Chi phí hành động = Giá trị của ô số di chuyển
                </p>
                <button onclick="callSolve('late')" class="w-full max-w-[240px] h-9 bg-primary text-white rounded-full flex items-center justify-center transition-all hover:bg-primary/90 cursor-pointer shadow-sm">
                    <span class="font-bold text-[13px]">Uniform Cost Search</span>
                </button>
            </div>`;
        return;
    }
    
    body.parentElement.className = 'bg-surface-container-lowest border border-outline-variant rounded-xl px-3 py-3 shadow-sm';
    title.className = 'font-headline-sm text-headline-sm text-on-surface';
    title.textContent = '2. ' + algoNames[currentAlgo] + ' Configuration';
    
    if (hasEarlyLate.includes(currentAlgo)) {
        body.innerHTML = `
            <div class="flex gap-3 justify-center">
                <button id="btn-early" onclick="callSolve('early')" class="flex-1 h-9 px-4 bg-white shadow-sm border border-outline-variant rounded-full flex items-center justify-center transition-all hover:bg-surface-container-low cursor-pointer">
                    <span class="font-bold text-primary text-[13px]">Early Goal Test</span>
                </button>
                <button id="btn-late" onclick="callSolve('late')" class="flex-1 h-9 px-4 bg-surface-container-low border border-outline-variant/30 rounded-full flex items-center justify-center transition-all hover:bg-surface-container-highest/50 cursor-pointer">
                    <span class="font-bold text-on-surface-variant text-[13px]">Late Goal Test</span>
                </button>
            </div>`;
    } else if (hasDepthLimit.includes(currentAlgo)) {
        body.innerHTML = `
            <div class="flex flex-col gap-3 items-center">
                <div class="flex items-center gap-3">
                    <span class="font-label-md text-[12px] text-on-surface-variant font-semibold">Depth Limit:</span>
                    <div class="flex items-center border border-outline-variant rounded-lg overflow-hidden">
                        <button onclick="adjustDepth(-1)" class="w-8 h-9 flex items-center justify-center bg-surface-container-low hover:bg-surface-container-highest transition-colors cursor-pointer border-r border-outline-variant">
                            <span class="text-primary font-bold text-[16px]">−</span>
                        </button>
                        <input type="number" id="depth-limit" value="50" min="1" max="200" class="w-14 h-9 text-center font-headline-sm text-[16px] font-bold text-primary bg-white border-none focus:outline-none focus:ring-0">
                        <button onclick="adjustDepth(1)" class="w-8 h-9 flex items-center justify-center bg-surface-container-low hover:bg-surface-container-highest transition-colors cursor-pointer border-l border-outline-variant">
                            <span class="text-primary font-bold text-[16px]">+</span>
                        </button>
                    </div>
                </div>
                <button onclick="callSolve('none')" class="w-full h-9 px-4 bg-primary text-white rounded-full flex items-center justify-center transition-all hover:bg-primary/90 cursor-pointer shadow-sm">
                    <span class="font-bold text-[13px]">Run IDS</span>
                </button>
            </div>`;
    } else {
        body.innerHTML = `
            <div class="flex justify-center">
                <button onclick="callSolve('none')" class="w-full h-9 px-4 bg-primary text-white rounded-full flex items-center justify-center transition-all hover:bg-primary/90 cursor-pointer shadow-sm">
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

function selectAlgo(el) {
    document.querySelectorAll('.algo-item').forEach(x => x.classList.remove('active'));
    el.classList.add('active');
    currentAlgo = el.dataset.algo;
    currentCategory = el.dataset.category;
    document.getElementById('algo-label').textContent = algoNames[currentAlgo] + ' (' + currentCategory + ')';
    document.getElementById('algo-menu').classList.remove('show');
    document.getElementById('algo-toggle').classList.remove('open');
    renderConfigUI();
}

document.addEventListener('click', function(e) {
    if(!e.target.closest('.algo-dropdown')) {
        document.getElementById('algo-menu').classList.remove('show');
        document.getElementById('algo-toggle').classList.remove('open');
    }
});

async function callSolve(mode) {
    document.getElementById('execution-log').innerHTML = '<span class="text-outline">Đang chạy thuật toán ' + algoNames[currentAlgo] + '...</span>';
    const start_state = [];
    for(let i=0; i<9; i++) {
        let val = parseInt(document.getElementById(`cell-${i}`).value);
        if(isNaN(val)) val = 0;
        start_state.push(val);
    }
    
    let depthLimit = 50;
    const depthInput = document.getElementById('depth-limit');
    if(depthInput) depthLimit = parseInt(depthInput.value) || 50;
    
    const result = await pywebview.api.solve(start_state, mode, currentAlgo, depthLimit);
    const modeLabel = mode === 'none' ? '' : ' — ' + mode.toUpperCase() + ' GOAL TEST';
    
    if (result.success) {
        document.getElementById('stat-steps').innerText = result.depth;
        document.getElementById('stat-nodes').innerText = result.nodes.toLocaleString();
        document.getElementById('stat-time').innerText = result.time + "ms";
        document.getElementById('stat-depth').innerText = result.depth;
        
        let logHtml = `<div class="text-primary font-bold mb-2" style="font-size:12px;">ĐANG GIẢI BẰNG: ${algoNames[currentAlgo].toUpperCase()}${modeLabel}</div>`;
        logHtml += formatLogState("Trạng thái bắt đầu:", start_state);
        result.path.forEach((step, idx) => { logHtml += formatLogState(idx+1, step[1], step[0]); });
        document.getElementById('execution-log').innerHTML = logHtml;
        animatePath(start_state, result.path);
    } else {
        document.getElementById('execution-log').innerHTML = '<div class="text-red-600 font-bold" style="font-size:12px;">Không tìm thấy giải pháp!</div>';
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
    loadExample();
    renderConfigUI();
});
</script>
</body></html>"""

class Api:
    def solve(self, start_state, mode, algorithm='bfs', depth_limit=50):
        start_time = time.time()
        goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        
        # Dispatch to the selected algorithm
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
        else:
            path, nodes_generated = bfs(start_state, goal_state, mode)
        
        end_time = time.time()
        elapsed_ms = int((end_time - start_time) * 1000)
        
        if path is not None:
            return {"success": True, "path": path, "nodes": nodes_generated, "time": elapsed_ms, "depth": len(path)}
        else:
            return {"success": False, "nodes": nodes_generated, "time": elapsed_ms}

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