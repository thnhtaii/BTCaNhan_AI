import time
import random

# Player definitions:
# 0 = empty
# 1 = Player X (Human)
# 2 = Player O (AI)

def check_winner(board):
    # Winning combinations (3x3 grid indices)
    win_combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # columns
        [0, 4, 8], [2, 4, 6]             # diagonals
    ]
    for combo in win_combos:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != 0:
            return board[combo[0]] # Returns 1 or 2
    if 0 not in board:
        return 0 # Draw
    return None # Game not finished

def get_legal_moves(board):
    return [i for i in range(9) if board[i] == 0]

def make_move(board, idx, player):
    new_board = list(board)
    new_board[idx] = player
    return new_board

# --- MINIMAX ---
def minimax_search(board):
    nodes_generated = 0
    
    def max_value(state, depth):
        nonlocal nodes_generated
        nodes_generated += 1
        
        winner = check_winner(state)
        if winner == 2: return 10 - depth
        if winner == 1: return -10 + depth
        if winner == 0: return 0
        
        v = -float('inf')
        for move in get_legal_moves(state):
            v = max(v, min_value(make_move(state, move, 2), depth + 1))
        return v

    def min_value(state, depth):
        nonlocal nodes_generated
        nodes_generated += 1
        
        winner = check_winner(state)
        if winner == 2: return 10 - depth
        if winner == 1: return -10 + depth
        if winner == 0: return 0
        
        v = float('inf')
        for move in get_legal_moves(state):
            v = min(v, max_value(make_move(state, move, 1), depth + 1))
        return v

    # Root call (AI O's turn)
    legal = get_legal_moves(board)
    if not legal:
        return None, 0
        
    best_move = None
    best_val = -float('inf')
    
    for move in legal:
        val = min_value(make_move(board, move, 2), 1)
        if val > best_val:
            best_val = val
            best_move = move
            
    return best_move, nodes_generated


# --- ALPHA-BETA ---
def alpha_beta_search(board):
    nodes_generated = 0
    
    def max_value(state, alpha, beta, depth):
        nonlocal nodes_generated
        nodes_generated += 1
        
        winner = check_winner(state)
        if winner == 2: return 10 - depth
        if winner == 1: return -10 + depth
        if winner == 0: return 0
        
        v = -float('inf')
        for move in get_legal_moves(state):
            v = max(v, min_value(make_move(state, move, 2), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        nonlocal nodes_generated
        nodes_generated += 1
        
        winner = check_winner(state)
        if winner == 2: return 10 - depth
        if winner == 1: return -10 + depth
        if winner == 0: return 0
        
        v = float('inf')
        for move in get_legal_moves(state):
            v = min(v, max_value(make_move(state, move, 1), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    legal = get_legal_moves(board)
    if not legal:
        return None, 0
        
    best_move = None
    best_val = -float('inf')
    alpha = -float('inf')
    beta = float('inf')
    
    for move in legal:
        val = min_value(make_move(board, move, 2), alpha, beta, 1)
        if val > best_val:
            best_val = val
            best_move = move
        alpha = max(alpha, best_val)
        
    return best_move, nodes_generated


# --- EXPECTIMAX ---
def expectimax_search(board):
    nodes_generated = 0
    
    def max_value(state, depth):
        nonlocal nodes_generated
        nodes_generated += 1
        
        winner = check_winner(state)
        if winner == 2: return 10 - depth
        if winner == 1: return -10 + depth
        if winner == 0: return 0
        
        v = -float('inf')
        for move in get_legal_moves(state):
            v = max(v, exp_value(make_move(state, move, 2), depth + 1))
        return v

    def exp_value(state, depth):
        nonlocal nodes_generated
        nodes_generated += 1
        
        winner = check_winner(state)
        if winner == 2: return 10 - depth
        if winner == 1: return -10 + depth
        if winner == 0: return 0
        
        legal = get_legal_moves(state)
        if not legal:
            return 0
            
        total_val = 0
        for move in legal:
            total_val += max_value(make_move(state, move, 1), depth + 1)
        return total_val / len(legal)

    legal = get_legal_moves(board)
    if not legal:
        return None, 0
        
    best_move = None
    best_val = -float('inf')
    
    for move in legal:
        val = exp_value(make_move(board, move, 2), 1)
        if val > best_val:
            best_val = val
            best_move = move
            
    return best_move, nodes_generated

# Solve dispatcher for the API
def adversarial_solve(board, algorithm='minimax'):
    t0 = time.time()
    
    # 1. Identify current winner
    initial_winner = check_winner(board)
    if initial_winner is not None:
        elapsed = int((time.time() - t0) * 1000)
        return {
            "success": True,
            "game_over": True,
            "winner": initial_winner,
            "board": board,
            "move": None,
            "nodes": 0,
            "time": elapsed
        }
        
    # 2. Select algorithm
    if algorithm == 'minimax':
        best_move, nodes = minimax_search(board)
    elif algorithm == 'alpha_beta':
        best_move, nodes = alpha_beta_search(board)
    elif algorithm == 'expectimax':
        best_move, nodes = expectimax_search(board)
    else:
        best_move, nodes = minimax_search(board)
        
    elapsed = int((time.time() - t0) * 1000)
    
    if best_move is not None:
        new_board = make_move(board, best_move, 2) # AI places O
        winner = check_winner(new_board)
        return {
            "success": True,
            "game_over": winner is not None,
            "winner": winner,
            "board": new_board,
            "move": best_move,
            "nodes": nodes,
            "time": elapsed
        }
    else:
        return {
            "success": False,
            "game_over": True,
            "winner": 0,
            "board": board,
            "move": None,
            "nodes": nodes,
            "time": elapsed
        }
