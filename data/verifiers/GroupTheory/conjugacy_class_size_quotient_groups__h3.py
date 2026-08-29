import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, N = witness
                x_list = None
            elif len(witness) == 3:
                G, N, x_val = witness
                x_list = [x_val]
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() < float('inf')
    except Exception:
        h1 = False
        
    # H2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False
        
    # neg_Q: The size of the conjugacy class of xN in G/N does NOT divide the size of the conjugacy class of x in G
    neg_q = False
    try:
        if h1 and h2:
            G_elements = list(G.generate())
            N_elements = list(N.generate())
            
            if x_list is None:
                x_list_to_check = G_elements
            else:
                x_list_to_check = [x for x in x_list if x in G_elements]
                
            visited = set()
            for x in x_list_to_check:
                if x in visited:
                    continue
                
                # Conjugacy class of x in G
                conj_G = set()
                for g in G_elements:
                    conj_G.add(g * x * ~g)
                
                visited.update(conj_G)
                size_G = len(conj_G)
                
                # Conjugacy class of xN in G/N
                # The class consists of cosets (g * x * ~g)N
                cosets_GN = set()
                for y in conj_G:
                    # Represent a coset by a frozenset of its elements
                    coset = frozenset(y * n for n in N_elements)
                    cosets_GN.add(coset)
                size_GN = len(cosets_GN)
                
                if size_G % size_GN != 0:
                    neg_q = True
                    break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "¬Q: The size of the conjugacy class of xN in G/N does not divide the size of the conjugacy class of x in G"
]

N_HYP = 2
NEG_Q_INDEX = 2