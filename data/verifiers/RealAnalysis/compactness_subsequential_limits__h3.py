import sympy as sp
import math
import itertools
import functools

# Top-level setup
n = sp.Symbol('n', integer=True, positive=True)

def check_H1(witness):
    n_sym = sp.Symbol('n', integer=True, positive=True)
    if isinstance(witness, sp.Expr):
        for i in range(1, 21):
            try:
                val = witness.subs(n_sym, i).evalf()
                if not val.is_real:
                    return False
            except Exception:
                return False
        return True
    elif callable(witness):
        for i in range(1, 21):
            try:
                val = witness(i)
                if isinstance(val, (int, float)):
                    continue
                elif isinstance(val, complex):
                    if val.imag != 0:
                        return False
                elif hasattr(val, 'is_real'):
                    if not val.is_real:
                        return False
                else:
                    return False
            except Exception:
                return False
        return True
    elif isinstance(witness, (int, float)):
        return True
    return False

def check_bounded(witness):
    n_sym = sp.Symbol('n', integer=True, positive=True)
    if isinstance(witness, sp.Expr):
        try:
            L = sp.limit(sp.Abs(witness), n_sym, sp.oo)
            if L == sp.oo:
                return False
            if L.is_number and L < sp.oo:
                return True
        except Exception:
            pass
            
        evaluated_any = False
        for exp in [2, 3, 4, 10, 100, 1000]:
            try:
                val = abs(float(witness.subs(n_sym, 10**exp)))
                evaluated_any = True
                if val > 1e5:
                    return False
            except Exception:
                pass
        return evaluated_any

    elif callable(witness):
        evaluated_any = False
        for exp in [2, 3, 4, 10, 100, 1000, 10000]:
            try:
                val = abs(float(witness(10**exp)))
                evaluated_any = True
                if val > 1e5:
                    return False
            except Exception:
                pass
        return evaluated_any
        
    elif isinstance(witness, (int, float)):
        return True
        
    return False

def check_neg_Q(witness):
    if check_bounded(witness):
        return False
        
    n_sym = sp.Symbol('n', integer=True, positive=True)
    if isinstance(witness, sp.Expr):
        try:
            L = sp.limit(witness, n_sym, sp.oo)
            if L == sp.oo or L == -sp.oo:
                return True
        except Exception:
            pass
            
    vals = []
    if isinstance(witness, sp.Expr):
        for i in range(1, 10001):
            try:
                vals.append(float(witness.subs(n_sym, i)))
            except Exception:
                pass
    elif callable(witness):
        for i in range(1, 10001):
            try:
                vals.append(float(witness(i)))
            except Exception:
                pass
    elif isinstance(witness, (int, float)):
        return False
                
    if len(vals) >= 100:
        num_blocks = 10
        block_size = len(vals) // num_blocks
        blocks = [vals[i*block_size:(i+1)*block_size] for i in range(num_blocks)]
        min_blocks = [min(b) for b in blocks]
        max_blocks = [max(b) for b in blocks]
        
        if all(min_blocks[i] <= min_blocks[i+1] for i in range(num_blocks-1)) and min_blocks[-1] > 10:
            return True
        if all(max_blocks[i] >= max_blocks[i+1] for i in range(num_blocks-1)) and max_blocks[-1] < -10:
            return True
            
        if all(min_blocks[i] >= min_blocks[i+1] for i in range(num_blocks-1)) and min_blocks[-1] < -10:
            if all(max_blocks[i] <= max_blocks[i+1] for i in range(num_blocks-1)) and max_blocks[-1] > 10:
                return True
                
        cluster_candidates = set()
        for i in range(num_blocks):
            block_rounded = set(round(v, 1) for v in blocks[i])
            if i == 0:
                cluster_candidates = block_rounded
            else:
                cluster_candidates = cluster_candidates.intersection(block_rounded)
                
        if not cluster_candidates:
            return True
            
        if max(cluster_candidates) - min(cluster_candidates) > 1000:
            return True
            
    return False

def conditions(witness):
    try:
        h1 = check_H1(witness)
    except Exception:
        h1 = False
        
    try:
        h2 = check_bounded(witness)
    except Exception:
        h2 = False
        
    try:
        neg_q = check_neg_Q(witness)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (x_n) is a sequence of real numbers",
    "H_2: (x_n) is bounded",
    "¬Q: E is not a non-empty and compact subset of R"
]

N_HYP = 2
NEG_Q_INDEX = 2