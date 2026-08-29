import sympy
from sympy import groebner, Tuple
from sympy.abc import x, y, z

# Top-level setup for witness expressions
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    """
    Given a witness (R, a, b), check if it is a valid counterexample to the conjecture.
    H1: R is a principal ideal domain
    H2: The greatest common divisor of a and b is a unit
    neg_Q: The ideal sum <a> + <b> is NOT equal to the entire ring R
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        R, a, b = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a principal ideal domain
    try:
        h1 = bool(getattr(R, 'is_PID', False))
    except Exception:
        h1 = False

    # H_2: The greatest common divisor of a and b is a unit
    try:
        g = R.gcd(a, b)
        # In a SymPy domain, an element is a unit if 1 is exactly divisible by it
        R.exquo(R.one, g)
        h2 = True
    except Exception:
        h2 = False

    # neg_Q: The ideal sum <a> + <b> is NOT equal to the entire ring R
    try:
        if getattr(R, 'is_PID', False):
            # In a PID, <a> + <b> == R if and only if gcd(a, b) is a unit
            g_val = R.gcd(a, b)
            try:
                R.exquo(R.one, g_val)
                is_R = True
            except Exception:
                is_R = False
        else:
            # Fallback for non-PIDs (e.g. ZZ[x], QQ[x, y])
            expr_a = a.as_expr() if hasattr(a, 'as_expr') else sympy.sympify(a)
            expr_b = b.as_expr() if hasattr(b, 'as_expr') else sympy.sympify(b)
            gens = R.gens if hasattr(R, 'gens') else []
            
            if not gens:
                free_symbols = Tuple(expr_a, expr_b).free_symbols
                gens = list(free_symbols)
            
            if gens:
                dom = getattr(R, 'dom', None)
                if dom is None:
                    if R == sympy.ZZ or getattr(R, 'is_IntegerRing', False):
                        dom = sympy.ZZ
                    else:
                        dom = sympy.QQ
                
                is_R = None
                # For univariate polynomials, we can use the resultant
                if len(gens) == 1:
                    try:
                        res = sympy.resultant(expr_a, expr_b, gens[0])
                        res_dom = dom.from_sympy(res)
                        try:
                            dom.exquo(dom.one, res_dom)
                            is_R = True
                        except Exception:
                            is_R = False
                    except Exception:
                        pass # Fallback to Groebner basis if resultant fails
                
                # For multivariate polynomials or if resultant failed
                if is_R is None:
                    gb = groebner([expr_a, expr_b], *gens, domain=dom)
                    is_R = False
                    for p in gb:
                        if p == 1 or p == -1:
                            is_R = True
                            break
                        if hasattr(p, 'is_number') and p.is_number and p != 0:
                            try:
                                p_dom = dom.from_sympy(p)
                                dom.exquo(dom.one, p_dom)
                                is_R = True
                                break
                            except Exception:
                                pass
            else:
                # No generators, meaning they are constants
                g_val = R.gcd(a, b)
                try:
                    R.exquo(R.one, g_val)
                    is_R = True
                except Exception:
                    is_R = False

        neg_q = not is_R
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: The greatest common divisor of a and b is a unit",
    "¬Q: The ideal sum <a> + <b> is not equal to the entire ring R"
]

N_HYP = 2
NEG_Q_INDEX = 2