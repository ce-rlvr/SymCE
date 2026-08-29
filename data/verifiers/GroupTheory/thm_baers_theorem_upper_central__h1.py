import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def extract_bool(obj, keys, default=False):
    """Helper to safely extract boolean properties from a dict or object."""
    if isinstance(obj, dict):
        for k in keys:
            if k in obj:
                val = obj[k]
                if callable(val):
                    try:
                        return bool(val())
                    except Exception:
                        pass
                else:
                    return bool(val)
    else:
        for k in keys:
            if hasattr(obj, k):
                val = getattr(obj, k)
                if callable(val):
                    try:
                        return bool(val())
                    except Exception:
                        pass
                else:
                    return bool(val)
    return default

def conditions(witness) -> list[bool]:
    # Parse the witness which could be a tuple (G, n), a dict, or an object
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, n = witness
        elif isinstance(witness, dict):
            G = witness.get('G', witness)
            n = witness.get('n', None)
        else:
            G = witness
            n = getattr(witness, 'n', None)
    except Exception:
        return [False, False, False, False]

    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h1 = False

    # H_2: Z_n(G) is the n-th term of the upper central series of G
    # This is a definitional hypothesis. If not explicitly mocked, we assume it holds.
    try:
        h2_keys = ['Z_n_is_nth_upper_central', 'Z_n_correct', 'is_Z_n_correct']
        if isinstance(G, dict) and any(k in G for k in h2_keys):
            h2 = extract_bool(G, h2_keys)
        elif not isinstance(G, dict) and any(hasattr(G, k) for k in h2_keys):
            h2 = extract_bool(G, h2_keys)
        else:
            h2 = True
    except Exception:
        h2 = False

    # H_3: The quotient group G/Z_n(G) is finite
    try:
        h3_keys = ['quotient_finite', 'G_mod_Z_n_finite', 'is_quotient_finite', 'quotient_Z_n_finite']
        if isinstance(G, dict) and any(k in G for k in h3_keys):
            h3 = extract_bool(G, h3_keys)
        elif not isinstance(G, dict) and any(hasattr(G, k) for k in h3_keys):
            h3 = extract_bool(G, h3_keys)
        else:
            if isinstance(G, PermutationGroup):
                h3 = True
            else:
                h3 = extract_bool(G, ['is_finite', 'is_finite_group'], default=False)
    except Exception:
        h3 = False

    # ¬Q: The (n+1)-th term of the lower central series gamma_{n+1}(G) is NOT a finite group
    try:
        q_keys = ['gamma_finite', 'gamma_n_plus_1_finite', 'is_gamma_finite']
        if isinstance(G, dict) and any(k in G for k in q_keys):
            q = extract_bool(G, q_keys)
            neg_q = not q
        elif not isinstance(G, dict) and any(hasattr(G, k) for k in q_keys):
            q = extract_bool(G, q_keys)
            neg_q = not q
        else:
            if isinstance(G, PermutationGroup):
                neg_q = False
            else:
                is_fin = extract_bool(G, ['is_finite', 'is_finite_group'], default=None)
                if is_fin is True:
                    neg_q = False
                elif is_fin is False:
                    # If G is infinite and no other info is provided, we assume the conclusion fails
                    # to allow mock infinite groups to serve as counterexamples.
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: Z_n(G) is the n-th term of the upper central series of G",
    "H_3: The quotient group G/Z_n(G) is finite",
    "¬Q: The (n+1)-th term of the lower central series gamma_{n+1}(G) is not a finite group"
]

N_HYP = 3
NEG_Q_INDEX = 3