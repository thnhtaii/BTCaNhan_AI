import webview
import time
from bfs import bfs
import json

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
                    "headline-md": ["18px", {"lineHeight": "26px", "fontWeight": "600"}],
                    "label-sm": ["11px", {"lineHeight": "14px", "fontWeight": "600"}],
                    "headline-lg": ["24px", {"lineHeight": "30px", "fontWeight": "700"}],
                    "body-lg": ["15px", {"lineHeight": "21px", "fontWeight": "400"}],
                    "body-md": ["13px", {"lineHeight": "18px", "fontWeight": "400"}],
                    "label-md": ["13px", {"lineHeight": "16px", "fontWeight": "600"}],
                    "headline-sm": ["16px", {"lineHeight": "22px", "fontWeight": "600"}]
            }
          },
        },
      }
    </script>
<style>
        body { font-family: 'Inter', sans-serif; background-color: #f5f6f8; margin: 0; }
        .material-symbols-outlined { font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 20; }
        .custom-scrollbar::-webkit-scrollbar { width: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(0, 74, 198, 0.15); border-radius: 10px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(0, 74, 198, 0.3); }
        input[type="number"]::-webkit-inner-spin-button, input[type="number"]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
        input[type="number"] { -moz-appearance: textfield; }

        .cell-wrapper { position: relative; }
        .cell-wrapper input { width: 100%; }
        .spinner-btns {
            position: absolute; right: 5px; top: 50%; transform: translateY(-50%);
            display: flex; flex-direction: column; gap: 2px; opacity: 0;
            transition: opacity 0.2s ease; pointer-events: none;
        }
        .cell-wrapper:hover .spinner-btns { opacity: 1; pointer-events: auto; }
        .spinner-btns button {
            width: 20px; height: 16px; display: flex; align-items: center; justify-content: center;
            background: rgba(255, 255, 255, 0.95); border: 1px solid #c3c6d7; border-radius: 4px;
            cursor: pointer; color: #434655; font-size: 9px; line-height: 1; padding: 0; transition: background 0.15s;
        }
        .spinner-btns button:hover { background: #d3daef; }
    </style>
</head>
<body class="bg-background text-on-surface text-sm flex flex-col h-screen w-screen overflow-hidden">

<header class="flex justify-between items-center px-6 min-h-[60px] w-full bg-surface-container-lowest border-b border-outline-variant shrink-0 z-50">
    <div class="flex items-center gap-3">
        <span class="font-headline-sm text-[18px] font-bold text-on-surface">8-Puzzle Solver Simulator</span>
    </div>
    <nav class="hidden md:flex items-center gap-4">
        <button class="flex items-center gap-1 text-primary font-bold border-b-2 border-primary pb-0.5 font-label-md text-[14px]">
            <span>BFS (Uninformed)</span>
        </button>
    </nav>
</header>

<main class="flex-1 w-full p-6 overflow-y-auto custom-scrollbar">
<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 w-full max-w-[2000px] mx-auto">
    <div class="lg:col-span-7 flex flex-col gap-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <section class="bg-surface-container-lowest border border-outline-variant rounded-xl p-5 shadow-sm">
                <div class="flex items-center justify-between mb-4 border-b border-outline-variant pb-2">
                    <h3 class="font-headline-sm text-headline-sm text-on-surface">1. Initial State</h3>
                    <span class="material-symbols-outlined text-outline text-[18px]">tune</span>
                </div>
                <div class="grid grid-cols-3 gap-3 mb-4" id="initial-grid"></div>
                <div class="flex gap-3">
                    <button id="btn-random" class="flex-1 py-2 bg-[#e1e8fd] text-primary border border-primary/20 rounded-lg font-semibold text-label-md hover:bg-[#d3daef] transition-colors">Random</button>
                    <button id="btn-reset" class="flex-1 py-2 bg-[#e1e8fd] text-primary border border-primary/20 rounded-lg font-semibold text-label-md hover:bg-[#d3daef] transition-colors">Reset</button>
                    <button id="btn-load" class="flex-1 py-2 bg-[#e1e8fd] text-primary border border-primary/20 rounded-lg font-semibold text-label-md hover:bg-[#d3daef] transition-colors">Load Example</button>
                </div>
            </section>
            
            <section class="bg-surface-container-lowest border border-outline-variant rounded-xl p-5 shadow-sm">
                <div class="flex items-center justify-between mb-4 border-b border-outline-variant pb-2">
                    <h3 class="font-headline-sm text-headline-sm text-on-surface">Goal State</h3>
                    <span class="material-symbols-outlined text-primary text-[18px]">check_circle</span>
                </div>
                <div class="grid grid-cols-3 gap-3">
                    <div class="h-12 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-headline-sm text-on-surface border border-outline-variant/20">1</div>
                    <div class="h-12 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-headline-sm text-on-surface border border-outline-variant/20">2</div>
                    <div class="h-12 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-headline-sm text-on-surface border border-outline-variant/20">3</div>
                    <div class="h-12 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-headline-sm text-on-surface border border-outline-variant/20">4</div>
                    <div class="h-12 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-headline-sm text-on-surface border border-outline-variant/20">5</div>
                    <div class="h-12 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-headline-sm text-on-surface border border-outline-variant/20">6</div>
                    <div class="h-12 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-headline-sm text-on-surface border border-outline-variant/20">7</div>
                    <div class="h-12 flex items-center justify-center bg-surface-container-low rounded-lg font-headline-sm text-headline-sm text-on-surface border border-outline-variant/20">8</div>
                    <div class="h-12 flex items-center justify-center bg-surface-container-lowest rounded-lg text-outline-variant border border-dashed border-outline-variant"></div>
                </div>
            </section>
        </div>
        
        <section class="bg-surface-container-lowest border border-outline-variant rounded-xl p-5 shadow-sm flex flex-col items-center">
            <div class="flex items-center justify-between border-b border-outline-variant pb-3 mb-3 w-full">
                <h3 class="font-headline-sm text-headline-sm text-on-surface">3. Visual Simulation</h3>
                <div id="step-wrapper">
                    <span id="step-label" class="px-3 py-1 bg-surface-container-high text-on-surface-variant rounded font-semibold text-label-md">Ready</span>
                </div>
            </div>
            <div class="w-full flex items-center justify-center py-2">
                <div id="anim-board" class="w-full max-w-[260px] aspect-square bg-surface-container-low rounded-xl p-2.5 grid grid-cols-3 gap-2.5 relative overflow-hidden"></div>
            </div>
        </section>
    </div>
    
    <div class="lg:col-span-5 flex flex-col gap-6">
        <div class="grid grid-cols-2 gap-3">
            <div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-4 shadow-sm">
                <span class="font-label-sm text-label-sm text-outline uppercase block mb-1">Steps</span>
                <div id="stat-steps" class="font-headline-md text-headline-md text-on-surface">-</div>
            </div>
            <div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-4 shadow-sm">
                <span class="font-label-sm text-label-sm text-outline uppercase block mb-1">Nodes</span>
                <div id="stat-nodes" class="font-headline-md text-headline-md text-on-surface">-</div>
            </div>
            <div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-4 shadow-sm">
                <span class="font-label-sm text-label-sm text-outline uppercase block mb-1">Time</span>
                <div id="stat-time" class="font-headline-md text-headline-md text-on-surface">-</div>
            </div>
            <div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-4 shadow-sm">
                <span class="font-label-sm text-label-sm text-outline uppercase block mb-1">Max Depth</span>
                <div id="stat-depth" class="font-headline-md text-headline-md text-on-surface">-</div>
            </div>
        </div>
        
        <section class="bg-surface-container-lowest border border-outline-variant rounded-xl p-5 shadow-sm">
            <div class="flex items-center justify-between mb-3 border-b border-outline-variant pb-2">
                <h3 class="font-headline-sm text-headline-sm text-on-surface">2. BFS Configuration</h3>
            </div>
            <div class="flex gap-4 justify-center">
                <button id="btn-early" class="flex-1 h-10 px-4 bg-white shadow-sm border border-outline-variant rounded-full flex items-center justify-center transition-all hover:bg-surface-container-low cursor-pointer">
                    <span class="font-bold text-primary text-[14px]">Early Goal Test</span>
                </button>
                <button id="btn-late" class="flex-1 h-10 px-4 bg-surface-container-low border border-outline-variant/30 rounded-full flex items-center justify-center transition-all hover:bg-surface-container-highest/50 cursor-pointer">
                    <span class="font-bold text-on-surface-variant text-[14px]">Late Goal Test</span>
                </button>
            </div>
        </section>
        
        <section class="bg-surface-container-high border border-outline-variant rounded-xl flex flex-col shadow-sm h-[340px]">
            <div class="flex items-center justify-between px-4 py-2 bg-surface-container-highest border-b border-outline-variant rounded-t-xl">
                <div class="flex items-center gap-2">
                    <span class="material-symbols-outlined text-primary text-[16px]">terminal</span>
                    <span class="font-label-md text-[13px] font-bold text-on-surface uppercase tracking-wider">Execution Log</span>
                </div>
            </div>
            <div id="execution-log" class="flex-1 p-4 font-mono text-[12px] leading-relaxed overflow-y-auto custom-scrollbar text-[#0f172a]">
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
        // Ô số to hơn (h-12)
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
    const nums = [1,8,3,2,6,4,7,0,5];
    buildInitialGrid(nums); renderBoard(nums);
}

function formatLogState(title, state, action=null) {
    let stateStr = "";
    for(let i=0; i<9; i+=3) {
        let row = state.slice(i, i+3).map(x => (x===0 || x==='0') ? "[ ]" : ("  "+x+"  ")).join("");
        stateStr += " " + row + "\\n";
    }
    let titleHtml = action ? `<p class="mb-1.5 font-semibold" style="font-size:13px;">Bước ${title}: Di chuyển ô trống sang <span class="text-primary">${action}</span></p>` 
                           : `<p class="mb-1.5 font-semibold" style="font-size:13px;">${title}</p>`;
                           
    return `
    <div class="mb-2">
        ${titleHtml}
        <div class="bg-surface-container-low p-2 rounded border border-outline-variant/30 inline-block">
            <pre class="leading-tight text-[12px] font-bold text-on-surface">${stateStr}</pre>
        </div>
    </div>
    <div class="border-t border-outline-variant/20 pt-1 opacity-50 mt-2 mb-2"></div>
    `;
}

async function animatePath(start_state, path) {
    clearTimeout(animationTimeout);
    renderBoard(start_state);
    
    document.getElementById('step-wrapper').innerHTML = `<span id="step-label" class="px-3 py-1 bg-surface-container-high text-on-surface-variant rounded font-semibold text-label-md">Step 0/${path.length}</span>`;
    
    await new Promise(r => { animationTimeout = setTimeout(r, 800); });
    for(let i=0; i<path.length; i++) {
        renderBoard(path[i][1]);
        document.getElementById('step-label').textContent = `Step ${i+1}/${path.length}`;
        await new Promise(r => { animationTimeout = setTimeout(r, 500); });
    }
    // Chữ Finished bo nền xanh ngọc đậm đẹp mắt
    document.getElementById('step-wrapper').innerHTML = `<span style="background:#0d9488; color:white; padding:4px 12px; border-radius:6px; font-size:12px; font-weight:600; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">Finished</span>`;
}

async function callBfs(mode) {
    document.getElementById('execution-log').innerHTML = '<span class="text-outline">Đang chạy thuật toán...</span>';
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
        
        let logHtml = `<div class="text-primary font-bold mb-3" style="font-size:13px;">ĐANG GIẢI BẰNG: ${mode.toUpperCase()} GOAL TEST</div>`;
        logHtml += formatLogState("Trạng thái bắt đầu:", start_state);
        result.path.forEach((step, idx) => { logHtml += formatLogState(idx+1, step[1], step[0]); });
        document.getElementById('execution-log').innerHTML = logHtml;
        animatePath(start_state, result.path);
    } else {
        document.getElementById('execution-log').innerHTML = '<div class="text-red-600 font-bold" style="font-size:13px;">Không tìm thấy giải pháp!</div>';
        document.getElementById('stat-steps').innerText = "-";
        document.getElementById('stat-nodes').innerText = result.nodes.toLocaleString();
        document.getElementById('stat-time').innerText = result.time + "ms";
        document.getElementById('stat-depth').innerText = "-";
        renderBoard(start_state);
        document.getElementById('step-wrapper').innerHTML = `<span style="background:#dc2626; color:white; padding:4px 12px; border-radius:6px; font-size:12px; font-weight:600; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">No Solution</span>`;
    }
}

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
        width=1200, 
        height=800, 
        resizable=True
    )
    webview.start()