import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import totient
import math

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

def holomorph_cyclic(n):
    """Constructs the holomorph of the cyclic group C_n as a PermutationGroup."""
    if n == 1:
        return PermutationGroup([Permutation(0)])
    
    # Generator for C_n acting on itself by addition modulo n
    sigma = Permutation([(i + 1) % n for i in range(n)])
    gens = [sigma]
    
    # Generators for Aut(C_n) acting on C_n by multiplication modulo n
    for k in range(1, n):
        if math.gcd(k, n) == 1:
            tau_k = Permutation([(k * i) % n for i in range(n)])
            gens.append(tau_k)
            
    return PermutationGroup(gens)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Case 1: Witness is just the integer n
        if isinstance(witness, int) and not isinstance(witness, bool):
            n = witness
            if n > 0:
                h1 = True
                h2 = True  # G is defined as the holomorph of C_n
                G = holomorph_cyclic(n)
                neg_q = not bool(G.is_solvable)
                
        # Case 2: Witness is a tuple (n, G)
        elif isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int):
            n, G = witness
            if n > 0:
                h1 = True
                try:
                    hol = holomorph_cyclic(n)
                    h2 = bool(G.is_isomorphic(hol))
                except Exception:
                    h2 = False
                neg_q = not bool(G.is_solvable)
                
        # Case 3: Witness is just the group G
        elif isinstance(witness, PermutationGroup):
            G = witness
            h1 = True  # We assume there exists some C_n
            order = G.order()
            h2 = False
            
            # Find an n such that |Hol(C_n)| == |G| and check for isomorphism
            if order <= 100000:
                for n in range(1, order + 1):
                    if n * totient(n) == order:
                        hol = holomorph_cyclic(n)
                        try:
                            if G.is_isomorphic(hol):
                                h2 = True
                                break
                        except Exception:
                            pass
            neg_q = not bool(G.is_solvable)
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: C_n is a cyclic group of order n",
    "H_2: G is the holomorph of C_n",
    "¬Q: G is not solvable"
]

N_HYP = 2
NEG_Q_INDEX = 2