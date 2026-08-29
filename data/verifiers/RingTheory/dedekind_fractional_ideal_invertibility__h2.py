import sympy as sp
from sympy.abc import x, y, z, t, u, v, w
from functools import reduce

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "In an integral domain, every non-zero fractional ideal is invertible."
    (The missing hypothesis is that R is a Dedekind domain).
    
    The witness is expected to be a list or tuple of SymPy expressions representing
    the generators of a fractional ideal I in the polynomial ring R = QQ[vars],
    where vars are the free symbols in the expressions.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) == 0:
            return [False, False, False]
        
        witness_exprs = [sp.sympify(w_expr) for w_expr in witness]
        
        vars_set = set()
        for expr in witness_exprs:
            vars_set.update(expr.free_symbols)
        vars = sorted(list(vars_set), key=lambda sym: sym.name)
        
        nums = []
        denoms = []
        for expr in witness_exprs:
            n, d = sp.fraction(sp.cancel(expr))
            # Check if the generator is a valid rational function in QQ(vars)
            if not n.is_polynomial(*vars) or not d.is_polynomial(*vars):
                return [False, False, False]
            nums.append(n)
            denoms.append(d)
            
        # H_1: R is an integral domain
        # R is implicitly QQ[vars]. Polynomial rings over fields are always integral domains.
        h1_ok = True
        
        # H_2: I is a non-zero fractional ideal of R
        # It is non-zero if at least one generator is non-zero.
        is_nonzero = any(sp.cancel(expr) != 0 for expr in witness_exprs)
        h2_ok = is_nonzero
        
        # ¬Q: I is not an invertible fractional ideal
        # In a UFD like QQ[vars], a fractional ideal is invertible iff it is principal.
        # We bring all generators to a common denominator, then check if the numerator ideal is principal.
        # The numerator ideal is principal iff dividing by the GCD of the generators yields the unit ideal.
        common_denom = reduce(sp.lcm, denoms)
        scaled_nums = [sp.cancel(expr * common_denom) for expr in witness_exprs]
        
        d = reduce(sp.gcd, scaled_nums)
        if d == 0:
            is_invertible = False
        else:
            core_gens = [sp.cancel(sn / d) for sn in scaled_nums]
            if not vars:
                # Over QQ, any non-zero ideal is the unit ideal (hence principal and invertible)
                is_invertible = True
            else:
                gb = sp.groebner(core_gens, *vars, domain='QQ')
                # The ideal is the unit ideal iff the reduced Groebner basis is [1]
                is_invertible = (len(gb) == 1 and sp.cancel(gb[0] - 1) == 0)
                
        neg_q_ok = not is_invertible
        
        return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: I is a non-zero fractional ideal of R",
    "¬Q: I is not an invertible fractional ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2