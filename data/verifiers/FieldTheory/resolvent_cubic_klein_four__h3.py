import sympy
from sympy import Poly, Symbol, Rational, sqrt
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup
x = Symbol('x')

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(
    Permutation(0, 1)(2, 3),
    Permutation(0, 2)(1, 3),
    Permutation(0, 3)(1, 2)
)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    # Extract witness
    R = None
    G = None
    f = None
    
    if isinstance(witness, dict):
        f = witness.get('f')
        G = witness.get('G')
        R = witness.get('R')
    else:
        try:
            groups = []
            for item in witness:
                if isinstance(item, PermutationGroup):
                    groups.append(item)
                else:
                    try:
                        p = Poly(item, x)
                        if p.degree() == 4:
                            f = item
                        elif p.degree() == 3:
                            R = item
                    except Exception:
                        pass
            if groups:
                G = groups[-1]
        except Exception:
            pass

    # H1: K is a field of characteristic not equal to 2 or 3.
    try:
        poly_f = Poly(f, x, domain='QQ')
        h1 = True
    except Exception:
        h1 = False

    # H2: f(x) is an irreducible separable quartic polynomial.
    try:
        if poly_f.degree() == 4 and poly_f.is_irreducible and poly_f.is_sqf:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: V is the Klein four-group...
    h3 = True

    # H4: R(x) is the resolvent cubic of f(x).
    try:
        coeffs = poly_f.all_coeffs()
        if len(coeffs) == 5:
            a4, a3, a2, a1, a0 = coeffs
            a = a3 / a4
            b = a2 / a4
            c = a1 / a4
            d = a0 / a4
            
            # Common definitions of the resolvent cubic
            R_std1 = x**3 - b*x**2 + (a*c - 4*d)*x - a**2*d + 4*b*d - c**2
            R_std2 = x**3 - 2*b*x**2 + (b**2 + a*c - 4*d)*x + c**2 - a*b*c + a**2*d
            R_std3 = x**3 + 2*b*x**2 + (b**2 + a*c - 4*d)*x - c**2 + a*b*c - a**2*d
            
            if R is None:
                R = R_std1
                h4 = True
            else:
                poly_R = Poly(R, x, domain='QQ')
                poly_R_std1 = Poly(R_std1, x, domain='QQ')
                poly_R_std2 = Poly(R_std2, x, domain='QQ')
                poly_R_std3 = Poly(R_std3, x, domain='QQ')
                
                if poly_R.degree() == 3 and (
                    poly_R.monic() == poly_R_std1.monic() or 
                    poly_R.monic() == poly_R_std2.monic() or
                    poly_R.monic() == poly_R_std3.monic()
                ):
                    h4 = True
                else:
                    h4 = False
        else:
            h4 = False
    except Exception:
        h4 = False

    # Neg_Q: The Galois group of R(x) over K is NOT isomorphic to G / (G \cap V).
    try:
        poly_R = Poly(R, x, domain='QQ')
        factors = poly_R.factor_list()[1]
        degrees = sorted([fac[0].degree() for fac in factors])
        
        if degrees == [1, 1, 1]:
            galois_order = 1
        elif degrees == [1, 2]:
            galois_order = 2
        elif degrees == [3]:
            disc = poly_R.discriminant()
            if sqrt(disc).is_rational:
                galois_order = 3
            else:
                galois_order = 6
        else:
            galois_order = -1
            
        V = PermutationGroup(
            Permutation(0, 1)(2, 3), 
            Permutation(0, 2)(1, 3), 
            Permutation(0, 3)(1, 2)
        )
        elements_G = list(G.generate())
        elements_V = list(V.generate())
        
        def eval_perm(p, i):
            return p(i) if i < p.size else i

        intersection = []
        for g in elements_G:
            # To be in V, g must not move any element >= 4
            if any(eval_perm(g, i) != i for i in range(4, g.size)):
                continue
            for v in elements_V:
                if all(eval_perm(g, i) == eval_perm(v, i) for i in range(4)):
                    intersection.append(g)
                    break
                    
        quotient_order = len(elements_G) // len(intersection)
        
        if galois_order != -1 and galois_order != quotient_order:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field of characteristic not equal to 2 or 3",
    "H_2: f(x) is an irreducible separable quartic polynomial",
    "H_3: V is the Klein four-group",
    "H_4: R(x) is the resolvent cubic of f(x)",
    "¬Q: The Galois group of R(x) over K is NOT isomorphic to G / (G \\cap V)"
]

N_HYP = 4
NEG_Q_INDEX = 4