import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, N) where G is a PermutationGroup and N is a subgroup.
    """
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a nilpotent group
    try:
        if callable(G.is_nilpotent):
            h1 = bool(G.is_nilpotent())
        else:
            h1 = bool(G.is_nilpotent)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = True
        # Check if N is a subgroup of G
        for gen in N.generators:
            if gen not in G:
                h2 = False
                break
        
        # Check normality: g * n * g^-1 in N for all generators
        if h2:
            for g in G.generators:
                for n in N.generators:
                    if (g * n * ~g) not in N:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # neg_Q: The intersection of N and Z(G) is the trivial group
    try:
        if callable(G.center):
            Z = G.center()
        else:
            Z = G.center
            
        try:
            n_elems = N.elements
        except Exception:
            n_elems = list(N.generate())
            
        neg_q = True
        for n in n_elems:
            is_id = getattr(n, 'is_Identity', False)
            try:
                if n == G.identity:
                    is_id = True
            except Exception:
                pass
                
            if not is_id and n in Z:
                neg_q = False
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: N is a normal subgroup of G",
    "¬Q: The intersection of N and Z(G) is the trivial group"
]

N_HYP = 2
NEG_Q_INDEX = 2