import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a group and N is a subgroup of G",
    "¬Q: The centralizer C_G(N) is not a normal subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    # Extract G and N from the witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
        else:
            G, N = witness
            
        # Normalize N to a PermutationGroup if it's a list or a single Permutation
        if isinstance(N, list):
            N = PermutationGroup(N)
        elif isinstance(N, Permutation):
            N = PermutationGroup([N])
    except Exception:
        return [False, False]
        
    # H_1: G is a group and N is a subgroup of G
    try:
        h1_ok = (isinstance(G, PermutationGroup) and 
                 isinstance(N, PermutationGroup) and 
                 all(G.contains(n) for n in N.generators))
    except Exception:
        h1_ok = False
        
    # ¬Q: The centralizer C_G(N) is not a normal subgroup of G
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            gens_N = N.generators
            c_elements = []
            
            # Find all elements in G that commute with every generator of N
            for g in G.generate():
                if all(g * n == n * g for n in gens_N):
                    c_elements.append(g)
            
            if not c_elements:
                neg_q_ok = False
            else:
                C = PermutationGroup(c_elements)
                is_normal = True
                
                # Check if C is normal in G: for all g in G, c in C, g * c * g^-1 in C
                for g in G.generate():
                    for c in C.generators:
                        if not C.contains(g * c * ~g):
                            is_normal = False
                            break
                    if not is_normal:
                        break
                        
                neg_q_ok = not is_normal
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]