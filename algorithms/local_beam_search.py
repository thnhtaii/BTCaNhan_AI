import time
import random

def get_successors(mt):
    pos = mt.index(0)
    r, c = pos // 3, pos % 3
    successors = []
    def swap(mt, i, j):
        new_mt = list(mt)
        new_mt[i], new_mt[j] = new_mt[j], new_mt[i]
        return new_mt, new_mt[i]
    if c > 0: 
        new_state, cost = swap(mt, pos, pos - 1)
        successors.append(("Trái", new_state, cost))
    if c < 2: 
        new_state, cost = swap(mt, pos, pos + 1)
        successors.append(("Phải", new_state, cost))
    if r > 0: 
        new_state, cost = swap(mt, pos, pos - 3)
        successors.append(("Lên", new_state, cost))
    if r < 2: 
        new_state, cost = swap(mt, pos, pos + 3)
        successors.append(("Xuống", new_state, cost))
    return successors

def count_manhattan(mt, goal):
    dist = 0
    for i in range(9):
        val = mt[i]
        if val != 0:
            r, c = i // 3, i % 3
            goal_idx = goal.index(val)
            gr, gc = goal_idx // 3, goal_idx % 3
            dist += abs(r - gr) + abs(c - gc)
    return dist

def state_to_tuple(state):
    return tuple(state)

def local_beam_search_solve(start_state, goal_state, k=3, max_steps=500):
    """
    Heuristic: Manhattan
    """
    log_data = []
    def h(state): return count_manhattan(state, goal_state)
    h_label = "Manhattan"
    nodes_generated = 1
    start_h = h(start_state)
    beam = [(list(start_state), start_h, [])]
    log_data.append({"step": 0, "action_html": f"Khởi tạo beam ban đầu với k = {k}<br>Trạng thái bắt đầu: h({h_label}) = {start_h}", "frontier_str": f"Beam size: 1, Best h = {start_h}", "reached_str": f"k = {k}"})
    visited = {state_to_tuple(start_state)}
    for iteration in range(1, max_steps + 1):
        for state, state_h, path in beam:
            if state == goal_state:
                log_data.append({"step": iteration, "action_html": f"Trạng thái trong beam trùng khớp với Goal!<br>THUẬT TOÁN DỪNG VÀ TRẢ VỀ THÀNH CÔNG", "frontier_str": "Đã đạt đích!", "reached_str": f"Thành công sau {iteration - 1} bước lặp!"})
                return path, nodes_generated, log_data
        all_candidates = []
        action_html = f"<b>Bước lặp {iteration}</b> - Beam hiện tại có {len(beam)} trạng thái:<br>"
        for beam_idx, (current_state, current_h, current_path) in enumerate(beam):
            action_html += f"<br>Beam[{beam_idx + 1}]: h = {current_h}<br>"
            successors = get_successors(current_state)
            for action, child, _ in successors:
                child_tuple = state_to_tuple(child)
                if child_tuple not in visited:
                    child_h = h(child)
                    nodes_generated += 1
                    new_path = current_path + [(action, child)]
                    all_candidates.append((child, child_h, new_path, beam_idx, action))
                    action_html += f"  - {action}: h = {child_h}<br>"
                else:
                    action_html += f"  - {action}: <span style='color:#7f7f7f;'>Đã thăm</span><br>"
        if not all_candidates:
            action_html += f"<br><b style='color: #d62728;'>Không có trạng thái lân cận mới nào!</b><br>"
            action_html += f"<b>THUẬT TOÁN DỪNG - KHÔNG TÌM ĐƯỢC LỜI GIẢI</b>"
            log_data.append({"step": iteration, "action_html": action_html, "frontier_str": "Hết trạng thái mới!", "reached_str": "Thất bại!"})
            best_in_beam = min(beam, key=lambda x: x[1])
            return best_in_beam[2], nodes_generated, log_data
        all_candidates.sort(key=lambda x: x[1])
        selected = []
        selected_tuples = set()
        for cand in all_candidates:
            cand_tuple = state_to_tuple(cand[0])
            if cand_tuple not in selected_tuples:
                selected.append(cand)
                selected_tuples.add(cand_tuple)
                if len(selected) >= k:
                    break
        best_current_h = min(s[1] for s in beam)
        best_new_h = selected[0][1] if selected else float('inf')
        action_html += f"<br>Tổng cộng {len(all_candidates)} trạng thái lân cận mới.<br>"
        action_html += f"<b>Chọn {len(selected)} trạng thái tốt nhất</b> cho beam mới:<br>"
        for i, (s, sh, sp, si, sa) in enumerate(selected):
            action_html += f"  Beam[{i+1}]: h = {sh} (từ Beam[{si+1}] → {sa})<br>"
        log_data.append({"step": iteration, "action_html": action_html, "frontier_str": f"Best h: {best_current_h} → {best_new_h}", "reached_str": f"Beam size: {len(selected)}, Nodes: {nodes_generated}"})
        beam = [(s, sh, sp) for s, sh, sp, si, sa in selected]
        for s, sh, sp in beam:
            visited.add(state_to_tuple(s))
    fail_html = f"<b style='color: #c53030;'>Đã hết {max_steps} bước lặp mà chưa tìm ra lời giải!</b><br>"
    fail_html += f"<b>THUẬT TOÁN DỪNG</b>"
    log_data.append({"step": "KQ", "action_html": fail_html, "frontier_str": "Hết bước lặp!", "reached_str": f"Nodes: {nodes_generated}"})
    best_in_beam = min(beam, key=lambda x: x[1])
    return best_in_beam[2], nodes_generated, log_data
