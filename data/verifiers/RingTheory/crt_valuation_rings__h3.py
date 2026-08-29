import sympy

# Standard Ring/Field bindings
QQ = sympy.QQ
ZZ = sympy.ZZ

class Z_p:
    """Localization of Z at a prime p. Represents a discrete valuation ring."""
    def __init__(self, p):
        self.p = p
        
    def is_valuation_ring(self):
        try:
            return sympy.isprime(int(self.p))
        except Exception:
            return False
        
    def is_ideal(self, gen):
        def is_int(g):
            return isinstance(g, int) or (hasattr(g, 'is_integer') and g.is_integer)
        
        if is_int(gen):
            return True
        if isinstance(gen, (tuple, list, set)):
            return all(is_int(g) for g in gen)
        return False
        
    def is_whole_ring(self, gen):
        if not self.is_ideal(gen):
            return False
        
        def is_unit(g):
            try:
                return int(g) % int(self.p) != 0
            except Exception:
                return False
            
        if isinstance(gen, (tuple, list, set)):
            return any(is_unit(g) for g in gen)
        return is_unit(gen)
        
    def __eq__(self, other):
        return isinstance(other, Z_p) and self.p == other.p
        
    def __str__(self):
        return f"Z_({self.p})"


def conditions(witness) -> list[bool]:
    try:
        R, I, J = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: R is a valuation ring
    try:
        if hasattr(R, 'is_valuation_ring'):
            h1 = bool(R.is_valuation_ring())
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: I is an ideal of R
    try:
        if hasattr(R, 'is_ideal'):
            h2 = bool(R.is_ideal(I))
        elif hasattr(I, 'is_ideal'):
            h2 = bool(I.is_ideal())
        elif hasattr(R, 'is_Field') and R.is_Field:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: J is an ideal of R
    try:
        if hasattr(R, 'is_ideal'):
            h3 = bool(R.is_ideal(J))
        elif hasattr(J, 'is_ideal'):
            h3 = bool(J.is_ideal())
        elif hasattr(R, 'is_Field') and R.is_Field:
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # NegQ: Neither I nor J is the whole ring R
    try:
        def is_whole_ring(ideal, ring):
            if hasattr(ring, 'is_whole_ring'):
                return bool(ring.is_whole_ring(ideal))
            if hasattr(ideal, 'is_whole_ring'):
                return bool(ideal.is_whole_ring())
            if hasattr(ring, 'is_Field') and ring.is_Field:
                if isinstance(ideal, (list, tuple, set)):
                    return any(g != 0 for g in ideal)
                return ideal != 0
            return False
        
        neg_q = (not is_whole_ring(I, R)) and (not is_whole_ring(J, R))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]


CONDITION_LABELS = [
    "H_1: R is a valuation ring",
    "H_2: I is an ideal of R",
    "H_3: J is an ideal of R",
    "¬Q: Neither I nor J is the whole ring R"
]

N_HYP = 3
NEG_Q_INDEX = 3