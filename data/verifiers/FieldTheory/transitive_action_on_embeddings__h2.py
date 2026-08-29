import sympy as sp
from sympy import factor_list, degree, RootOf
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group theory and linear algebra objects
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: E/F is a finite Galois extension",
    "¬Q: Gal(E/F) does not act transitively on Hom_F(K, E)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Given a witness (E_poly, K_poly) representing the field E = QQ[x]/(E_poly)
    and the F-algebra K = QQ[x]/(K_poly) where F = QQ, checks if E/F is Galois
    and whether Gal(E/F) fails to act transitively on Hom_F(K, E).
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
            
        E_expr, K_expr = witness
        
        E_expr = sp.sympify(E_expr)
        K_expr = sp.sympify(K_expr)
        
        free_symbols = E_expr.free_symbols | K_expr.free_symbols
        if len(free_symbols) > 1:
            return [False, False]
        var = list(free_symbols)[0] if free_symbols else x
        
        # H1: E/F is a finite Galois extension
        # E is represented as QQ[var]/(E_expr)
        facs = factor_list(E_expr)
        if len(facs[1]) != 1 or facs[1][0][1] != 1:
            h1 = False
        else:
            if degree(E_expr, var) == 1:
                h1 = True
            else:
                theta = RootOf(E_expr, 0)
                facs_ext = factor_list(E_expr, extension=theta)[1]
                h1 = True
                for fac, mult in facs_ext:
                    if degree(fac, var) != 1:
                        h1 = False
                        break
                        
        # neg_Q: Gal(E/F) does NOT act transitively on Hom_F(K, E)
        # K is represented as QQ[var]/(K_expr)
        # The number of orbits of Gal(E/F) on Hom_F(K, E) equals the number of 
        # distinct irreducible factors of K_expr over QQ that have at least one root in E.
        facs_K = factor_list(K_expr)[1]
        irreducible_factors = [fac for fac, mult in facs_K]
        
        orbits = 0
        if degree(E_expr, var) == 1:
            for g in irreducible_factors:
                if degree(g, var) == 1:
                    orbits += 1
        else:
            theta = RootOf(E_expr, 0)
            for g in irreducible_factors:
                if degree(g, var) == 1:
                    orbits += 1
                else:
                    g_facs = factor_list(g, extension=theta)[1]
                    has_root = False
                    for fac, mult in g_facs:
                        if degree(fac, var) == 1:
                            has_root = True
                            break
                    if has_root:
                        orbits += 1
                        
        # The action is transitive iff there is exactly 1 orbit.
        # If orbits == 0 (empty set) or orbits > 1, it is not transitive.
        neg_q = (orbits != 1)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]