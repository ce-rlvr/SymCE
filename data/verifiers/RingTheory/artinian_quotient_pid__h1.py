import sympy
from sympy import symbols, poly, groebner, QQ, ZZ

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the false conjecture:
    "Let I be a non-zero proper ideal of R. Then the quotient ring R/I is an Artinian ring."
    
    The witness should ideally be a tuple (vars, I_gens) where vars is a tuple of variables
    defining the polynomial ring R = QQ[vars], and I_gens is a list of polynomials generating I.
    """
    try:
        # Parse witness
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[1], (list, tuple)):
            vars, I_gens = witness
            if not isinstance(vars, (list, tuple)):
                vars = (vars,)
        else:
            I_gens = witness if isinstance(witness, (list, tuple)) else [witness]
            vars = tuple(set().union(*(sympy.sympify(p).free_symbols for p in I_gens)))
            if not vars:
                vars = (x,)
    except Exception:
        return [False, False]
        
    # H_1: I is a non-zero proper ideal of R
    try:
        gb = groebner(I_gens, *vars, domain='QQ', order='lex')
        gb_polys = list(gb)
        
        # Check if I is the zero ideal
        is_zero = all(poly(p, *vars, domain='QQ', order='lex').is_zero for p in gb_polys)
        
        # Check if I is the whole ring (i.e., not proper)
        is_proper = True
        for p in gb_polys:
            p_poly = poly(p, *vars, domain='QQ', order='lex')
            if p_poly.is_constant() and not p_poly.is_zero:
                is_proper = False
                break
                
        h1_ok = bool((not is_zero) and is_proper)
    except Exception:
        h1_ok = False
        
    # ¬Q: The quotient ring R/I is not an Artinian ring
    # R/I is Artinian iff I is a zero-dimensional ideal.
    # An ideal is zero-dimensional iff its Groebner basis contains a polynomial 
    # with a pure power leading monomial for each variable.
    try:
        if not h1_ok:
            neg_q = False
        else:
            is_zero_dim = True
            for v in vars:
                found = False
                for p in gb_polys:
                    p_poly = poly(p, *vars, domain='QQ', order='lex')
                    if p_poly.is_zero:
                        continue
                    lm = p_poly.monoms()[0]
                    v_idx = vars.index(v)
                    # Check if the leading monomial is a pure power of v
                    if lm[v_idx] > 0 and all(lm[i] == 0 for i in range(len(vars)) if i != v_idx):
                        found = True
                        break
                if not found:
                    is_zero_dim = False
                    break
            
            neg_q = not is_zero_dim
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: I is a non-zero proper ideal of R",
    "¬Q: The quotient ring R/I is not an Artinian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1