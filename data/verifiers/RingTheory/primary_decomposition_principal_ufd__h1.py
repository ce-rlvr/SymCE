import sympy as sp

def conditions(witness):
    """
    Verifies that the given witness is a counterexample to the conjecture.
    
    The witness must be an object with the following attributes:
      - vars: a tuple or list of sympy symbols (e.g., sp.symbols('P X Y'))
      - I: a list of sympy polynomials generating the quotient ideal
      - a: a sympy polynomial representing the element a
      - u: a sympy polynomial representing the unit u
      - factors: a list of tuples (p_i, e_i) where p_i is a sympy polynomial and e_i is an int
      - non_primary_witness: a tuple (idx, x, y) providing a counterexample to the primality 
                             of the ideal (p_idx^{e_idx}). Specifically, x*y in (p^e), 
                             y not in (p), and x not in (p^e).
    """
    try:
        vars_syms = witness.vars
        I = witness.I
        a = witness.a
        u = witness.u
        factors = witness.factors
        idx, x, y = witness.non_primary_witness
        
        # Compute base Groebner basis for the quotient ring
        G = list(sp.groebner(I, *vars_syms))
        
        # H1: a is a non-zero, non-unit element of R
        rem_a = sp.reduced(a, G, vars_syms)[1]
        h1_nonzero = (rem_a != 0)
        
        G_a = list(sp.groebner(I + [a], *vars_syms))
        h1_nonunit = (sp.reduced(1, G_a, vars_syms)[1] != 0)
        
        h1 = h1_nonzero and h1_nonunit
        
        # H2: a = u * p_1^{e_1} ... p_k^{e_k} is the prime factorization
        prod = u
        for p, e in factors:
            prod *= p**e
            
        h2_eq = (sp.reduced(sp.expand(a - prod), G, vars_syms)[1] == 0)
        
        G_u = list(sp.groebner(I + [u], *vars_syms))
        h2_u = (sp.reduced(1, G_u, vars_syms)[1] == 0)
        
        h2_e = all(e > 0 for p, e in factors)
        
        # Verify that p_i are pairwise non-associated
        h2_nonassoc = True
        for i in range(len(factors)):
            for j in range(i+1, len(factors)):
                p_i = factors[i][0]
                p_j = factors[j][0]
                G_pi = list(sp.groebner(I + [p_i], *vars_syms))
                G_pj = list(sp.groebner(I + [p_j], *vars_syms))
                in_j = (sp.reduced(p_i, G_pj, vars_syms)[1] == 0)
                in_i = (sp.reduced(p_j, G_pi, vars_syms)[1] == 0)
                if in_i and in_j:
                    h2_nonassoc = False
                    
        h2 = h2_eq and h2_u and h2_e and h2_nonassoc
        
        # ¬Q: The intersection is NOT the irredundant primary decomposition.
        # We prove this by showing that one of the components (p_i^{e_i}) is NOT a primary ideal.
        # If a component is not primary, the intersection cannot be a primary decomposition.
        p, e = factors[idx]
        
        G_pe = list(sp.groebner(I + [sp.expand(p**e)], *vars_syms))
        G_p = list(sp.groebner(I + [p], *vars_syms))
        
        # x * y \in (p^e)
        cond1 = (sp.reduced(sp.expand(x * y), G_pe, vars_syms)[1] == 0)
        # y \notin (p)
        cond2 = (sp.reduced(y, G_p, vars_syms)[1] != 0)
        # x \notin (p^e)
        cond3 = (sp.reduced(x, G_pe, vars_syms)[1] != 0)
        
        neg_q = cond1 and cond2 and cond3
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: a is a non-zero, non-unit element of R",
    "H_2: a = u p_1^{e_1} ... p_k^{e_k} is the prime factorization",
    "¬Q: The intersection is not the irredundant primary decomposition"
]

N_HYP = 2
NEG_Q_INDEX = 2