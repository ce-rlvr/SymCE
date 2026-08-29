import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.polys.numberfields import primitive_element

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

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K and L are finite Galois extensions of F",
    "H_3: The intersection K \\cap L is equal to F",
    "¬Q: Gal(KL/F) is not isomorphic to Gal(K/F) \\times Gal(L/F)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    # Try group-theoretic witness first
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, H_K, H_L = witness
            # Verify it's a group witness by accessing group methods
            _ = G.order()
            _ = H_K.is_normal(G)
            
            h1 = True
            h2 = bool(H_K.is_normal(G) and H_L.is_normal(G))
            
            H_KL = PermutationGroup(list(H_K.generators) + list(H_L.generators))
            h3 = bool(H_KL.order() == G.order())
            
            elements_K = set(H_K.generate())
            elements_L = set(H_L.generate())
            int_elements = elements_K.intersection(elements_L)
            order_int = len(int_elements)
            
            order_Gal_KL = G.order() // order_int
            order_Gal_K = G.order() // H_K.order()
            order_Gal_L = G.order() // H_L.order()
            
            neg_q = bool(order_Gal_KL != order_Gal_K * order_Gal_L)
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # Try polynomial witness (extensions of Q)
    x = sympy.Symbol('x')
    try:
        p_expr, q_expr = witness
        p = sympy.Poly(p_expr, x, domain='QQ')
        q = sympy.Poly(q_expr, x, domain='QQ')
    except Exception:
        return [False, False, False, False]

    try:
        h1 = True
    except Exception:
        h1 = False

    try:
        def is_galois(poly):
            if not poly.is_irreducible:
                return False
            deg = poly.degree()
            if deg == 1:
                return True
            r = sympy.RootOf(poly, 0)
            factors = sympy.factor_list(poly, extension=r)
            for fac, mult in factors[1]:
                if fac.degree() != 1:
                    return False
            return True
        
        h2 = bool(is_galois(p) and is_galois(q))
    except Exception:
        h2 = False

    try:
        r_q = sympy.RootOf(q, 0)
        factors_p = sympy.factor_list(p, extension=r_q)
        # K \cap L = Q iff p is irreducible over Q(root of q) (assuming Galois)
        h3 = bool(len(factors_p[1]) == 1 and factors_p[1][0][1] == 1)
    except Exception:
        h3 = False

    try:
        def aut_group_size(poly):
            if poly.degree() <= 0:
                return 1
            r = sympy.RootOf(poly, 0)
            factors = sympy.factor_list(poly, extension=r)
            return sum(1 for fac, mult in factors[1] if fac.degree() == 1)
        
        size_K = aut_group_size(p)
        size_L = aut_group_size(q)
        
        comp_poly = primitive_element([p.as_expr(), q.as_expr()], x)
        comp_poly = sympy.Poly(comp_poly, x, domain='QQ')
        size_KL = aut_group_size(comp_poly)
        
        neg_q = bool(size_KL != size_K * size_L)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]