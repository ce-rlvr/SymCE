import sympy
from sympy import Poly, roots, degree, factor, Mul, simplify, QQ
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def conditions(witness):
    # H_1: F is a field
    try:
        F = witness.get("F")
        h1 = hasattr(F, "is_Field") and F.is_Field
    except Exception:
        h1 = False

    # H_2: S is a finite set of polynomials over F
    try:
        F = witness.get("F")
        S = witness.get("S")
        if not isinstance(S, (list, tuple, set)):
            h2 = False
        else:
            h2 = True
            for p in S:
                Poly(p, x, domain=F)
    except Exception:
        h2 = False

    # H_3: g is the product of the polynomials in S
    try:
        S = witness.get("S")
        g = witness.get("g")
        if S is None or g is None:
            h3 = False
        else:
            prod = 1
            for p in S:
                prod *= p
            h3 = simplify(g - prod) == 0
    except Exception:
        h3 = False

    # H_4: E_1 is a splitting field of the set S over F
    try:
        F = witness.get("F")
        S = witness.get("S")
        E1_minpoly = witness.get("E1_minpoly")
        
        h4 = False
        if F == QQ:
            if Poly(E1_minpoly, x, domain="QQ").is_irreducible:
                R = []
                valid_roots = True
                for p in S:
                    rts = roots(p, x)
                    if sum(rts.values()) != degree(p, x):
                        valid_roots = False
                        break
                    R.extend(rts.keys())
                
                if valid_roots:
                    R = list(set(R))
                    if not R:
                        split_deg = 1
                    else:
                        from sympy.polys.numberfields import primitive_element
                        minp, _ = primitive_element(R, x)
                        split_deg = degree(minp, x)
                        
                    if degree(E1_minpoly, x) == split_deg:
                        E_roots = roots(E1_minpoly, x)
                        if E_roots:
                            E_root = list(E_roots.keys())[0]
                            splits_completely = True
                            for p in S:
                                fac = factor(p, extension=E_root)
                                factors = fac.args if isinstance(fac, Mul) else [fac]
                                for f in factors:
                                    if f.has(x) and degree(f, x) > 1:
                                        splits_completely = False
                                        break
                                if not splits_completely:
                                    break
                            if splits_completely:
                                h4 = True
    except Exception:
        h4 = False

    # neg_Q: E_1 and E_2 are not isomorphic over F
    try:
        E1_minpoly = witness.get("E1_minpoly")
        E2_minpoly = witness.get("E2_minpoly")
        
        neg_q = False
        if E1_minpoly is not None and E2_minpoly is not None:
            if degree(E1_minpoly, x) != degree(E2_minpoly, x):
                neg_q = True
            else:
                try:
                    from sympy.polys.numberfields import field_isomorphism
                    if field_isomorphism(E1_minpoly, E2_minpoly) is None:
                        neg_q = True
                except Exception:
                    r1 = roots(E1_minpoly, x)
                    if r1:
                        r1 = list(r1.keys())[0]
                        fac = factor(E2_minpoly, extension=r1)
                        factors = fac.args if isinstance(fac, Mul) else [fac]
                        has_linear = False
                        for f in factors:
                            if f.has(x) and degree(f, x) == 1:
                                has_linear = True
                                break
                        if not has_linear:
                            neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: S is a finite set of polynomials over F",
    "H_3: g is the product of the polynomials in S",
    "H_4: E_1 is a splitting field of the set S over F",
    "neg_Q: E_1 and E_2 are not isomorphic over F"
]

N_HYP = 4
NEG_Q_INDEX = 4