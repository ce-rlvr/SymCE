import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, H, n = witness
            elif len(witness) == 2:
                G, H = witness
                n = None
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if not h1:
            q = True
        else:
            if n is not None:
                GH_n = (G * H).derived_series()[n]
                G_n = G.derived_series()[n]
                H_n = H.derived_series()[n]
                q = (GH_n == G_n * H_n)
            else:
                q = True
                GH_series = (G * H).derived_series()
                G_series = G.derived_series()
                H_series = H.derived_series()
                max_len = max(len(GH_series), len(G_series), len(H_series))
                for i in range(max_len):
                    try:
                        if GH_series[i] != G_series[i] * H_series[i]:
                            q = False
                            break
                    except IndexError:
                        q = False
                        break
    except Exception:
        # If an exception occurs (e.g., IndexError when n is out of bounds for one of the series),
        # the mathematical equality cannot be evaluated as true, meaning the conclusion fails.
        q = False

    return [h1, not q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "¬Q: The n-th term of the derived series of GxH is not equal to G^(n) x H^(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1