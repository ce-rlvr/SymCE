import sympy
from sympy import QQ, Poly, factor_list, simplify, roots
from sympy.abc import x
import sympy.combinatorics.named_groups
import sympy.matrices

Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a polynomial over F",
    "H_3: K is the splitting field of f over F",
    "¬Q: K is not the splitting field of f**m over F"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    # Extract witness components
    if isinstance(witness, tuple):
        if len(witness) == 4:
            F, f, K, m = witness
        elif len(witness) == 2:
            f, m = witness
            F = QQ
            try:
                rts = roots(f, x)
                K = list(rts.keys())
            except Exception:
                K = []
        else:
            return [False, False, False, False]
    elif isinstance(witness, dict):
        F = witness.get('F', QQ)
        f = witness.get('f', None)
        K = witness.get('K', None)
        m = witness.get('m', None)
        if f is None or m is None:
            return [False, False, False, False]
        if K is None:
            try:
                rts = roots(f, x)
                K = list(rts.keys())
            except Exception:
                K = []
    else:
        return [False, False, False, False]

    # Normalize K to a list of extension expressions
    try:
        if F == QQ and K == QQ:
            K_exprs = []
        elif isinstance(K, (list, tuple)):
            K_exprs = list(K)
        elif hasattr(K, 'ext'):
            K_exprs = [K.ext]
        elif hasattr(K, 'gens'):
            K_exprs = list(K.gens)
        else:
            K_exprs = [K]
    except Exception:
        K_exprs = []

    # H1: F is a field
    try:
        h1 = False
        if hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
        elif hasattr(F, 'is_RationalField') and F.is_RationalField:
            h1 = True
        elif F == QQ:
            h1 = True
    except Exception:
        h1 = False

    # H2: f(x) is a polynomial in F
    try:
        p = Poly(f, x)
        if F == QQ:
            h2 = p.domain.is_RationalField or p.domain.is_IntegerRing
        else:
            h2 = True
    except Exception:
        h2 = False

    # H3: K is the splitting field of f(x) over F
    try:
        if not K_exprs:
            facs = factor_list(f)
            splits = all(Poly(fac, x).degree() <= 1 for fac, mult in facs[1])
            h3 = splits
        else:
            facs = factor_list(f, extension=K_exprs)
            splits = all(Poly(fac, x).degree() <= 1 for fac, mult in facs[1])
            
            roots_f = roots(f, x)
            k_are_roots = True
            for k in K_exprs:
                if not any(simplify(k - r) == 0 for r in roots_f):
                    k_are_roots = False
                    break
            h3 = splits and k_are_roots
    except Exception:
        h3 = False

    # neg_Q: K is NOT the splitting field of (f(x))^m over F
    try:
        if m < 0:
            if Poly(f, x).degree() > 0:
                neg_q = True
            else:
                neg_q = False
        else:
            g = f**m
            try:
                pg = Poly(g, x)
                is_poly = True
            except Exception:
                is_poly = False
                
            if not is_poly:
                neg_q = True
            else:
                if pg.degree() == 0:
                    if F == QQ:
                        K_in_F = all(getattr(k, 'is_rational', False) == True for k in K_exprs)
                    else:
                        K_in_F = True
                    is_split_g = K_in_F
                else:
                    if not K_exprs:
                        facs_g = factor_list(g)
                        splits_g = all(Poly(fac, x).degree() <= 1 for fac, mult in facs_g[1])
                        is_split_g = splits_g
                    else:
                        facs_g = factor_list(g, extension=K_exprs)
                        splits_g = all(Poly(fac, x).degree() <= 1 for fac, mult in facs_g[1])
                        roots_g = roots(g, x)
                        k_are_roots_g = True
                        for k in K_exprs:
                            if not any(simplify(k - r) == 0 for r in roots_g):
                                k_are_roots_g = False
                                break
                        is_split_g = splits_g and k_are_roots_g
                    
                neg_q = not is_split_g
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]