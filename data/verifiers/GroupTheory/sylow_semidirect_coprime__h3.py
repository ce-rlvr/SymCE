import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
from sympy.ntheory import primefactors, isprime

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
    h1_ok = False
    h2_ok = False
    h3_ok = False
    neg_q = False
    
    try:
        # Witness can be (G, N, H) or (G, N, H, p)
        if len(witness) == 4:
            G, N, H, p = witness
            if isprime(p):
                primes = [p]
            else:
                primes = []
        elif len(witness) == 3:
            G, N, H = witness
            primes = primefactors(G.order())
        else:
            return [False, False, False, False]
            
        # H1: G is a finite group, N is a normal subgroup, and H is a subgroup
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup):
            if N.is_subgroup(G) and H.is_subgroup(G) and N.is_normal(G):
                h1_ok = True
                
        # H2: G is the semidirect product of N and H
        if h1_ok:
            if N.order() * H.order() == G.order():
                if math.gcd(N.order(), H.order()) == 1:
                    h2_ok = True
                else:
                    try:
                        if len(set(N.elements).intersection(set(H.elements))) == 1:
                            h2_ok = True
                    except Exception:
                        pass
                        
        # H3: The orders of N and H are relatively prime
        if h1_ok:
            if math.gcd(N.order(), H.order()) == 1:
                h3_ok = True
                
        # ¬Q: There exists a Sylow p-subgroup of G that is not conjugate to a Sylow p-subgroup of H.
        # Two finite groups can only be conjugate if they have the same order.
        # If the highest power of p dividing |G| differs from that dividing |H|, 
        # their Sylow p-subgroups have different orders and thus cannot be conjugate.
        if h1_ok:
            for pr in primes:
                order_G = G.order()
                pow_G = 1
                while order_G % pr == 0:
                    pow_G *= pr
                    order_G //= pr
                
                order_H = H.order()
                pow_H = 1
                while order_H % pr == 0:
                    pow_H *= pr
                    order_H //= pr
                
                if pow_G != pow_H:
                    neg_q = True
                    break
                    
    except Exception:
        pass
        
    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group, N is a normal subgroup, and H is a subgroup",
    "H_2: G is the semidirect product of N and H",
    "H_3: The orders of N and H are relatively prime",
    "¬Q: There exists a Sylow p-subgroup of G that is not conjugate to a Sylow p-subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3