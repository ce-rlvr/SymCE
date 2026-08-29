import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime

# Top-level setup
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, p, x) where:
      - G is a finite group (PermutationGroup)
      - p is a prime number
      - x is an element of G
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False]
        G, p, x = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False
        
    # H_3: x is an element of G
    try:
        h3 = bool(x in G)
    except Exception:
        h3 = False
        
    # neg_Q: C_G(x) does NOT contain a Sylow p-subgroup of G
    # By Sylow's theorems and Lagrange's theorem, C_G(x) contains a Sylow p-subgroup of G
    # if and only if the index [G : C_G(x)] is coprime to p.
    # The index [G : C_G(x)] is exactly the size of the conjugacy class of x.
    # Therefore, C_G(x) does NOT contain a Sylow p-subgroup iff p divides the conjugacy class size.
    try:
        if h1 and h2 and h3:
            orbit = {x}
            frontier = [x]
            gens = G.generators
            c_size = 1
            
            # Compute conjugacy class size using orbit algorithm (capped for performance)
            while frontier and c_size <= 10000:
                next_frontier = []
                for y in frontier:
                    for g in gens:
                        z = g * y * g**-1
                        if z not in orbit:
                            orbit.add(z)
                            next_frontier.append(z)
                            c_size += 1
                            if c_size > 10000:
                                break
                    if c_size > 10000:
                        break
                frontier = next_frontier
            
            if c_size > 10000:
                # Fallback to centralizer computation if the orbit is too large
                H = PermutationGroup([x])
                C = G.centralizer(H)
                c_size = G.order() // C.order()
                
            neg_q = bool(c_size % p == 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: x is an element of G",
    "¬Q: C_G(x) does not contain a Sylow p-subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3