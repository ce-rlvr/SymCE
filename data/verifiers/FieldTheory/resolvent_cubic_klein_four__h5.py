import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.matrices import eye, zeros
import math

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(3), Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3), Permutation(0, 3)(1, 2))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_galois_group_order_QQ(poly_R, x):
    factors = sympy.factor_list(poly_R)
    degs = sorted([f.degree() for f, m in factors[1]])
    if not degs:
        return 1
    if sum(degs) == 1:
        return 1
    if sum(degs) == 2:
        if degs == [2]:
            return 2
        return 1
    if sum(degs) == 3:
        if degs == [3]:
            disc = sympy.discriminant(poly_R.as_expr(), x)
            if sympy.sqrt(disc).is_rational:
                return 3
            else:
                return 6
        elif degs == [1, 2]:
            return 2
        else:
            return 1
    if sum(degs) == 4:
        if degs == [4]:
            R_expr = poly_R.as_expr()
            R_monic = sympy.Poly(R_expr, x).monic()
            coeffs = R_monic.all_coeffs()
            a, b, c, d = coeffs[1], coeffs[2], coeffs[3], coeffs[4]
            R_R = x**3 - b*x**2 + (a*c - 4*d)*x - a**2 * d + 4*b*d - c**2
            R_R_poly = sympy.Poly(R_R, x)
            R_R_factors = sympy.factor_list(R_R_poly)
            R_R_degs = sorted([f.degree() for f, m in R_R_factors[1]])
            if R_R_degs == [3]:
                disc = sympy.discriminant(R_expr, x)
                if sympy.sqrt(disc).is_rational:
                    return 12
                else:
                    return 24
            elif R_R_degs == [1, 1, 1]:
                return 4
            elif R_R_degs == [1, 2]:
                return 8
        elif degs == [1, 3]:
            f3 = [f for f, m in factors[1] if f.degree() == 3][0]
            disc = sympy.discriminant(f3.as_expr(), x)
            if sympy.sqrt(disc).is_rational:
                return 3
            else:
                return 6
        elif degs == [2, 2]:
            f1, f2 = [f for f, m in factors[1] if f.degree() == 2]
            d1 = sympy.discriminant(f1.as_expr(), x)
            d2 = sympy.discriminant(f2.as_expr(), x)
            if sympy.sqrt(d1 * d2).is_rational:
                return 2
            else:
                return 4
        elif degs == [1, 1, 2]:
            return 2
        else:
            return 1
    return -1

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 5:
            K, f, G, V, R = witness
        else:
            return [False, False, False, False, False]
    except Exception:
        return [False, False, False, False, False]

    try:
        if K == sympy.QQ:
            h1 = True
        elif isinstance(K, int) and sympy.isprime(K) and K not in (2, 3):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        x = sympy.Symbol('x')
        if K == sympy.QQ:
            poly_f = sympy.Poly(f, x, domain='QQ')
            h2 = poly_f.degree() == 4 and poly_f.is_irreducible and sympy.discriminant(f, x) != 0
        elif isinstance(K, int):
            poly_f = sympy.Poly(f, x, domain=sympy.GF(K))
            h2 = poly_f.degree() == 4 and poly_f.is_irreducible and sympy.discriminant(f, x) % K != 0
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        x = sympy.Symbol('x')
        if K == sympy.QQ:
            expected_order = get_galois_group_order_QQ(sympy.Poly(f, x, domain='QQ'), x)
            h3 = isinstance(G, PermutationGroup) and G.order() == expected_order
        elif isinstance(K, int):
            h3 = isinstance(G, PermutationGroup) and G.order() == 4
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        if isinstance(V, PermutationGroup) and V.order() == 4:
            is_v4 = True
            for g in V.elements:
                if g.order() == 1:
                    continue
                cycles = g.cyclic_form
                if len(cycles) == 2 and len(cycles[0]) == 2 and len(cycles[1]) == 2:
                    continue
                is_v4 = False
            h4 = is_v4
        else:
            h4 = False
    except Exception:
        h4 = False

    try:
        x = sympy.Symbol('x')
        int_V = [g for g in G.elements if g in V.elements]
        quotient_order = G.order() // len(int_V)
        
        if K == sympy.QQ:
            poly_R = sympy.Poly(R, x, domain='QQ')
            gal_R_order = get_galois_group_order_QQ(poly_R, x)
            neg_q = (gal_R_order != quotient_order)
        elif isinstance(K, int):
            poly_R = sympy.Poly(R, x, domain=sympy.GF(K))
            factors = sympy.factor_list(poly_R)
            degs = [f.degree() for f, m in factors[1]]
            if not degs:
                gal_R_order = 1
            else:
                gal_R_order = math.lcm(*degs)
            neg_q = (gal_R_order != quotient_order)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field of characteristic not equal to 2 or 3",
    "H_2: f(x) is an irreducible separable quartic polynomial over K",
    "H_3: G is the Galois group of f(x) over K viewed as a subgroup of S4",
    "H_4: V is the Klein four-group viewed as the normal subgroup of S4",
    "not Q: The Galois group of R(x) over K is NOT isomorphic to G / (G intersection V)"
]

N_HYP = 4
NEG_Q_INDEX = 4