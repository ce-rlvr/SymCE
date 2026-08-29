import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: g_k = k(3k-1)/2 is the k-th generalized pentagonal number",
    "¬Q: p(n) != sum_{k != 0} (-1)^{k-1} p(n - g_k)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    n = None
    p = None
    g = None
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                n, p = witness
            elif len(witness) == 3:
                n, p, g = witness
            elif len(witness) > 0:
                n = witness[0]
        elif isinstance(witness, dict):
            n = witness.get('n')
            p = witness.get('p')
            g = witness.get('g')
        else:
            n = witness
    except Exception:
        pass

    # H1: n is a positive integer
    try:
        h1 = (int(n) == n) and (int(n) > 0)
    except Exception:
        h1 = False

    # H2: g_k = k(3k-1)/2
    try:
        if not h1:
            n_int = 10
        else:
            n_int = int(n)
            
        if g is None:
            h2 = True
            g_func = lambda k: k * (3 * k - 1) // 2
        elif callable(g):
            h2 = all(g(k) == k * (3 * k - 1) // 2 for k in range(-n_int-2, n_int+3))
            g_func = g
        elif isinstance(g, dict):
            h2 = all(v == k * (3 * k - 1) // 2 for k, v in g.items())
            g_func = lambda k: g.get(k, k * (3 * k - 1) // 2)
        else:
            h2 = False
            g_func = lambda k: k * (3 * k - 1) // 2
    except Exception:
        h2 = False
        g_func = lambda k: k * (3 * k - 1) // 2

    # neg_Q: p(n) != sum_{k != 0} (-1)^{k-1} p(n - g_k)
    try:
        if not h1:
            return [h1, h2, False]
            
        n_int = int(n)
        
        if p is None:
            from sympy.ntheory import npartitions
            def p_func(m):
                if m < 0: return 0
                return npartitions(m)
        elif callable(p):
            def p_func(m):
                if m < 0: return 0
                return p(m)
        elif isinstance(p, (list, tuple)):
            def p_func(m):
                if m < 0: return 0
                if m < len(p): return p[m]
                return 0
        elif isinstance(p, dict):
            def p_func(m):
                if m < 0: return 0
                return p.get(m, 0)
        else:
            p_func = lambda m: 0
            
        lhs = p_func(n_int)
        
        rhs = 0
        
        # For positive k
        k = 1
        while True:
            gk = g_func(k)
            if gk > n_int:
                break
            term = (1 if (k - 1) % 2 == 0 else -1) * p_func(n_int - gk)
            rhs += term
            k += 1
            if k > n_int + 2:
                break
                
        # For negative k
        k = -1
        while True:
            gk = g_func(k)
            if gk > n_int:
                break
            term = (1 if (k - 1) % 2 == 0 else -1) * p_func(n_int - gk)
            rhs += term
            k -= 1
            if k < -n_int - 2:
                break
                
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]