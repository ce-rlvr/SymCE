import sympy
from sympy import Matrix, eye, zeros, Poly, Symbol
from sympy.abc import x

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_rational(val):
    if isinstance(val, (int, float)):
        return True
    return getattr(val, 'is_Rational', False) == True

def conditions(witness) -> list[bool]:
    # H_1: V is a finite-dimensional vector space over F, T is a linear operator
    try:
        T = witness["T"]
        if not isinstance(T, Matrix):
            h1 = False
        elif T.rows != T.cols:
            h1 = False
        elif T.rows < 1:
            h1 = False
        elif not all(is_rational(val) for val in T):
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    # H_2: The polynomials p_1(x), ..., p_k(x) are distinct, monic, and irreducible over F
    try:
        p_e = witness["p_e"]
        if not isinstance(p_e, list) or len(p_e) == 0:
            h2 = False
        else:
            h2 = True
            polys = []
            for item in p_e:
                if not isinstance(item, (list, tuple)) or len(item) != 2:
                    h2 = False
                    break
                p, e = item
                if not isinstance(e, int) or e < 1:
                    h2 = False
                    break
                poly = Poly(p, x, domain='QQ')
                if not poly.is_monic:
                    h2 = False
                    break
                if not poly.is_irreducible:
                    h2 = False
                    break
                polys.append(poly)
            if h2:
                if len(polys) != len(set(polys)):
                    h2 = False
    except Exception:
        h2 = False

    # ¬Q: V is not the direct sum of the T-invariant subspaces ker(p_i(T)^{e_i})
    try:
        T = witness["T"]
        p_e = witness["p_e"]
        n = T.rows
        total_dim = 0
        
        for p, e in p_e:
            poly = Poly(p, x, domain='QQ')
            coeffs = poly.all_coeffs()
            deg = poly.degree()
            T_poly = zeros(n, n)
            for i, c in enumerate(coeffs):
                power = deg - i
                T_poly += c * (T ** power)
            
            T_poly_e = T_poly ** e
            dim_ker = n - T_poly_e.rank()
            total_dim += dim_ker
            
        # Since p_i are distinct irreducibles, p_i^{e_i} are pairwise coprime.
        # Thus, their kernels are always independent and their sum is direct.
        # The sum equals V if and only if the sum of dimensions equals dim(V).
        if total_dim == n:
            neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over F, T is a linear operator",
    "H_2: The polynomials p_1(x), ..., p_k(x) are distinct, monic, and irreducible over F",
    "¬Q: V is not the direct sum of the T-invariant subspaces ker(p_i(T)^{e_i})"
]

N_HYP = 2
NEG_Q_INDEX = 2