import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Integer

# Standard algebra objects
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

def dicyclic_group(n):
    """
    Constructs the dicyclic group Dic_n of order 4n as a PermutationGroup.
    Presentation: < a, x | a^{2n} = 1, x^2 = a^n, x^{-1} a x = a^{-1} >
    """
    if n < 1:
        return None
    A_list = [0] * (4 * n)
    X_list = [0] * (4 * n)
    for i in range(2 * n):
        # Generator a: two cycles of length 2n
        A_list[i] = (i + 1) % (2 * n)
        A_list[2 * n + i] = 2 * n + ((i + 1) % (2 * n))
        
        # Generator x
        X_list[i] = 2 * n + ((-i) % (2 * n))
        X_list[2 * n + i] = (-i + n) % (2 * n)
    
    return PermutationGroup(Permutation(A_list), Permutation(X_list))

def conditions(witness) -> list[bool]:
    try:
        G = None
        n = None
        
        if isinstance(witness, tuple) and len(witness) == 2:
            G, n = witness
        elif isinstance(witness, PermutationGroup):
            G = witness
            if G.order() % 4 == 0:
                n = G.order() // 4
        elif isinstance(witness, (int, Integer)):
            n = int(witness)
            if n >= 1:
                G = dicyclic_group(n)
                
        if G is None or n is None or n < 1:
            return [False, False]
            
        Dic_n = dicyclic_group(n)
        H1 = bool(G.is_isomorphic(Dic_n))
    except Exception:
        H1 = False
        
    try:
        if G is None or n is None or n < 1:
            neg_Q = False
        else:
            G_prime = G.derived_subgroup()
            Z_n = CyclicGroup(n)
            neg_Q = not bool(G_prime.is_isomorphic(Z_n))
    except Exception:
        neg_Q = False
        
    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: G is the dicyclic group Dic_n of order 4n",
    "¬Q: The commutator subgroup G' is not isomorphic to the cyclic group of order n"
]

N_HYP = 1
NEG_Q_INDEX = 1