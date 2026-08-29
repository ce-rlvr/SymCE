import sympy
from sympy.abc import x
import math

# Top-level setup
# (No specific named objects required for this domain)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The false conjecture incorrectly assumes that the trace map Tr_{L/K}(alpha) 
    is given by the sum_{i=0}^{[L:K]-1} alpha^{q^i}, forgetting that the base 
    field for the extension L/K has size |K| = q^m, not q.
    
    Expected witness format: (q, m, n, alpha)
    where:
      - q is the size of the base field F_q (must be a prime power)
      - m is the degree of K / F_q
      - n is the degree of L / K
      - alpha is an element of L (can be a symbolic expression like x)
    """
    try:
        if len(witness) != 4:
            return [False, False, False, False]
            
        q, m, n, alpha = witness
        
        # H_1: K is a finite field extension of F_q
        try:
            q_val = int(q)
            factors = sympy.ntheory.factorint(q_val)
            h1 = (len(factors) == 1)
            p = list(factors.keys())[0]
        except Exception:
            h1 = False
            p = 2
            q_val = 2
            
        try:
            if hasattr(m, 'degree'):
                m_val = int(m.degree())
            else:
                m_val = int(m)
            if m_val < 1:
                h1 = False
        except Exception:
            h1 = False
            m_val = 1
            
        # H_2: L is a finite field extension of K
        try:
            if hasattr(n, 'degree'):
                n_val = int(n.degree())
            else:
                n_val = int(n)
            h2 = (n_val >= 1)
        except Exception:
            h2 = False
            n_val = 1
            
        # H_3: alpha is an element of L
        h3 = True
        
        # Prevent DOS from huge exponents
        if m_val * n_val > 100:
            return [False, False, False, False]
            
        alpha_expr = sympy.sympify(alpha)
        if isinstance(alpha_expr, sympy.Poly):
            alpha_expr = alpha_expr.as_expr()
            
        # The false conjecture evaluates the trace using the base q instead of |K|
        def wrong_trace(degree, base_q, val):
            return sum(val**(base_q**i) for i in range(degree))
            
        tr_L_Fq = wrong_trace(m_val * n_val, q_val, alpha_expr)
        tr_L_K = wrong_trace(n_val, q_val, alpha_expr)
        tr_K_Fq = wrong_trace(m_val, q_val, tr_L_K)
        
        free_syms = alpha_expr.free_symbols
        sym = list(free_syms)[0] if free_syms else x
        
        # ¬Q: Tr_{L/F_q}(alpha) != Tr_{K/F_q}(Tr_{L/K}(alpha))
        try:
            poly1 = sympy.Poly(sympy.expand(tr_L_Fq), sym, domain=sympy.GF(p))
            poly2 = sympy.Poly(sympy.expand(tr_K_Fq), sym, domain=sympy.GF(p))
            neg_q = (poly1 != poly2)
        except Exception:
            diff = sympy.simplify(tr_L_Fq - tr_K_Fq)
            if diff == 0:
                neg_q = False
            else:
                try:
                    neg_q = (int(diff) % p != 0)
                except Exception:
                    neg_q = True

        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: K is a finite field extension of F_q",
    "H_2: L is a finite field extension of K",
    "H_3: alpha is an element of L",
    "¬Q: Tr_{L/F_q}(alpha) != Tr_{K/F_q}(Tr_{L/K}(alpha))"
]

N_HYP = 3
NEG_Q_INDEX = 3