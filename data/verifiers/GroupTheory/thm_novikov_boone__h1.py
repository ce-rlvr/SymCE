import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.combinatorics.free_groups import FreeGroup
from sympy.combinatorics.fp_groups import FpGroup
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
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: The witness represents a presentation or a class of presentations P.
    # We accept a single group or a list of groups (representing the class P).
    try:
        if isinstance(witness, (FpGroup, PermutationGroup, FreeGroup)):
            h1 = True
            groups = [witness]
        elif isinstance(witness, list) and all(isinstance(g, (FpGroup, PermutationGroup, FreeGroup)) for g in witness):
            h1 = True
            groups = witness
        else:
            h1 = False
            groups = []
    except Exception:
        h1 = False
        groups = []

    # neg_Q: The conclusion states there exists at least one finite presentation in P 
    # for which the word problem is algorithmically undecidable.
    # The negation is that for ALL presentations in P, the word problem is DECIDABLE.
    try:
        if not groups:
            neg_q = False
        else:
            neg_q = True
            for G in groups:
                decidable = False
                # Free groups and finite permutation groups have a decidable word problem
                if isinstance(G, (PermutationGroup, FreeGroup)):
                    decidable = True
                elif isinstance(G, FpGroup):
                    # If there are no relators, it's a free group (decidable)
                    if len(G.relators) == 0:
                        decidable = True
                    else:
                        # If it's a finite presentation of a finite group, it's decidable.
                        # We attempt to compute its order to verify finiteness.
                        try:
                            ord_G = G.order()
                            if ord_G is not None and ord_G > 0:
                                decidable = True
                        except Exception:
                            pass
                
                if not decidable:
                    neg_q = False
                    break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Witness is a presentation or a collection of presentations",
    "¬Q: The word problem is decidable for all presentations in the witness"
]

N_HYP = 1
NEG_Q_INDEX = 1