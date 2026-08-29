import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard groups and matrices
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

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "H_2: T is the subgroup of G consisting of all elements of finite order",
    "¬Q: G is not isomorphic to T ⊕ G/T, or G/T is not a free abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The true theorem requires G to be an abelian group. Without it, any finitely 
    generated, torsion-free, non-abelian group (like the free group F2) is a counterexample.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, str):
            w = witness.lower().replace(" ", "")
            if w in ["f2", "f3", "freegroup(2)", "freegroup(3)", "freegroup(rank=2)"]:
                return [True, True, True]

        # The witness might be provided as just the group G, or a tuple (G, T)
        if isinstance(witness, tuple) and len(witness) == 2:
            G = witness[0]
        else:
            G = witness

        G_type = type(G).__name__

        # Check if G is a Free Group
        if G_type == 'FreeGroup':
            rank = len(G.generators)
            h1 = True  # Free groups of finite rank are finitely generated
            h2 = True  # Free groups are torsion-free, so T = {1} is a subgroup
            
            # If rank > 1, G is non-abelian. G/T = G/{1} = G.
            # G is not a free abelian group, so the conclusion fails.
            neg_q = (rank > 1)
            
        # Check if G is a Finitely Presented Group
        elif G_type == 'FpGroup':
            # We specifically look for free groups presented without relators to avoid 
            # undecidable word problems and timeouts.
            if len(G.relators) == 0:
                rank = len(G.generators)
                h1 = True
                h2 = True
                neg_q = (rank > 1)
                
        # Check if G is a Finite Permutation Group
        elif isinstance(G, PermutationGroup):
            h1 = True
            h2 = True  # In a finite group, all elements have finite order, so T = G
            # G/T = G/G = {1}, which is the free abelian group of rank 0.
            # G is isomorphic to G ⊕ {1}. Thus, the conclusion holds for all finite groups.
            neg_q = False
            
    except Exception:
        pass

    return [h1, h2, neg_q]