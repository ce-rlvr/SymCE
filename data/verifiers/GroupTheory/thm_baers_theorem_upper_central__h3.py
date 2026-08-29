import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # Handle dictionary-based mock witnesses
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('is_group', False))
            n = witness.get('n', 0)
            h2 = bool(isinstance(n, int) and n > 0)
            h3 = bool(witness.get('quotient_Zn_finite', False))
            neg_q = not bool(witness.get('gamma_n_plus_1_finite', True))
            return [h1, h2, h3, neg_q]
        except Exception:
            return [False, False, False, False]

    # Handle tuple (G, n) or object with attribute n
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, n = witness
        else:
            G = witness
            n = getattr(G, 'n', None)
            if n is None:
                return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a group
    try:
        if hasattr(G, 'is_group'):
            val = G.is_group
            h1 = bool(val() if callable(val) else val)
        elif hasattr(G, 'is_Group'):
            val = G.is_Group
            h1 = bool(val() if callable(val) else val)
        else:
            h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: n is a positive integer
    try:
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False

    # H_3: The quotient group G/Z_n(G) is finite
    try:
        h3 = False
        if hasattr(G, 'quotient_Zn_finite'):
            val = G.quotient_Zn_finite
            h3 = bool(val(n) if callable(val) else val)
        elif hasattr(G, 'is_quotient_Zn_finite'):
            val = G.is_quotient_Zn_finite
            h3 = bool(val(n) if callable(val) else val)
        elif hasattr(G, 'Zn_quotient_finite'):
            val = G.Zn_quotient_finite
            h3 = bool(val(n) if callable(val) else val)
        elif hasattr(G, 'Z') and hasattr(G, 'quotient'):
            Zn = G.Z(n)
            Q = G.quotient(Zn)
            if hasattr(Q, 'is_finite'):
                h3 = bool(Q.is_finite() if callable(Q.is_finite) else Q.is_finite)
            elif hasattr(Q, 'order'):
                from sympy import oo
                h3 = Q.order() < oo
        else:
            if isinstance(G, PermutationGroup):
                h3 = True
            elif hasattr(G, 'upper_central_series') and hasattr(G, 'quotient'):
                ucs = G.upper_central_series()
                idx = min(n, len(ucs) - 1)
                Zn = ucs[idx]
                Q = G.quotient(Zn)
                if hasattr(Q, 'order'):
                    from sympy import oo
                    h3 = Q.order() < oo
                elif hasattr(Q, 'is_finite'):
                    h3 = bool(Q.is_finite)
    except Exception:
        h3 = False

    # neg_Q: The (n+1)-th term of the lower central series gamma_{n+1}(G) is NOT a finite group
    try:
        q = True
        if hasattr(G, 'gamma_n_plus_1_finite'):
            val = G.gamma_n_plus_1_finite
            q = bool(val(n) if callable(val) else val)
        elif hasattr(G, 'is_gamma_n_plus_1_finite'):
            val = G.is_gamma_n_plus_1_finite
            q = bool(val(n) if callable(val) else val)
        elif hasattr(G, 'gamma_finite'):
            val = G.gamma_finite
            q = bool(val(n + 1) if callable(val) else val)
        elif hasattr(G, 'gamma'):
            gn1 = G.gamma(n + 1)
            if hasattr(gn1, 'is_finite'):
                q = bool(gn1.is_finite() if callable(gn1.is_finite) else gn1.is_finite)
            elif hasattr(gn1, 'order'):
                from sympy import oo
                q = gn1.order() < oo
        else:
            if isinstance(G, PermutationGroup):
                q = True
            elif hasattr(G, 'lower_central_series'):
                lcs = G.lower_central_series()
                idx = min(n, len(lcs) - 1)
                gn1 = lcs[idx]
                if hasattr(gn1, 'order'):
                    from sympy import oo
                    q = gn1.order() < oo
                elif hasattr(gn1, 'is_finite'):
                    q = bool(gn1.is_finite)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: n is a positive integer",
    "H_3: The quotient group G/Z_n(G) is finite",
    "¬Q: The (n+1)-th term of the lower central series gamma_{n+1}(G) is not a finite group"
]

N_HYP = 3
NEG_Q_INDEX = 3