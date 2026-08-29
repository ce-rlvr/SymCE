import sympy
from sympy.combinatorics import Permutation
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a counterexample to the conjecture.
    The conjecture claims: If G is a group, Z_n(G) is the n-th term of the upper central series,
    and G/Z_n(G) is finite, then \gamma_{n+1}(G) is finite.
    """
    try:
        # Witness could be a tuple (G, n) or just G
        if isinstance(witness, tuple) and len(witness) == 2:
            G, n = witness
        else:
            G = witness
            n = None

        def get_prop(obj, prop_names):
            if isinstance(obj, dict):
                for name in prop_names:
                    if name in obj:
                        return bool(obj[name])
            for name in prop_names:
                if hasattr(obj, name):
                    val = getattr(obj, name)
                    return bool(val() if callable(val) else val)
            return None

        # H_1: G is a group
        h1_val = get_prop(G, ['is_group'])
        if h1_val is not None:
            h1 = h1_val
        else:
            h1 = hasattr(G, 'elements') or hasattr(G, 'generators')

        # H_2: Z_n(G) is the n-th term of the upper central series of G
        h2_val = get_prop(G, ['is_Z_n_upper_central', 'Z_n_is_upper_central'])
        if h2_val is not None:
            h2 = h2_val
        else:
            # Definitional hypothesis; assumed true if not explicitly mocked
            h2 = True

        # H_3: The quotient group G/Z_n(G) is finite
        h3_val = get_prop(G, ['quotient_finite', 'is_quotient_finite', 'G_mod_Z_n_finite'])
        if h3_val is not None:
            h3 = h3_val
        else:
            try:
                is_fin = get_prop(G, ['is_finite'])
                h3 = is_fin if is_fin is not None else True
            except Exception:
                h3 = False

        # neg_Q: The (n+1)-th term of the lower central series \gamma_{n+1}(G) is NOT finite
        gamma_val = get_prop(G, ['gamma_n_plus_1_finite', 'is_gamma_finite', 'lower_central_finite'])
        if gamma_val is not None:
            gamma_finite = gamma_val
        else:
            try:
                is_fin = get_prop(G, ['is_finite'])
                gamma_finite = is_fin if is_fin is not None else True
            except Exception:
                gamma_finite = True
                
        neg_q = not gamma_finite

        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Z_n(G) is the n-th term of the upper central series of G",
    "H_3: The quotient group G/Z_n(G) is finite",
    "¬Q: The (n+1)-th term of the lower central series gamma_{n+1}(G) is not a finite group"
]

N_HYP = 3
NEG_Q_INDEX = 3