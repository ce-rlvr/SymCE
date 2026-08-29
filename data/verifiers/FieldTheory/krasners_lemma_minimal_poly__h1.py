import sympy as sp
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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

def conditions(witness):
    try:
        # Witness is expected to be a tuple of two algebraic elements (alpha, beta)
        alpha, beta = witness
    except Exception:
        return [False, False, False, False, False]
        
    x = sp.Symbol('x')
    
    # H_1: alpha and beta are separable algebraic elements over K (we assume K=Q)
    try:
        m_alpha = sp.minpoly(alpha, x)
        m_beta = sp.minpoly(beta, x)
        # Over Q, all algebraic elements are separable.
        h1 = True
    except Exception:
        h1 = False

    # H_2: m_alpha is the minimal polynomial of alpha over K
    try:
        if h1 and m_alpha.has(x):
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: r is the minimum distance between alpha and any of its distinct Galois conjugates
    try:
        if h2:
            num_roots = sp.nroots(m_alpha)
            alpha_val = complex(sp.N(alpha))
            distances = []
            for r_expr in num_roots:
                r_val = complex(r_expr)
                dist = abs(alpha_val - r_val)
                if dist > 1e-7:  # distinct conjugate
                    distances.append(dist)
            if distances:
                r_min = min(distances)
            else:
                r_min = float('inf')
            h3 = True
        else:
            h3 = False
            r_min = 0
    except Exception:
        h3 = False
        r_min = 0

    # H_4: The distance between alpha and beta is strictly less than r
    try:
        if h3:
            beta_val = complex(sp.N(beta))
            dist_ab = abs(alpha_val - beta_val)
            h4 = dist_ab < r_min - 1e-9
        else:
            h4 = False
    except Exception:
        h4 = False

    # ¬Q: The minimal polynomial of alpha over K(beta) is NOT x - alpha (i.e., alpha is NOT in K(beta))
    try:
        if h1:
            deg_beta = sp.degree(m_beta, x)
            # Find the degree of the extension K(alpha, beta) over K
            # By Primitive Element Theorem, alpha + c*beta is primitive for most c.
            deg_ext = max(sp.degree(sp.minpoly(alpha + c * beta, x), x) for c in range(1, 10))
            
            # alpha is in K(beta) iff the degree of K(alpha, beta) equals the degree of K(beta)
            alpha_in_K_beta = (deg_ext == deg_beta)
            neg_q = not alpha_in_K_beta
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: α and β are separable algebraic elements over K",
    "H_2: m_α(x) is the minimal polynomial of α over K",
    "H_3: r is the minimum distance between α and any of its distinct Galois conjugates",
    "H_4: The distance between α and β is strictly less than r",
    "¬Q: The minimal polynomial of α over K(β) is not x - α (i.e., α ∉ K(β))"
]

N_HYP = 4
NEG_Q_INDEX = 4