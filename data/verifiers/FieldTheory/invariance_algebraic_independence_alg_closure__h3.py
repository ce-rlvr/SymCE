import sympy
from sympy import Symbol, Rational, Integer
from sympy.abc import x, y, z, t, u, v, w

def conditions(witness) -> list[bool]:
    # Check if witness provides direct boolean attributes/methods
    try:
        if hasattr(witness, 'h1') and hasattr(witness, 'h2') and hasattr(witness, 'neg_q'):
            h1 = witness.h1() if callable(witness.h1) else witness.h1
            h2 = witness.h2() if callable(witness.h2) else witness.h2
            neg_q = witness.neg_q() if callable(witness.neg_q) else witness.neg_q
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    try:
        # Unpack witness
        if hasattr(witness, 'K'):
            K = witness.K
            L = witness.L
            K_bar = witness.K_bar
            S = witness.S
        else:
            K, L, K_bar, S = witness
            
        # Convert to lists
        K = list(K)
        L = list(L)
        K_bar = list(K_bar)
        S = list(S)
        
        def get_syms(gens):
            syms = set()
            for g in gens:
                if hasattr(g, 'free_symbols'):
                    syms.update(g.free_symbols)
            return syms
            
        def is_alg_over(expr, K_gens):
            if not hasattr(expr, 'free_symbols') or not expr.free_symbols:
                return True
            K_syms = get_syms(K_gens)
            return expr.free_symbols.issubset(K_syms)
            
        def is_alg_indep(S_gens, K_gens):
            K_syms = get_syms(K_gens)
            S_syms = get_syms(S_gens)
            if any(not hasattr(s, 'free_symbols') or not s.free_symbols for s in S_gens):
                return False
            new_syms = S_syms - K_syms
            return len(new_syms) >= len(S_gens)

        L_syms = get_syms(L)
        K_bar_syms = get_syms(K_bar)
        S_syms = get_syms(S)
        
        # H1: L is a field extension of K
        h1 = True
        for g in K:
            if hasattr(g, 'free_symbols') and g.free_symbols:
                if not g.free_symbols.issubset(L_syms):
                    h1 = False
                    
        # H2: K_bar is the algebraic closure of K within L
        h2 = True
        for g in K:
            if hasattr(g, 'free_symbols') and g.free_symbols:
                if not g.free_symbols.issubset(K_bar_syms):
                    h2 = False
        for g in K_bar:
            if hasattr(g, 'free_symbols') and g.free_symbols:
                if not g.free_symbols.issubset(L_syms):
                    h2 = False
            if not is_alg_over(g, K):
                h2 = False
        for g in L:
            if is_alg_over(g, K):
                if hasattr(g, 'free_symbols') and g.free_symbols:
                    if not g.free_symbols.issubset(K_bar_syms):
                        h2 = False
                        
        # Conclusion: S is algebraically independent over K iff S is algebraically independent over K_bar
        indep_K = is_alg_indep(S, K)
        
        # If S is not a subset of L, it cannot be evaluated over K_bar (which is defined within L)
        # This captures the dropped hypothesis "S is a subset of L"
        if not S_syms.issubset(L_syms):
            indep_K_bar = False
        else:
            indep_K_bar = is_alg_indep(S, K_bar)
            
        neg_q = not (indep_K == indep_K_bar)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: L is a field extension of K",
    "H_2: K_bar is the algebraic closure of K within L",
    "¬Q: S is algebraically independent over K if and only if S is algebraically independent over K_bar fails"
]

N_HYP = 2
NEG_Q_INDEX = 2