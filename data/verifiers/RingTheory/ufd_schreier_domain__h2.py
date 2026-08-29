import sympy
from sympy import symbols, ZZ, QQ, Tuple
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            R, a, b, c = witness
        elif len(witness) == 3:
            a, b, c = witness
            syms = set()
            for obj in (a, b, c):
                if hasattr(obj, 'free_symbols'):
                    syms.update(obj.free_symbols)
            if syms:
                R = ZZ.poly_ring(*syms)
            else:
                R = ZZ
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: R is a unique factorization domain
    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    def is_ideal(obj):
        return isinstance(obj, (list, tuple, set, Tuple))

    def ideal_contains(I_gens, J_gens):
        try:
            I = R.ideal(*I_gens)
            return all(I.contains(g) for g in J_gens)
        except Exception:
            return False

    def divides(div, val):
        if is_ideal(div) and is_ideal(val):
            return ideal_contains(div, val)
        if div == 0:
            return val == 0
        try:
            q, r = R.div(val, div)
            return r == 0
        except Exception:
            pass
        try:
            R.exquo(val, div)
            return True
        except Exception:
            pass
        try:
            return sympy.simplify(val / div).is_polynomial()
        except Exception:
            return False

    # H2: a divides bc
    try:
        if is_ideal(a) and is_ideal(b) and is_ideal(c):
            bc = []
            for gb in b:
                for gc in c:
                    bc.append(gb * gc)
            h2 = divides(a, bc)
        else:
            if hasattr(R, 'mul'):
                bc = R.mul(b, c)
            else:
                bc = b * c
            h2 = divides(a, bc)
    except Exception:
        h2 = False

    # neg_Q: NOT (exists a1, a2 in R such that a = a1*a2, a1|b, a2|c)
    try:
        q_holds = False
        if is_ideal(a):
            # If a is an ideal, it cannot be written as a product of two elements
            # unless it is principal. The conclusion specifically asks for elements.
            q_holds = False
        else:
            # Try GCD approach (works for elements in any UFD)
            try:
                g = R.gcd(a, b)
                a2 = R.exquo(a, g)
                if divides(g, b) and divides(a2, c):
                    q_holds = True
            except Exception:
                pass
            
            # Fallback to checking all divisors if GCD approach fails
            if not q_holds:
                try:
                    from sympy import divisors
                    for a1 in divisors(a):
                        try:
                            if hasattr(R, 'exquo'):
                                a2 = R.exquo(a, R(a1))
                            else:
                                a2 = a / a1
                            if divides(a1, b) and divides(a2, c):
                                q_holds = True
                                break
                        except Exception:
                            pass
                except Exception:
                    pass
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a divides the product bc",
    "¬Q: There do not exist elements a1, a2 in R such that a = a1 a2, a1 divides b, and a2 divides c"
]

N_HYP = 2
NEG_Q_INDEX = 2