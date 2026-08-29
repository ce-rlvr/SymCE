import sympy
from sympy import symbols, Poly, groebner, reduced
from sympy import gcd as sympy_gcd
import itertools
import math
from sympy.abc import x, y, z, t

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "For non-zero elements a, b in a ring R, the gcd exists and can be written as ax + by."
    
    A valid witness is a tuple (a, b) of elements in a ring (e.g., ZZ[x] or QQ[x, y])
    where the gcd cannot be written as a linear combination of a and b.
    """
    try:
        if len(witness) != 2:
            return [False, False]
        a = sympy.sympify(witness[0])
        b = sympy.sympify(witness[1])
    except Exception:
        return [False, False]

    # H_1: a and b are non-zero elements of R
    try:
        a_zero = sympy.simplify(a) == 0
        b_zero = sympy.simplify(b) == 0
        h1_ok = bool(not a_zero and not b_zero)
    except Exception:
        h1_ok = False

    # neg_Q: The greatest common divisor of a and b cannot be written as ax + by
    try:
        g = sympy_gcd(a, b)
        
        gens_set = set()
        if hasattr(a, 'free_symbols'):
            gens_set.update(a.free_symbols)
        if hasattr(b, 'free_symbols'):
            gens_set.update(b.free_symbols)
        gens = sorted(list(gens_set), key=lambda sym: sym.name)

        if not gens:
            # Constants (no variables)
            try:
                if a.is_Integer and b.is_Integer:
                    av = int(a)
                    bv = int(b)
                    gv = int(g)
                    d = math.gcd(av, bv)
                    if d == 0:
                        in_ideal = (gv == 0)
                    else:
                        in_ideal = (gv % d == 0)
                else:
                    # For fields, any non-zero element generates the whole ring
                    if a != 0 or b != 0:
                        in_ideal = True
                    else:
                        in_ideal = (g == 0)
            except Exception:
                in_ideal = False
        else:
            # Polynomials
            try:
                pa = Poly(a, *gens)
                pb = Poly(b, *gens)
                is_zz = pa.domain.is_ZZ and pb.domain.is_ZZ
            except Exception:
                is_zz = False

            in_ideal = True
            
            # Fast path: evaluate at small integer points to prove non-membership
            if len(gens) <= 3:
                vals = [-2, -1, 0, 1, 2]
            elif len(gens) <= 5:
                vals = [-1, 0, 1]
            else:
                vals = [0, 1]
            points_to_test = list(itertools.product(vals, repeat=len(gens)))
            
            for pt in points_to_test:
                subs_dict = dict(zip(gens, pt))
                try:
                    av = a.subs(subs_dict)
                    bv = b.subs(subs_dict)
                    gv = g.subs(subs_dict)
                    
                    if is_zz:
                        av_int = int(av)
                        bv_int = int(bv)
                        gv_int = int(gv)
                        d = math.gcd(av_int, bv_int)
                        if d == 0:
                            if gv_int != 0:
                                in_ideal = False
                                break
                        else:
                            if gv_int % d != 0:
                                in_ideal = False
                                break
                    else:
                        if av == 0 and bv == 0 and gv != 0:
                            in_ideal = False
                            break
                except Exception:
                    pass

            # Fallback to Groebner basis if point evaluation didn't rule it out
            if in_ideal:
                try:
                    domain = 'ZZ' if is_zz else 'QQ'
                    gb = groebner([a, b], *gens, domain=domain)
                    rem = reduced(g, gb, *gens, domain=domain)[1]
                    if rem != 0:
                        in_ideal = False
                except Exception:
                    pass

        neg_q_ok = not in_ideal
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a and b are non-zero elements of R",
    "¬Q: The greatest common divisor of a and b cannot be written as ax + by"
]

N_HYP = 1
NEG_Q_INDEX = 1