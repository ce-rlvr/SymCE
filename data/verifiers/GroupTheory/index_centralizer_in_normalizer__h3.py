import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.ntheory import totient

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, x) or (G, x, n), checks if it is a valid counterexample.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, x, n = witness
            elif len(witness) == 2:
                G, x = witness
                n = 1
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: x is an element of G
    try:
        h2 = isinstance(x, Permutation) and x in G
    except Exception:
        h2 = False
        
    # neg_Q: The index of C_G(x) in N_G(H) does not divide phi(n)
    try:
        if not (isinstance(n, (int, sympy.Integer)) and n > 0):
            neg_q = False
        else:
            # Generate the cyclic subgroup H = <x>
            H_elements = set()
            curr = x
            for _ in range(x.order() + 2):
                H_elements.add(curr)
                if curr.is_Identity:
                    break
                curr = curr * x
                
            N_G_count = 0
            C_G_count = 0
            
            # Iterate over all elements in G to find normalizer and centralizer sizes
            for g in G.generate():
                conj = g * x * ~g
                if conj in H_elements:
                    N_G_count += 1
                if conj == x:
                    C_G_count += 1
                    
            if C_G_count == 0:
                neg_q = False
            else:
                index = N_G_count // C_G_count
                phi_n = totient(n)
                neg_q = (phi_n % index != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x is an element of G",
    "not Q: The index of C_G(x) in N_G(H) does not divide phi(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2