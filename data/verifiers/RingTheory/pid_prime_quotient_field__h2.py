import sympy
import sympy.polys
import sympy.abc

# Top-level setup for potential witness objects
ZZ = sympy.polys.domains.ZZ
QQ = sympy.polys.domains.QQ
x = sympy.abc.x
QQ_x = QQ.poly_ring(x)
ZZ_x = ZZ.poly_ring(x)

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: The quotient ring R/(p) is not a field"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # Witness can be a tuple (R, p) or just p (defaulting R to ZZ)
        if isinstance(witness, tuple) and len(witness) == 2:
            R, p = witness
        else:
            R, p = ZZ, witness
    except Exception:
        return [False, False]

    # H_1: R is a principal ideal domain
    try:
        h1 = bool(getattr(R, 'is_PID', False))
    except Exception:
        h1 = False

    # ¬Q: The quotient ring R/(p) is NOT a field
    try:
        is_field = False
        
        if getattr(R, 'is_Field', False):
            # In a field, the only proper ideal is (0), and R/(0) is isomorphic to R (a field).
            is_field = (p == 0 or p == getattr(R, 'zero', 0))
        elif R == ZZ:
            # In ZZ, R/(p) is a field iff |p| is prime.
            try:
                val = abs(int(p))
                is_field = sympy.isprime(val)
            except Exception:
                is_field = False
        else:
            # Assume it's a polynomial ring over a field like QQ[x]
            if p == 0 or p == getattr(R, 'zero', 0):
                is_field = False
            else:
                try:
                    expr = sympy.sympify(p)
                    syms = list(expr.free_symbols)
                    if not syms:
                        # Non-zero constants are units, quotient is the zero ring (not a field)
                        is_field = False
                    else:
                        gen = syms[0]
                        if sympy.degree(expr, gen) <= 0:
                            is_field = False
                        else:
                            # In F[x], R/(p) is a field iff p is irreducible
                            factors = sympy.factor_list(expr)
                            # factor_list returns (content, [(factor1, mult1), ...])
                            if len(factors[1]) == 1 and factors[1][0][1] == 1:
                                is_field = True
                            else:
                                is_field = False
                except Exception:
                    is_field = False
                    
        neg_q = not is_field
    except Exception:
        neg_q = False

    return [h1, neg_q]