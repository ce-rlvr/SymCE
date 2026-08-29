import math
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard group theory objects
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

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    'Sylow Subgroups of Coprime Semidirect Products' (with a dropped hypothesis).
    
    Witness is expected to be a tuple: (G, N, H, p)
    where G, N, H are PermutationGroups and p is an integer.
    """
    try:
        G, N, H, p = witness
    except Exception:
        return [False, False, False]

    # H_1: The orders |N| and |H| are relatively prime (and N, H are subgroups of G)
    try:
        # Check that N and H are actually subgroups of G
        n_in_g = all(g in G for g in N.generators)
        h_in_g = all(g in G for g in H.generators)
        
        # Check coprime orders
        gcd_coprime = math.gcd(int(N.order()), int(H.order())) == 1
        
        h1 = bool(n_in_g and h_in_g and gcd_coprime)
    except Exception:
        h1 = False

    # H_2: p is a prime number dividing |H|
    try:
        h2 = bool(sympy.isprime(p) and int(H.order()) % int(p) == 0)
    except Exception:
        h2 = False

    # ¬Q: Every Sylow p-subgroup of G is isomorphic to a Sylow p-subgroup of H (must FAIL)
    # Negation: A Sylow p-subgroup of G is NOT isomorphic to a Sylow p-subgroup of H.
    try:
        if not sympy.isprime(p):
            neg_q = False
        else:
            order_G = int(G.order())
            order_H = int(H.order())
            p_int = int(p)
            
            # Find the highest power of p dividing |G|
            p_power_G = 1
            while order_G % (p_power_G * p_int) == 0:
                p_power_G *= p_int
                
            # Find the highest power of p dividing |H|
            p_power_H = 1
            while order_H % (p_power_H * p_int) == 0:
                p_power_H *= p_int
                
            # If the Sylow p-subgroups have different orders, they cannot be isomorphic
            if p_power_G != p_power_H:
                neg_q = True
            else:
                # If they have the same order, we must check for isomorphism
                sylow_G = G.sylow_subgroup(p_int)
                sylow_H = H.sylow_subgroup(p_int)
                neg_q = not sylow_G.is_isomorphic(sylow_H)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The orders |N| and |H| are relatively prime",
    "H_2: p is a prime number dividing |H|",
    "¬Q: A Sylow p-subgroup of G is NOT isomorphic to a Sylow p-subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2