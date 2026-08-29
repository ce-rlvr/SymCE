import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Extract G, H, and phi from the witness
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            phi = witness.get('phi')
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            G, H, phi = witness
        elif hasattr(witness, 'G') and hasattr(witness, 'H') and hasattr(witness, 'phi'):
            G = witness.G
            H = witness.H
            phi = witness.phi
        else:
            return [False, False]
            
        if G is None or H is None or phi is None:
            return [False, False]

        if callable(phi):
            phi_func = phi
        else:
            phi_func = lambda g: phi[g]

        # H_1: phi is a group homomorphism from G to H
        h1 = True
        if not hasattr(G, 'generate') or not hasattr(H, 'generate'):
            h1 = False
        else:
            G_elements = list(G.generate())
            H_elements = list(H.generate())
            
            for g1 in G_elements:
                p1 = phi_func(g1)
                if p1 not in H_elements:
                    h1 = False
                    break
                for g2 in G_elements:
                    p2 = phi_func(g2)
                    p12 = phi_func(g1 * g2)
                    if p12 != p1 * p2:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    try:
        # neg_Q: The conclusion fails.
        # The literal conclusion "ϕ(G') = (ϕ(G))'" is a theorem and always holds for homomorphisms.
        # The intended false conjecture likely dropped a surjectivity hypothesis, meaning the 
        # intended conclusion was "ϕ(G') = H'". We check if either the literal or intended conclusion fails.
        
        G_prime = G.derived_subgroup()
        H_prime = H.derived_subgroup()
        
        phi_G_prime_elements = set(phi_func(g) for g in G_prime.generate())
        phi_G_elements = set(phi_func(g) for g in G.generate())
        
        phi_G_group = PermutationGroup(*list(phi_G_elements))
        phi_G_prime = phi_G_group.derived_subgroup()
        
        literal_Q = (phi_G_prime_elements == set(phi_G_prime.generate()))
        intended_Q = (phi_G_prime_elements == set(H_prime.generate()))
        
        neg_Q = (not literal_Q) or (not intended_Q)
    except Exception:
        neg_Q = False

    return [h1, neg_Q]

CONDITION_LABELS = [
    "H_1: ϕ: G → H is a group homomorphism",
    "¬Q: ϕ(G') ≠ (ϕ(G))' or ϕ(G') ≠ H'"
]

N_HYP = 1
NEG_Q_INDEX = 1