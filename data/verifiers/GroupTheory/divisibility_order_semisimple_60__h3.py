import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
)
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

def is_finite_group(G):
    """Check if G is a finite group."""
    try:
        return hasattr(G, 'order') and G.order() > 0
    except Exception:
        return False

def is_semisimple(G):
    """
    Check if G is a semisimple finite group.
    A finite group is semisimple if it has no non-trivial abelian normal subgroups.
    Equivalently, for every non-identity element g, its normal closure is non-abelian.
    The normal closure of g is abelian iff its conjugacy class mutually commutes.
    """
    try:
        if not hasattr(G, 'order') or not hasattr(G, 'generators') or not hasattr(G, 'identity'):
            return False
            
        if G.order() == 1:
            return True
            
        # Limit order to prevent timeouts on extremely large groups
        if G.order() > 5000:
            return False
            
        elements = list(G.generate())
        id_el = G.identity
        checked = set()
        
        gens = G.generators
        gens_inv = [~gen for gen in gens]
        
        for g in elements:
            if g == id_el or g in checked:
                continue
                
            # BFS to find the conjugacy class of g
            C = {g}
            queue = [g]
            while queue:
                curr = queue.pop(0)
                for gen, gen_inv in zip(gens, gens_inv):
                    # Conjugate by generator
                    conj1 = gen * curr * gen_inv
                    if conj1 not in C:
                        C.add(conj1)
                        queue.append(conj1)
                    # Conjugate by inverse of generator
                    conj2 = gen_inv * curr * gen
                    if conj2 not in C:
                        C.add(conj2)
                        queue.append(conj2)
            
            checked.update(C)
            
            # Check if the conjugacy class mutually commutes
            commutes = True
            C_list = list(C)
            for i in range(len(C_list)):
                for j in range(i + 1, len(C_list)):
                    if C_list[i] * C_list[j] != C_list[j] * C_list[i]:
                        commutes = False
                        break
                if not commutes:
                    break
                    
            if commutes:
                # Found a non-trivial element whose normal closure is abelian
                return False
                
        return True
    except Exception:
        return False

def neg_q(G):
    """Check if the conclusion FAILS (order of G is NOT an integer multiple of 60)."""
    try:
        return G.order() % 60 != 0
    except Exception:
        return False

def conditions(witness):
    return [
        is_finite_group(witness),
        is_semisimple(witness),
        neg_q(witness)
    ]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "¬Q: The order of G is not an integer multiple of 60"
]

N_HYP = 2
NEG_Q_INDEX = 2