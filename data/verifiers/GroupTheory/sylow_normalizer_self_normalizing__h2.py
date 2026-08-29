import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

# Top-level setup: named object bindings
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

def get_normalizer_set(G_elements, P_elements):
    P_set = set(P_elements)
    norm_set = set()
    for g in G_elements:
        is_in_norm = True
        for p in P_set:
            # Check if g * p * g^-1 is in P
            if (g * p * ~g) not in P_set:
                is_in_norm = False
                break
        if is_in_norm:
            norm_set.add(g)
    return norm_set

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, P = witness
                N = None
            elif len(witness) == 3:
                G, P, N = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
        
        # H_1: G is a finite group
        h1 = isinstance(G, PermutationGroup)
        if not h1:
            return [False, False, False, False]
            
        if not isinstance(P, PermutationGroup):
            return [True, False, False, False]
            
        # H_2: P is a Sylow p-subgroup of G
        h2 = False
        if P.is_subgroup(G):
            order_G = G.order()
            order_P = P.order()
            factors_P = factorint(order_P)
            
            if len(factors_P) <= 1:
                if len(factors_P) == 1:
                    p, k = list(factors_P.items())[0]
                    # Check if p^k is the highest power of p dividing |G|
                    if order_G % (p**k) == 0 and order_G % (p**(k+1)) != 0:
                        h2 = True
                else:
                    # order_P == 1, which is a Sylow p-subgroup for any prime p not dividing |G|
                    h2 = True
                    
        # H_3: N_G(P) is the normalizer of P in G
        G_elements = list(G.generate())
        P_elements = list(P.generate())
        norm_P_set = get_normalizer_set(G_elements, P_elements)
        
        if N is not None:
            if isinstance(N, PermutationGroup):
                N_elements = set(N.generate())
                h3 = (N_elements == norm_P_set)
            else:
                h3 = False
                N_elements = norm_P_set  # Fallback to prevent crash in conclusion check
        else:
            h3 = True
            N_elements = norm_P_set
            
        # ¬Q: The normalizer of N_G(P) in G is NOT equal to N_G(P)
        norm_N_set = get_normalizer_set(G_elements, N_elements)
        neg_q = (norm_N_set != set(N_elements))
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: N_G(P) is the normalizer of P in G",
    "¬Q: The normalizer of N_G(P) in G is not equal to N_G(P)"
]

N_HYP = 3
NEG_Q_INDEX = 3