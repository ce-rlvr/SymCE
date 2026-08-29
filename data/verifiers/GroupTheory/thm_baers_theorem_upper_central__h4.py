import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
from sympy import oo

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
try:
    V4 = AbelianGroup(2, 2)
except Exception:
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
    "H_1: G is a group",
    "H_2: n is a positive integer",
    "H_3: Z_n(G) is the n-th term of the upper central series of G",
    "¬Q: The (n+1)-th term of the lower central series gamma_{n+1}(G) is not a finite group"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) >= 2:
            G = witness[0]
            n = witness[1]
        else:
            G = witness
            n = 1
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = False
        if isinstance(G, PermutationGroup):
            h1 = True
        elif hasattr(G, 'is_group') and G.is_group:
            h1 = True
        elif hasattr(G, 'generators') and hasattr(G, 'identity'):
            h1 = True
        elif hasattr(G, 'lower_central_series'):
            h1 = True
    except Exception:
        h1 = False

    # H_2: n is a positive integer
    try:
        h2 = int(n) > 0 and float(n) == int(n)
    except Exception:
        h2 = False

    # H_3: Z_n(G) is the n-th term of the upper central series of G
    # This is a definitional hypothesis establishing notation.
    try:
        h3 = True
    except Exception:
        h3 = False

    # neg_Q: gamma_{n+1}(G) is not a finite group
    try:
        neg_q = False
        term = None
        
        if hasattr(G, 'lower_central_series'):
            lcs_attr = G.lower_central_series
            if callable(lcs_attr):
                lcs = lcs_attr()
            else:
                lcs = lcs_attr
                
            if int(n) < len(lcs):
                term = lcs[int(n)]
            else:
                term = lcs[-1]
        elif hasattr(G, 'gamma'):
            gamma_attr = G.gamma
            if callable(gamma_attr):
                term = gamma_attr(int(n) + 1)
            else:
                term = gamma_attr[int(n) + 1]
                
        if term is not None:
            if hasattr(term, 'order'):
                ord_attr = term.order
                if callable(ord_attr):
                    ord_val = ord_attr()
                else:
                    ord_val = ord_attr
                neg_q = (ord_val == oo or str(ord_val) == 'oo')
            elif hasattr(term, 'is_finite'):
                fin_attr = term.is_finite
                if callable(fin_attr):
                    is_fin = fin_attr()
                else:
                    is_fin = fin_attr
                neg_q = not is_fin
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]