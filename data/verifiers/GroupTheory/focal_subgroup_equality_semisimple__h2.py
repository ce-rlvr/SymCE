import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = DihedralGroup(2)

def get_order(grp):
    return grp.order() if callable(grp.order) else grp.order

def check_solvable(grp):
    return grp.is_solvable() if callable(grp.is_solvable) else grp.is_solvable

def conditions(witness):
    try:
        # The witness can be a group G, or a tuple (G, P) where P is a Sylow subgroup.
        if isinstance(witness, tuple):
            G, P = witness
        else:
            G = witness
            P = None

        # H_1: G is a semisimple finite group
        # A finite group is semisimple if it has no non-trivial normal solvable subgroups.
        h1 = False
        if isinstance(G, PermutationGroup):
            g_order = get_order(G)
            if g_order > 1 and check_solvable(G):
                h1 = False
            else:
                is_semi = True
                for N in G.normal_subgroups():
                    if get_order(N) > 1 and check_solvable(N):
                        is_semi = False
                        break
                h1 = is_semi

        # neg_Q: The focal subgroup of P in G, defined as P \cap [G, G], is equal to P.
        # The conclusion holds if P \cap [G, G] == P, which is equivalent to P being a subgroup of [G, G].
        # We want neg_Q to be True when the conclusion FAILS (i.e., P is NOT a subgroup of [G, G]).
        neg_q = False
        if h1:
            D = G.derived_subgroup()
            if P is not None:
                # Check if the specific Sylow subgroup P is contained in D
                is_sub = all(g in D for g in P.generators)
                neg_q = not is_sub
            else:
                # If P is not specified, the conclusion fails if it fails for ANY Sylow subgroup
                g_order = get_order(G)
                primes = factorint(g_order).keys()
                all_sylow_in_D = True
                for p in primes:
                    Syl_p = G.sylow_subgroup(p)
                    if not all(g in D for g in Syl_p.generators):
                        all_sylow_in_D = False
                        break
                neg_q = not all_sylow_in_D

    except Exception:
        h1 = False
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "¬Q: The focal subgroup of P in G is not equal to P"
]

N_HYP = 1
NEG_Q_INDEX = 1