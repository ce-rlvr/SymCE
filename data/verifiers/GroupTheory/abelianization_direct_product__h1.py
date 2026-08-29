import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.matrices import eye, zeros

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

try:
    trivial = CyclicGroup(1)
except Exception:
    trivial = PermutationGroup([Permutation(0)])

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: witness is a pair of groups (G, H) with abelianizations",
    "¬Q: The abelianization of G x H is not isomorphic to G_ab x H_ab"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        h1 = (isinstance(witness, tuple) and len(witness) == 2 and
              hasattr(witness[0], 'abelian_invariants') and
              hasattr(witness[1], 'abelian_invariants'))
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            G, H = witness
            
            def construct_abelian_group(invs):
                invs = [d for d in invs if d > 1]
                if not invs:
                    try:
                        return CyclicGroup(1)
                    except Exception:
                        return PermutationGroup([Permutation(0)])
                res = CyclicGroup(invs[0])
                for d in invs[1:]:
                    res = res * CyclicGroup(d)
                return res
            
            # Compute abelian invariants of G x H
            invs_GH = (G * H).abelian_invariants()
            
            # Compute abelian invariants of G_ab x H_ab
            G_ab = construct_abelian_group(G.abelian_invariants())
            H_ab = construct_abelian_group(H.abelian_invariants())
            invs_Gab_Hab = (G_ab * H_ab).abelian_invariants()
            
            # Two finite abelian groups are isomorphic iff their invariant factors are identical
            neg_q = (list(invs_GH) != list(invs_Gab_Hab))
    except Exception:
        neg_q = False

    return [h1, neg_q]