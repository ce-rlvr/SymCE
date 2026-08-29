import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, B = witness
    except Exception:
        return [False, False, False, False]

    # H1: V is a vector space over a field F (B is a subset of V)
    try:
        h1 = False
        if isinstance(B, (list, tuple)) and isinstance(G, (list, tuple)) and len(G) > 0:
            n = G[0].rows
            h1 = True
            for v in B:
                if not isinstance(v, sympy.MatrixBase) or v.rows != n or v.cols != 1:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: GL(V) is the general linear group of V (G contains invertible matrices)
    try:
        h2 = False
        if h1:
            n = G[0].rows
            h2 = True
            for g in G:
                if not isinstance(g, sympy.MatrixBase) or g.rows != n or g.cols != n:
                    h2 = False
                    break
                if g.det() == 0:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # H3: G is a subgroup of GL(V) acting naturally on V
    try:
        h3 = False
        if h2:
            n = G[0].rows
            I = sympy.eye(n)
            h3 = True
            if I not in G:
                h3 = False
            else:
                # Check closure under multiplication
                for g1 in G:
                    for g2 in G:
                        if g1 * g2 not in G:
                            h3 = False
                            break
                    if not h3:
                        break
                # Check closure under inversion
                if h3:
                    for g in G:
                        if g.inv() not in G:
                            h3 = False
                            break
    except Exception:
        h3 = False

    # neg_Q: The pointwise stabilizer of B in G is not the trivial subgroup
    try:
        neg_q = False
        if h2:
            n = G[0].rows
            I = sympy.eye(n)
            for g in G:
                if g != I:
                    stabilizes = True
                    for v in B:
                        if g * v != v:
                            stabilizes = False
                            break
                    if stabilizes:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F (B is a subset of V)",
    "H_2: GL(V) is the general linear group of V (G contains invertible matrices)",
    "H_3: G is a subgroup of GL(V) acting naturally on V",
    "¬Q: The pointwise stabilizer of B in G is not the trivial subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3