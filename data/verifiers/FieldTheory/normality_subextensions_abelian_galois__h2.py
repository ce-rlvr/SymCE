import sympy
from sympy import Symbol, Poly, RootOf, factor_list
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    # 1. Try group witness (Galois correspondence)
    # Witness is (G, H) where G = Gal(L/K) and H = Gal(L/M)
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2 and isinstance(witness[0], PermutationGroup):
            G, H = witness
            h1 = True  # G is a valid group representing a Galois extension
            h2 = H.is_subgroup(G)
            
            def is_normal_subgroup(G, H):
                if hasattr(G, 'is_normal'):
                    return G.is_normal(H)
                for g in G.generators:
                    for h in H.generators:
                        if (g * h * ~g) not in H:
                            return False
                return True
                
            neg_q = not is_normal_subgroup(G, H)
            return [h1, bool(h2), bool(neg_q)]
    except Exception:
        pass

    # 2. Try polynomial witness
    # Witness is (f, g) or (f, g, roots_f, root_g)
    # f represents L = Q[x]/(f), g represents M = Q[x]/(g)
    x = Symbol('x')
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 4:
            f_expr, g_expr, roots_f_expr, root_g_expr = witness
            f = Poly(f_expr, x, domain='QQ')
            g = Poly(g_expr, x, domain='QQ')
            
            if not f.is_irreducible or not g.is_irreducible:
                return [False, False, False]
                
            roots_f = [Poly(r, x, domain='QQ') for r in roots_f_expr]
            root_g = Poly(root_g_expr, x, domain='QQ')
            
            h1_2 = len(roots_f) == f.degree()
            h1_3 = all((f.compose(r) % f).is_zero for r in roots_f)
            h1_4 = True
            for i in range(len(roots_f)):
                for j in range(i + 1, len(roots_f)):
                    if ((roots_f[i] - roots_f[j]) % f).is_zero:
                        h1_4 = False
                        break
            h1 = bool(h1_2 and h1_3 and h1_4)
            
            h2 = bool((g.compose(root_g) % f).is_zero)
            
            r = RootOf(g.as_expr(), 0)
            factors = factor_list(g.as_expr(), extension=r)[1]
            neg_q = len(factors) < g.degree()
            
            return [h1, h2, neg_q]
            
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            f_expr, g_expr = witness
            f = Poly(f_expr, x, domain='QQ')
            g = Poly(g_expr, x, domain='QQ')
            
            if not f.is_irreducible or not g.is_irreducible:
                return [False, False, False]
                
            r_f = RootOf(f.as_expr(), 0)
            factors_f = factor_list(f.as_expr(), extension=r_f)[1]
            h1 = len(factors_f) == f.degree()
            
            factors_g = factor_list(g.as_expr(), extension=r_f)[1]
            h2 = any(fac[0].degree() == 1 for fac in factors_g)
            
            r_g = RootOf(g.as_expr(), 0)
            factors_g_self = factor_list(g.as_expr(), extension=r_g)[1]
            neg_q = len(factors_g_self) < g.degree()
            
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: L/K is a Galois extension",
    "H_2: M is an intermediate field such that K <= M <= L",
    "¬Q: The extension M/K is not a Galois extension"
]

N_HYP = 2
NEG_Q_INDEX = 2