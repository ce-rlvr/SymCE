import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If M is a maximal subgroup of G, and M is finite, then G is finite."
    
    The witness should represent the pair (G, M).
    Since the only groups satisfying this are exotic infinite groups (e.g., Tarski monsters),
    the witness is expected to be a mock object, a dictionary, or a string representation.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, M = witness
        elif isinstance(witness, dict):
            G = witness.get('G')
            M = witness.get('M')
        else:
            G = witness.G
            M = witness.M
    except Exception:
        return [False, False, False]

    # Special case for string-based witnesses of known exotic counterexamples
    if isinstance(G, str):
        g_lower = G.lower()
        if "tarski" in g_lower or "monster" in g_lower:
            h1 = True
            neg_q = True
            if isinstance(M, str):
                h2 = True
            else:
                try:
                    if isinstance(M, dict):
                        if 'is_finite' in M:
                            val = M['is_finite']
                            h2 = val() if callable(val) else bool(val)
                        else:
                            h2 = True
                    else:
                        if hasattr(M, 'is_finite'):
                            val = M.is_finite
                            h2 = val() if callable(val) else bool(val)
                        elif hasattr(M, 'order'):
                            o = M.order()
                            h2 = o != float('inf') and str(o) != 'oo'
                        else:
                            h2 = True
                except Exception:
                    h2 = False
            return [h1, h2, neg_q]

    # H_1: M is a maximal subgroup of G
    try:
        h1 = False
        if isinstance(G, dict):
            if 'is_maximal_subgroup' in G:
                val = G['is_maximal_subgroup']
                h1 = val(M) if callable(val) else bool(val)
            elif 'maximal_subgroups' in G:
                h1 = M in G['maximal_subgroups']
        else:
            if hasattr(G, 'is_maximal_subgroup'):
                val = G.is_maximal_subgroup
                h1 = val(M) if callable(val) else bool(val)
            elif hasattr(G, 'maximal_subgroups'):
                val = G.maximal_subgroups
                subs = val() if callable(val) else val
                h1 = M in subs

        if not h1:
            if isinstance(M, dict):
                if 'is_maximal_in' in M:
                    val = M['is_maximal_in']
                    h1 = val(G) if callable(val) else bool(val)
                elif 'is_maximal_subgroup_of' in M:
                    val = M['is_maximal_subgroup_of']
                    h1 = val(G) if callable(val) else bool(val)
            else:
                if hasattr(M, 'is_maximal_in'):
                    val = M.is_maximal_in
                    h1 = val(G) if callable(val) else bool(val)
                elif hasattr(M, 'is_maximal_subgroup_of'):
                    val = M.is_maximal_subgroup_of
                    h1 = val(G) if callable(val) else bool(val)
    except Exception:
        h1 = False

    # H_2: M is a finite group
    try:
        h2 = False
        if isinstance(M, dict):
            if 'is_finite' in M:
                val = M['is_finite']
                h2 = val() if callable(val) else bool(val)
        else:
            if hasattr(M, 'is_finite'):
                val = M.is_finite
                h2 = val() if callable(val) else bool(val)
            elif hasattr(M, 'order'):
                o = M.order()
                h2 = o != float('inf') and str(o) != 'oo'
            elif type(M).__name__ == 'PermutationGroup':
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: G is NOT a finite group
    try:
        neg_q = False
        if isinstance(G, dict):
            if 'is_finite' in G:
                val = G['is_finite']
                is_fin = val() if callable(val) else bool(val)
                neg_q = not is_fin
        else:
            if hasattr(G, 'is_finite'):
                val = G.is_finite
                is_fin = val() if callable(val) else bool(val)
                neg_q = not is_fin
            elif hasattr(G, 'order'):
                o = G.order()
                neg_q = o == float('inf') or str(o) == 'oo'
            elif type(G).__name__ == 'PermutationGroup':
                neg_q = False
            elif type(G).__name__ == 'FreeGroup':
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is a maximal subgroup of G",
    "H_2: M is a finite group",
    "¬Q: G is not a finite group"
]

N_HYP = 2
NEG_Q_INDEX = 2