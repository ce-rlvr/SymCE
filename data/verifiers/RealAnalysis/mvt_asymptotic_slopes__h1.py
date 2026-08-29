import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

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
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, sp.Expr):
            return [False, False]
    except Exception:
        return [False, False]

    free_symbols = witness.free_symbols
    if len(free_symbols) == 0:
        x = sp.Symbol('x')
    elif len(free_symbols) > 1:
        x_sym = sp.Symbol('x')
        if x_sym in free_symbols:
            x = x_sym
        else:
            x = list(free_symbols)[0]
    else:
        x = list(free_symbols)[0]

    # H1: limit of f'(x) as x -> oo exists and is a real number L
    try:
        df = sp.diff(witness, x)
        L = sp.limit(df, x, sp.oo)
        if L.has(sp.oo, -sp.oo, sp.zoo, sp.nan) or not L.is_number:
            h1 = False
        elif isinstance(L, sp.Limit) or type(L).__name__ == 'AccumBounds':
            h1 = False
        else:
            try:
                if abs(complex(L).imag) > 1e-9:
                    h1 = False
                else:
                    h1 = True
            except Exception:
                h1 = False
    except Exception:
        h1 = False
        L = None

    # neg_Q: limit of f(x)/x as x -> oo does not exist or is not equal to L
    try:
        if not h1:
            neg_q = False
        else:
            L2 = sp.limit(witness/x, x, sp.oo)
            if isinstance(L2, sp.Limit) or L2.has(sp.oo, -sp.oo, sp.zoo, sp.nan) or not L2.is_number or type(L2).__name__ == 'AccumBounds':
                if L2.has(sp.oo, -sp.oo, sp.zoo, sp.nan) or type(L2).__name__ == 'AccumBounds':
                    neg_q = True
                else:
                    # Unevaluated limit fallback to numerical check
                    try:
                        v1 = complex((witness/x).subs(x, 10**6).evalf())
                        v2 = complex((witness/x).subs(x, 10**7).evalf())
                        L_num = complex(L)
                        if abs(v1 - L_num) > 1e-2 or abs(v2 - L_num) > 1e-2:
                            neg_q = True
                        else:
                            neg_q = False
                    except Exception:
                        neg_q = False
            else:
                if abs(complex(L2) - complex(L)) > 1e-9:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        try:
            v = complex((witness/x).subs(x, 10**7).evalf())
            if abs(v - complex(L)) > 1e-2:
                neg_q = True
            else:
                neg_q = False
        except Exception:
            neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The limit lim_{x -> oo} f'(x) exists and is equal to a real number L",
    "¬Q: The limit lim_{x -> oo} f(x)/x does not exist or is not equal to L"
]

N_HYP = 1
NEG_Q_INDEX = 1