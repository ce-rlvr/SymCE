import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
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
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Witness is expected to be a tuple: (G, P, p)
    where G is a PermutationGroup, P is a PermutationGroup (subgroup of G), and p is an integer.
    """
    try:
        G, P, p = witness
    except Exception:
        return [False, False, False]

    # H_1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        is_sub = P.is_subgroup(G)
        p_order = P.order()
        
        # Check if P is a p-group
        temp = p_order
        is_p_group = True
        if temp > 1:
            while temp % p == 0:
                temp //= p
            if temp != 1:
                is_p_group = False
        else:
            is_p_group = True
            
        # Check if P is maximal (p does not divide the index [G : P])
        is_maximal = (G.order() % (p_order * p)) != 0
        
        h2 = bool(is_sub and is_p_group and is_maximal)
    except Exception:
        h2 = False

    # ¬Q: The conclusion "P is a normal subgroup of G if and only if P is the unique Sylow p-subgroup of G" FAILS.
    try:
        is_normal = P.is_normal(G)
        
        # Check if P is the unique Sylow p-subgroup.
        # By Sylow's theorems, all Sylow p-subgroups are conjugate.
        # Thus, P is unique if and only if it contains all its conjugates,
        # which is mathematically equivalent to P being a normal subgroup.
        is_unique = True
        for g in G.generators:
            for h in P.generators:
                if not P.contains(g * h * ~g):
                    is_unique = False
                    break
                if not P.contains((~g) * h * g):
                    is_unique = False
                    break
            if not is_unique:
                break
                
        # The conclusion is the biconditional: is_normal <==> is_unique
        # We want the negation of this conclusion.
        neg_q = not (is_normal == is_unique)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P is a Sylow p-subgroup of G",
    "¬Q: The biconditional 'P is normal in G iff P is the unique Sylow p-subgroup' is false"
]

N_HYP = 2
NEG_Q_INDEX = 2