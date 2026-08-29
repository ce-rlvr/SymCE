import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
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
    # H_1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The direct product G × G acts on G via (g, h) · x = g x h⁻¹
    try:
        if not h1:
            h2 = False
        else:
            G = witness
            elems = list(G.elements)
            e = G.identity
            
            # Check identity action: (e, e) · x == x
            ident_ok = all(e * x * e**-1 == x for x in elems)
            
            # Check compatibility: (g1, h1) · ((g2, h2) · x) == (g1*g2, h1*h2) · x
            # Checked on generators to ensure it completes quickly
            gens = G.generators if G.generators else [e]
            compat_ok = True
            for g1, h1, g2, h2 in itertools.product(gens, gens, gens, gens):
                for x in elems:
                    step1 = g2 * x * h2**-1
                    step2 = g1 * step1 * h1**-1
                    expected = (g1 * g2) * x * (h1 * h2)**-1
                    if step2 != expected:
                        compat_ok = False
                        break
                if not compat_ok:
                    break
            
            h2 = ident_ok and compat_ok
    except Exception:
        h2 = False

    # ¬Q: The stabilizer of e in G × G is not the diagonal subgroup Δ(G)
    try:
        if not h1:
            neg_q = False
        else:
            G = witness
            elems = list(G.elements)
            e = G.identity
            
            stab_e = set()
            for g in elems:
                for h in elems:
                    if g * e * h**-1 == e:
                        stab_e.add((g, h))
            
            delta_G = set((g, g) for g in elems)
            
            # The conclusion is that stab_e == delta_G.
            # We return True if the conclusion FAILS.
            neg_q = not (stab_e == delta_G)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The direct product G × G acts on G via (g, h) · x = g x h⁻¹",
    "¬Q: The stabilizer of e in G × G is not the diagonal subgroup Δ(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2