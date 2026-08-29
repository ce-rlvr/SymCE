import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Symbol, Poly

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    h1, h2, h3, h4, neg_q = False, False, False, False, False

    def get(name):
        if isinstance(witness, dict) and name in witness:
            return witness[name]
        if hasattr(witness, name):
            return getattr(witness, name)
        return None

    try:
        h1_val = get('h1')
        if h1_val is not None:
            h1 = bool(h1_val)
        else:
            n = get('n')
            if n is not None:
                h1 = (int(n) == n) and (n > 0)
    except Exception:
        h1 = False

    try:
        h2_val = get('h2')
        if h2_val is not None:
            h2 = bool(h2_val)
        else:
            zeta = get('zeta')
            n = get('n')
            K = get('K')
            if zeta is not None and n is not None:
                is_root = (zeta**int(n) == 1)
                is_primitive = True
                for k in range(1, int(n)):
                    if zeta**k == 1:
                        is_primitive = False
                        break
                if is_root and is_primitive:
                    if K is not None and hasattr(K, 'contains'):
                        h2 = bool(K.contains(zeta))
                    else:
                        h2 = True
    except Exception:
        h2 = False

    try:
        h3_val = get('h3')
        if h3_val is not None:
            h3 = bool(h3_val)
        else:
            a = get('a')
            n = get('n')
            K = get('K')
            if a is not None and n is not None and K is not None:
                x = Symbol('x')
                poly = Poly(x**int(n) - a, x, domain=K)
                h3 = bool(poly.is_irreducible)
    except Exception:
        h3 = False

    try:
        h4_val = get('h4')
        if h4_val is not None:
            h4 = bool(h4_val)
        else:
            is_split = get('is_splitting_field')
            if is_split is not None:
                h4 = bool(is_split)
            else:
                L = get('L')
                if L is not None and hasattr(L, 'is_splitting_field'):
                    h4 = bool(L.is_splitting_field)
    except Exception:
        h4 = False

    try:
        q_val = get('q')
        if q_val is not None:
            neg_q = not bool(q_val)
        else:
            conclusion_val = get('conclusion')
            if conclusion_val is not None:
                neg_q = not bool(conclusion_val)
            else:
                Gal = get('Gal')
                n = get('n')
                if Gal is not None and n is not None:
                    is_cyclic = get('is_cyclic')
                    if is_cyclic is None:
                        if hasattr(Gal, 'is_isomorphic'):
                            is_cyclic = Gal.is_isomorphic(CyclicGroup(int(n)))
                        else:
                            is_cyclic = False
                    
                    sigma = get('sigma')
                    alpha = get('alpha')
                    zeta = get('zeta')
                    maps_correctly = False
                    if sigma is not None and alpha is not None and zeta is not None:
                        if callable(sigma):
                            maps_correctly = (sigma(alpha) == zeta * alpha)
                        elif isinstance(sigma, dict):
                            maps_correctly = (sigma.get(alpha) == zeta * alpha)
                    
                    neg_q = not (is_cyclic and maps_correctly)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: K contains a primitive n-th root of unity zeta",
    "H_3: a in K and x^n - a is irreducible over K",
    "H_4: L is the splitting field of x^n - a over K",
    "¬Q: The Galois group is not isomorphic to Z/nZ"
]

N_HYP = 4
NEG_Q_INDEX = 4