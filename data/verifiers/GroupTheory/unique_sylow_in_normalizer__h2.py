import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, P, p) where:
      - G is a finite group (PermutationGroup)
      - P is a subgroup of G (PermutationGroup)
      - p is a prime number
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False]
        G, P, p = witness
    except Exception:
        return [False, False]
        
    # H_1: G is a finite group, P is a subgroup of G, and p is a prime
    try:
        h1 = False
        if isinstance(G, PermutationGroup) and isinstance(P, PermutationGroup) and isprime(p):
            if hasattr(P, 'is_subgroup'):
                h1 = P.is_subgroup(G)
            else:
                h1 = set(P.elements).issubset(set(G.elements))
    except Exception:
        h1 = False
        
    # ¬Q: P is not the unique Sylow p-subgroup of N_G(P)
    try:
        if not h1:
            neg_q = False
        else:
            P_elems = set(P.elements)
            P_order = len(P_elems)
            P_gens = P.generators
            
            # Check if P is a p-group
            is_p_group = True
            temp = P_order
            while temp > 1:
                if temp % p != 0:
                    is_p_group = False
                    break
                temp //= p
                
            if not is_p_group:
                # If P is not a p-group, it cannot be a Sylow p-subgroup
                neg_q = True
            else:
                # Calculate the order of the normalizer N_G(P)
                n_order = 0
                for g in G.elements:
                    g_inv = ~g
                    # g normalizes P iff g * x * g^-1 is in P for all generators x of P
                    if all((g * x * g_inv) in P_elems for x in P_gens):
                        n_order += 1
                
                # P is normal in N_G(P). A normal Sylow p-subgroup is always unique.
                # Thus, P is the unique Sylow p-subgroup of N_G(P) iff P is a Sylow p-subgroup of N_G(P).
                # P is a Sylow p-subgroup of N_G(P) iff p does not divide |N_G(P)| / |P|.
                if n_order % (P_order * p) == 0:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group, P is a subgroup of G, and p is a prime",
    "¬Q: P is not the unique Sylow p-subgroup of N_G(P)"
]

N_HYP = 1
NEG_Q_INDEX = 1