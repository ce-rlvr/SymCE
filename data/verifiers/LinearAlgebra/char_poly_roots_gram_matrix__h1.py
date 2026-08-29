import sympy
from sympy import Matrix, eye, zeros, Symbol

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H1: G = A^* A is well-defined
    try:
        if not hasattr(witness, 'H'):
            h1 = False
            G = None
        else:
            G = witness.H * witness
            h1 = True
    except Exception:
        h1 = False
        G = None

    # H2: p(x) is well-defined
    try:
        if h1 and hasattr(G, 'charpoly'):
            x = Symbol('x')
            p = G.charpoly(x)
            h2 = True
        else:
            h2 = False
            p = None
    except Exception:
        h2 = False
        p = None

    # neg_Q: Not all roots of p(x) are non-negative real numbers
    try:
        if not h2:
            neg_q = False
        else:
            roots = p.roots()
            if hasattr(G, 'shape') and sum(roots.values()) < G.shape[0]:
                if hasattr(G, 'eigenvals'):
                    roots = G.eigenvals()
            
            all_non_negative_real = True
            for r in roots.keys():
                if r.is_nonnegative is False:
                    all_non_negative_real = False
                    break
                elif r.is_nonnegative is None:
                    try:
                        c = complex(r.evalf())
                        if abs(c.imag) > 1e-12 or c.real < -1e-12:
                            all_non_negative_real = False
                            break
                    except Exception:
                        all_non_negative_real = False
                        break
            neg_q = not all_non_negative_real
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G = A^* A is well-defined",
    "H_2: p(x) is the characteristic polynomial of G",
    "¬Q: Not all roots of p(x) are non-negative real numbers"
]
N_HYP = 2
NEG_Q_INDEX = 2