import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
import math

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, I) where R is a ring and I is an ideal 
    (represented by a list of generators or a single generator).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        elif hasattr(witness, 'R') and hasattr(witness, 'I'):
            R = witness.R
            I = witness.I
        elif witness in [ZZ, QQ] or hasattr(witness, 'is_Domain'):
            R = witness
            I = [1]
        elif isinstance(witness, int):
            R = ZZ
            I = [witness]
        elif isinstance(witness, list):
            R = ZZ
            I = witness
        else:
            R, I = None, None
    except Exception:
        R, I = None, None

    def is_commutative(ring):
        if ring in [ZZ, QQ]: return True
        if getattr(ring, 'is_commutative', False) or getattr(ring, 'is_Commutative', False): return True
        if hasattr(ring, 'domain'): return is_commutative(ring.domain)
        return False

    def is_noetherian(ring):
        if ring in [ZZ, QQ]: return True
        if getattr(ring, 'is_PID', False): return True
        if getattr(ring, 'is_Field', False): return True
        if hasattr(ring, 'domain'): return is_noetherian(ring.domain)
        return False

    def is_integral_domain(ring):
        if ring in [ZZ, QQ]: return True
        if getattr(ring, 'is_Domain', False) or getattr(ring, 'is_IntegralDomain', False): return True
        if getattr(ring, 'is_Field', False): return True
        if hasattr(ring, 'domain'): return is_integral_domain(ring.domain)
        return False

    # H_1: R is a commutative ring
    try:
        h1 = False
        if R is not None:
            h1 = is_commutative(R)
    except Exception:
        h1 = False

    # H_2: R is a Noetherian ring
    try:
        h2 = False
        if R is not None:
            h2 = is_noetherian(R)
    except Exception:
        h2 = False

    # H_3: R is an integral domain
    try:
        h3 = False
        if R is not None:
            h3 = is_integral_domain(R)
    except Exception:
        h3 = False

    # ¬Q: The intersection \bigcap_{n=1}^\infty I^n is not the zero ideal.
    # In a Noetherian integral domain, Krull's intersection theorem guarantees 
    # the intersection is zero for any proper ideal. Thus, the conclusion fails 
    # (intersection is non-zero) if and only if I is the whole ring R (i.e., I = R).
    try:
        neg_q = False
        if R is not None and I is not None:
            if isinstance(I, (list, tuple, set)):
                gens = list(I)
            else:
                gens = [I]
            
            if gens:
                # Check if 1 is explicitly in gens
                if any(g == 1 or (hasattr(R, 'one') and g == R.one) for g in gens):
                    neg_q = True
                elif R == ZZ:
                    g = 0
                    for elem in gens:
                        g = math.gcd(g, int(elem))
                    neg_q = (g == 1)
                elif R == QQ or getattr(R, 'is_Field', False):
                    neg_q = any(g != 0 for g in gens)
                else:
                    # Try Groebner basis for polynomial rings
                    try:
                        from sympy import groebner
                        if all(hasattr(g, 'free_symbols') for g in gens):
                            symbols = set()
                            for g in gens:
                                symbols.update(g.free_symbols)
                            if symbols:
                                dom = 'ZZ'
                                if hasattr(R, 'domain'):
                                    if R.domain == QQ: dom = 'QQ'
                                elif R == QQ:
                                    dom = 'QQ'
                                gb = groebner(gens, *list(symbols), domain=dom)
                                if len(gb) == 1 and gb[0] == 1:
                                    neg_q = True
                    except Exception:
                        pass
                    
                    # Fallback for PIDs
                    if not neg_q and getattr(R, 'is_PID', False):
                        try:
                            g = gens[0]
                            for elem in gens[1:]:
                                g = R.gcd(g, elem)
                            if hasattr(R, 'is_unit'):
                                neg_q = R.is_unit(g)
                            elif hasattr(R, 'rem'):
                                neg_q = (R.rem(R.one, g) == R.zero)
                        except Exception:
                            pass
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a Noetherian ring",
    "H_3: R is an integral domain",
    "¬Q: The intersection \\bigcap_{n=1}^\\infty I^n is not the zero ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3