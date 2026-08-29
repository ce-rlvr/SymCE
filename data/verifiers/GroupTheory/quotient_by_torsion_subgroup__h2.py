import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, T) or a dict {'G': G, 'T': T} where G is a group and T is a subgroup.
    """
    try:
        if isinstance(witness, dict):
            G = witness['G']
            T = witness['T']
        else:
            G, T = witness
    except Exception:
        return [False, False]
        
    # H_1: G is an abelian group
    try:
        h1 = bool(G.is_abelian)
    except Exception:
        h1 = False
        
    # ¬Q: The quotient group G/T is not torsion-free
    # For finite groups, G/T is torsion-free if and only if it is the trivial group (order 1).
    # Thus, G/T is not torsion-free iff |G| > |T|.
    try:
        if isinstance(T, list):
            if len(T) == 0:
                is_sub = True
                order_T = 1
            else:
                T_group = PermutationGroup(T)
                is_sub = all(g in G for g in T_group.generators)
                order_T = T_group.order()
        else:
            is_sub = all(g in G for g in T.generators)
            order_T = T.order()
            
        if is_sub:
            order_G = G.order()
            if order_G != sympy.oo and order_G != float('inf'):
                neg_q = bool(order_G > order_T)
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "¬Q: The quotient group G/T is not torsion-free"
]

N_HYP = 1
NEG_Q_INDEX = 1