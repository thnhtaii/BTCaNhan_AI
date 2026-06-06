import webview
import time
from bfs import bfs
import json

html_content = """<!DOCTYPE html><html class="light" lang="en" style="width: 100%; height: 100%; overflow: auto; position: relative;"><head>
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
                    "background": "#f9f9ff",
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
            "spacing": {
                    "base": "4px",
                    "lg": "1rem",
                    "xs": "0.25rem",
                    "md": "0.75rem",
                    "sm": "0.375rem",
                    "xl": "1.25rem",
                    "gutter": "0.75rem",
                    "margin": "1rem"
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
                    "headline-md": ["20px", {"lineHeight": "28px", "letterSpacing": "-0.01em", "fontWeight": "600"}],
                    "label-sm": ["10px", {"lineHeight": "13px", "fontWeight": "600"}],
                    "headline-lg": ["26px", {"lineHeight": "34px", "letterSpacing": "-0.02em", "fontWeight": "700"}],
                    "body-lg": ["14px", {"lineHeight": "20px", "fontWeight": "400"}],
                    "body-md": ["12px", {"lineHeight": "18px", "fontWeight": "400"}],
                    "label-md": ["11px", {"lineHeight": "14px", "letterSpacing": "0.01em", "fontWeight": "500"}],
                    "headline-sm": ["15px", {"lineHeight": "22px", "fontWeight": "600"}]
            }
          },
        },
      }
    </script>
<style>
        body { font-family: 'Inter', sans-serif; background-color: #f5f6f8; margin: 0; }
        .material-symbols-outlined { font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24; }
        .custom-scrollbar::-webkit-scrollbar { width: 5px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(0, 74, 198, 0.1); border-radius: 10px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(0, 74, 198, 0.2); }
        input[type="number"]::-webkit-inner-spin-button, input[type="number"]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
        input[type="number"] { -moz-appearance: textfield; }

        /* Cell with inline spinner - hidden by default, shown on hover */
        .cell-wrapper {
            position: relative;
        }
        .cell-wrapper input {
            width: 100%;
        }
        .spinner-btns {
            position: absolute;
            right: 4px;
            top: 50%;
            transform: translateY(-50%);
            display: flex;
            flex-direction: column;
            gap: 1px;
            opacity: 0;
            transition: opacity 0.2s ease;
            pointer-events: none;
        }
        .cell-wrapper:hover .spinner-btns {
            opacity: 1;
            pointer-events: auto;
        }
        .spinner-btns button {
            width: 18px;
            height: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(225, 232, 253, 0.9);
            border: 1px solid #c3c6d7;
            border-radius: 3px;
            cursor: pointer;
            color: #434655;
            font-size: 8px;
            line-height: 1;
            padding: 0;
            transition: background 0.15s;
        }
        .spinner-btns button:hover { background: #d3daef; }
        .spinner-btns button:active { background: #b4c5ff; }
    </style>
</head>
<body class="bg-background text-on-surface">
<!-- TopNavBar -->
<header class="flex justify-between items-center px-margin h-12 w-full bg-surface-container-lowest border-b border-outline-variant top-0 z-50">
<div class="flex items-center gap-md">
<span class="font-headline-sm text-headline-sm font-bold text-on-surface">8-Puzzle Solver Simulator</span>
</div>
<nav class="hidden md:flex items-center gap-lg">
<div class="relative group">
<button class="flex items-center gap-xs text-primary font-bold border-b-2 border-primary pb-1 font-label-md text-label-md cursor-pointer active:opacity-80 transition-all">
<span>BFS (Uninformed)</span>
</button>
</div>
</nav>
</header>
<!-- Main Content Canvas -->
<main class="p-margin">
<div class="grid grid-cols-1 lg:grid-cols-12 gap-gutter max-w-[1600px] mx-auto">
<!-- Left Column (8 Columns Wide) -->
<div class="lg:col-span-8 flex flex-col gap-gutter">
<div class="grid grid-cols-1 md:grid-cols-2 gap-gutter">
<!-- 1. Initial State Card -->
<section class="bg-surface-container-lowest border border-outline-variant rounded-xl p-lg">
<div class="flex items-center justify-between mb-sm border-b border-outline-variant pb-sm">
<h3 class="font-headline-sm text-headline-sm text-on-surface">1. Initial State</h3>
<span class="material-symbols-outlined text-outline text-[18px]">tune</span>
</div>
<div class="grid grid-cols-3 gap-sm mb-md" id="initial-grid">
<!-- JS will build cells with spinners -->
</div>
<div class="flex gap-sm">
<button id="btn-random" class="flex-1 py-1 bg-secondary text-on-secondary rounded-lg font-label-md text-label-md hover:opacity-90 transition-opacity">Random</button>
<button id="btn-reset" class="flex-1 py-1 border border-outline-variant text-secondary rounded-lg font-label-md text-label-md hover:bg-surface-container-low transition-colors">Reset</button>
<button id="btn-load" class="flex-1 py-1 border border-outline-variant text-secondary rounded-lg font-label-md text-label-md hover:bg-surface-container-low transition-colors">Load Example</button>
</div>
</section>
<!-- Goal State Card -->
<section class="bg-surface-container-lowest border border-outline-variant rounded-xl p-lg">
<div class="flex items-center justify-between mb-sm border-b border-outline-variant pb-sm">
<h3 class="font-headline-sm text-headline-sm text-on-surface">Goal State</h3>
<span class="material-symbols-outlined text-primary text-[18px]">check_circle</span>
</div>
<div class="grid grid-cols-3 gap-sm">
<div class="h-10 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-headline-sm text-on-surface border border-outline-variant/20">1</div>
<div class="h-10 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-headline-sm text-on-surface border border-outline-variant/20">2</div>
<div class="h-10 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-headline-sm text-on-surface border border-outline-variant/20">3</div>
<div class="h-10 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-headline-sm text-on-surface border border-outline-variant/20">4</div>
<div class="h-10 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-headline-sm text-on-surface border border-outline-variant/20">5</div>
<div class="h-10 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-headline-sm text-on-surface border border-outline-variant/20">6</div>
<div class="h-10 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-headline-sm text-on-surface border border-outline-variant/20">7</div>
<div class="h-10 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-headline-sm text-on-surface border border-outline-variant/20">8</div>
<div class="h-10 flex items-center justify-center bg-surface-container-lowest rounded-lg font-label-sm text-label-sm text-outline-variant border border-dashed border-outline-variant"><br></div>
</div>
</section></div>
<!-- 3. Visual Simulation Card -->
<section class="bg-surface-container-lowest border border-outline-variant rounded-xl p-lg">
<div class="flex items-center justify-between border-b border-outline-variant pb-sm mb-sm">
<h3 class="font-headline-sm text-headline-sm text-on-surface">3. Visual Simulation</h3>
<span id="step-label" class="px-sm py-0.5 bg-surface-container-high text-on-surface-variant rounded font-label-sm text-label-sm">Ready</span>
</div>
<div class="flex items-center justify-center">
<div id="anim-board" class="w-full max-w-[280px] aspect-square bg-surface-container-low rounded-xl p-sm grid grid-cols-3 gap-sm relative overflow-hidden">
<!-- JS Will populate board here -->
</div>
</div>
</section>
</div>
<!-- Right Column (4 Columns Wide) -->
<div class="lg:col-span-4 flex flex-col gap-gutter">
<!-- Statistics Grid -->
<div class="grid grid-cols-2 gap-sm">
<div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-md">
<span class="font-label-sm text-label-sm text-outline uppercase block mb-xs">Steps</span>
<div id="stat-steps" class="font-headline-md text-headline-md text-on-surface">-</div>
</div>
<div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-md">
<span class="font-label-sm text-label-sm text-outline uppercase block mb-xs">Nodes</span>
<div id="stat-nodes" class="font-headline-md text-headline-md text-on-surface">-</div>
</div>
<div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-md">
<span class="font-label-sm text-label-sm text-outline uppercase block mb-xs">Time</span>
<div id="stat-time" class="font-headline-md text-headline-md text-on-surface">-</div>
</div>
<div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-md">
<span class="font-label-sm text-label-sm text-outline uppercase block mb-xs">Max Depth</span>
<div id="stat-depth" class="font-headline-md text-headline-md text-on-surface">-</div>
</div>
</div>
<!-- BFS Configuration -->
<section class="bg-surface-container-lowest border border-outline-variant rounded-xl p-lg">
<div class="flex items-center justify-between mb-sm border-b border-outline-variant pb-sm">
<h3 class="font-headline-sm text-headline-sm text-on-surface">2. BFS Configuration</h3>
</div>
<div class="flex flex-col gap-sm items-center">
<button id="btn-early" class="w-full h-10 px-md bg-white shadow-sm border border-outline-variant rounded-full flex items-center justify-center transition-all hover:bg-surface-container-low cursor-pointer">
<span class="font-bold text-primary text-label-md">Early Goal Test</span>
</button>
<button id="btn-late" class="w-full h-10 px-md bg-surface-container-low border border-outline-variant/30 rounded-full flex items-center justify-center transition-all hover:bg-surface-container-highest/50 cursor-pointer">
<span class="font-bold text-on-surface-variant text-label-md">Late Goal Test</span>
</button>
</div>
</section>
<!-- Execution Log -->
<section class="bg-surface-container-high border border-outline-variant rounded-xl flex flex-col shadow-sm" style="height: 280px;">
<div class="flex items-center justify-between px-md py-1.5 bg-surface-container-highest border-b border-outline-variant rounded-t-xl">
<div class="flex items-center gap-sm">
<span class="material-symbols-outlined text-primary text-[16px]">terminal</span>
<span class="font-label-md text-label-md font-bold text-on-surface uppercase tracking-wider">Execution Log</span>
</div>
</div>
<div id="execution-log" class="flex-1 p-md font-mono text-[11px] leading-relaxed overflow-y-auto custom-scrollbar text-[#0f172a]">
<span class="text-outline">Waiting for execution...</span>
</div>
</section>
</div>
</div>
</main>

<script>
let animationTimeout;

// ========== INITIAL STATE GRID WITH INLINE SPINNERS ==========
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
        input.className = 'h-11 w-full text-center bg-surface-container-high rounded-lg font-headline-sm text-headline-sm text-primary border border-primary/20 focus:outline-none focus:ring-2 focus:ring-primary';
        input.value = values[i];
        input.min = 0;
        input.max = 8;
        input.dataset.prev = values[i];
        
        input.addEventListener('change', function() {
            handleCellChange(i);
        });
        
        const spinBtns = document.createElement('div');
        spinBtns.className = 'spinner-btns';
        
        const btnUp = document.createElement('button');
        btnUp.innerHTML = '&#9650;';
        btnUp.title = 'Tăng';
        btnUp.addEventListener('click', (e) => { e.preventDefault(); spinCell(i, 1); });
        
        const btnDown = document.createElement('button');
        btnDown.innerHTML = '&#9660;';
        btnDown.title = 'Giảm';
        btnDown.addEventListener('click', (e) => { e.preventDefault(); spinCell(i, -1); });
        
        spinBtns.appendChild(btnUp);
        spinBtns.appendChild(btnDown);
        
        wrapper.appendChild(input);
        wrapper.appendChild(spinBtns);
        grid.appendChild(wrapper);
    }
}

function getCellValue(idx) {
    return parseInt(document.getElementById(`cell-${idx}`).value) || 0;
}

function setCellValue(idx, val) {
    const el = document.getElementById(`cell-${idx}`);
    el.value = val;
    el.dataset.prev = val;
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
        if(getCellValue(i) === newVal) {
            setCellValue(i, oldVal);
            break;
        }
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
        if(getCellValue(i) === newVal) {
            setCellValue(i, oldVal);
            break;
        }
    }
    setCellValue(idx, newVal);
    updateBoardPreview();
}

function updateBoardPreview() {
    const state = [];
    for(let i = 0; i < 9; i++) state.push(getCellValue(i));
    renderBoard(state);
}

// ========== VISUAL SIMULATION BOARD ==========
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

// ========== BUTTONS ==========
function randomBoard() {
    let nums = [1,2,3,4,5,6,7,8,0];
    for(let i=nums.length-1; i>0; i--){
        const j = Math.floor(Math.random()*(i+1));
        [nums[i], nums[j]] = [nums[j], nums[i]];
    }
    buildInitialGrid(nums);
    renderBoard(nums);
}

function resetBoard() {
    const nums = [1,2,3,4,5,6,7,8,0];
    buildInitialGrid(nums);
    renderBoard(nums);
}

function loadExample() {
    const nums = [1,8,3,2,6,4,7,0,5];
    buildInitialGrid(nums);
    renderBoard(nums);
}

// ========== LOG FORMATTING ==========
function formatLogState(title, state, action=null) {
    let stateStr = "";
    for(let i=0; i<9; i+=3) {
        let row = state.slice(i, i+3).map(x => (x===0 || x==='0') ? "[ ]" : ("  "+x+"  ")).join("");
        stateStr += " " + row + "\\n";
    }
    let titleHtml = action ? `<p class="mb-1 font-semibold" style="font-size:12px;">Bước ${title}: Di chuyển ô trống sang <span class="text-primary">${action}</span></p>` 
                           : `<p class="mb-1 font-semibold" style="font-size:12px;">${title}</p>`;
                           
    return `
    <div>
        ${titleHtml}
        <div class="bg-surface-container-low p-2 rounded border border-outline-variant/30 inline-block">
            <pre class="leading-tight" style="font-size:11px;">${stateStr}</pre>
        </div>
    </div>
    <div class="border-t border-outline-variant/20 pt-1 opacity-50 mt-2 mb-2"></div>
    `;
}

// ========== ANIMATION ==========
async function animatePath(start_state, path) {
    clearTimeout(animationTimeout);
    renderBoard(start_state);
    document.getElementById('step-label').textContent = `Step 0/${path.length}`;
    
    await new Promise(r => { animationTimeout = setTimeout(r, 800); });
    
    for(let i=0; i<path.length; i++) {
        renderBoard(path[i][1]);
        document.getElementById('step-label').textContent = `Step ${i+1}/${path.length}`;
        await new Promise(r => { animationTimeout = setTimeout(r, 500); });
    }
    document.getElementById('step-label').innerHTML = `<span style="background:#d1fae5; color:#065f46; padding:2px 8px; border-radius:4px; font-size:10px; font-weight:600;">Finished</span>`;
}

// ========== SOLVE ==========
async function callBfs(mode) {
    document.getElementById('execution-log').innerHTML = '<span class="text-outline">Đang chạy thuật toán, vui lòng đợi...</span>';
    
    const start_state = [];
    for(let i=0; i<9; i++) {
        let val = parseInt(document.getElementById(`cell-${i}`).value);
        if(isNaN(val)) val = 0;
        start_state.push(val);
    }
    
    const result = await pywebview.api.solve(start_state, mode);
    
    if (result.success) {
        document.getElementById('stat-steps').innerText = result.depth;
        document.getElementById('stat-nodes').innerText = result.nodes.toLocaleString();
        document.getElementById('stat-time').innerText = result.time + "ms";
        document.getElementById('stat-depth').innerText = result.depth;
        
        let logHtml = `<div class="text-primary font-bold mb-3" style="font-size:12px;">ĐANG GIẢI BẰNG: ${mode.toUpperCase()} GOAL TEST</div>`;
        logHtml += formatLogState("Trạng thái bắt đầu:", start_state);
        result.path.forEach((step, idx) => {
            logHtml += formatLogState(idx+1, step[1], step[0]);
        });
        document.getElementById('execution-log').innerHTML = logHtml;
        
        animatePath(start_state, result.path);
    } else {
        document.getElementById('execution-log').innerHTML = '<div class="text-red-600 font-bold" style="font-size:12px;">Không tìm thấy giải pháp!</div>';
        document.getElementById('stat-steps').innerText = "-";
        document.getElementById('stat-nodes').innerText = result.nodes.toLocaleString();
        document.getElementById('stat-time').innerText = result.time + "ms";
        document.getElementById('stat-depth').innerText = "-";
        renderBoard(start_state);
        document.getElementById('step-label').innerHTML = `<span style="background:#fee2e2; color:#991b1b; padding:2px 8px; border-radius:4px; font-size:10px; font-weight:600;">No Solution</span>`;
    }
}

// ========== INIT ==========
window.addEventListener('pywebviewready', function() {
    document.getElementById('btn-early').onclick = () => callBfs('early');
    document.getElementById('btn-late').onclick = () => callBfs('late');
    document.getElementById('btn-random').onclick = randomBoard;
    document.getElementById('btn-reset').onclick = resetBoard;
    document.getElementById('btn-load').onclick = loadExample;
    loadExample();
});
</script>
</body></html>"""

class Api:
    def solve(self, start_state, mode):
        start_time = time.time()
        goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        
        # Gọi hàm BFS từ bfs.py
        path, nodes_generated = bfs(start_state, goal_state, mode)
        
        end_time = time.time()
        elapsed_ms = int((end_time - start_time) * 1000)
        
        if path is not None:
            return {
                "success": True,
                "path": path,
                "nodes": nodes_generated,
                "time": elapsed_ms,
                "depth": len(path)
            }
        else:
            return {
                "success": False,
                "nodes": nodes_generated,
                "time": elapsed_ms
            }

if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        '8-Puzzle Solver Simulator', 
        html=html_content, 
        js_api=api,
        width=1300, 
        height=850,
        resizable=True
    )
    webview.start()