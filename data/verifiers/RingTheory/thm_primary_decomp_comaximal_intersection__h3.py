import sympy
from sympy.abc import x, y, z

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: Q_1, ..., Q_n are primary ideals of R",
    "¬Q: The intersection of Q_i is not equal to their product"
]

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "The intersection of primary ideals is equal to their product."
    
    The witness should be a list of generators for the ideals Q_i.
    We support ideals in Z (list of integers) or in Q[x] (list of single-variable polynomials).
    """
    h1_ok = False
    h2_ok = False
    neg_q_ok = False
    
    # H_1: R is a commutative ring
    # We verify the witness represents ideals in a supported PID (Z or Q[x])
    try:
        if isinstance(witness, (list, tuple)) and len(witness) >= 1:
            exprs = [sympy.sympify(q) for q in witness]
            
            if all(q.is_Integer for q in exprs):
                h1_ok = True
            else:
                symbols = set()
                for e in exprs:
                    if isinstance(e, sympy.Expr):
                        symbols.update(e.free_symbols)
                if len(symbols) <= 1 and all(isinstance(e, sympy.Expr) for e in exprs):
                    h1_ok = True
    except Exception:
        pass

    # H_2: Q_1, ..., Q_n are primary ideals of R
    try:
        if h1_ok:
            h2_ok = True
            exprs = [sympy.sympify(q) for q in witness]
            for q in exprs:
                if q.is_Integer:
                    val = abs(int(q))
                    if val == 1:
                        h2_ok = False
                        break
                    if val > 1:
                        # In Z, an ideal (m) is primary iff m = p^k for some prime p
                        if len(sympy.factorint(val)) != 1:
                            h2_ok = False
                            break
                else:
                    if q == 0:
                        continue
                    # In Q[x], units (non-zero constants) generate the whole ring, not a proper ideal
                    if q.is_number:
                        h2_ok = False
                        break
                    # In Q[x], an ideal (f) is primary iff f = p^k for some irreducible p
                    factors = sympy.factor_list(q)
                    if len(factors[1]) != 1:
                        h2_ok = False
                        break
    except Exception:
        h2_ok = False

    # ¬Q: The intersection of Q_i is not equal to their product
    try:
        if h1_ok:
            exprs = [sympy.sympify(q) for q in witness]
            if all(q.is_Integer for q in exprs):
                vals = [abs(int(q)) for q in exprs]
                lcm_val = 1
                for v in vals:
                    lcm_val = sympy.lcm(lcm_val, v)
                prod_val = 1
                for v in vals:
                    prod_val *= v
                neg_q_ok = (lcm_val != prod_val)
            else:
                lcm_val = sympy.S.One
                for e in exprs:
                    lcm_val = sympy.lcm(lcm_val, e)
                prod_val = sympy.S.One
                for e in exprs:
                    prod_val *= e
                
                if prod_val == 0:
                    neg_q_ok = (lcm_val != 0)
                else:
                    # Check if they generate the same ideal (i.e., differ by a unit/constant)
                    q_div = sympy.cancel(lcm_val / prod_val)
                    if not q_div.is_number:
                        neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]