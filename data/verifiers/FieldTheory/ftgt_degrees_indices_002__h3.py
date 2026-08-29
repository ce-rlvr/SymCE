import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def check_subgroup(sub, group):
    """Safely check if sub is a subgroup of group, handling degree mismatches."""
    try:
        if sub.is_subgroup(group):
            return True
    except Exception:
        pass
    try:
        for gen in sub.generators:
            p_array = gen.array_form
            if len(p_array) < group.degree:
                p_array = p_array + list(range(len(p_array), group.degree))
            elif len(p_array) > group.degree:
                if any(p_array[i] != i for i in range(group.degree, len(p_array))):
                    return False
                p_array = p_array[:group.degree]
            p = Permutation(p_array)
            if p not in group:
                return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # Try group-based witness first (Galois correspondence representation)
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            E = witness.get('E') or witness.get('E_subgroup')
            H = witness.get('H')
        elif isinstance(witness, tuple) and len(witness) == 3:
            G, E, H = witness
        elif isinstance(witness, tuple) and len(witness) == 5:
            _, _, E, G, H = witness
        else:
            G, E, H = None, None, None

        if G is not None and E is not None and H is not None:
            # H1: K/F is a finite Galois extension with Galois group G
            # (Implicitly requires H to be a subgroup of G for index to be well-defined)
            h1_base = hasattr(G, 'order') and hasattr(G, 'is_subgroup')
            h_is_subgroup = check_subgroup(H, G)
            h1 = h1_base and h_is_subgroup
            
            # H2: E is an intermediate field such that F is a subfield of E and E is a subfield of K
            h2 = check_subgroup(E, G)
            
            deg_K_E = E.order()
            deg_E_F = G.order() // E.order()
            
            order_H = H.order()
            index_G_H = G.order() // H.order()
            
            q = (deg_K_E == order_H) and (deg_E_F == index_G_H)
            
            return [bool(h1), bool(h2), not q]
    except Exception:
        pass

    # Fallback to numeric witness (abstract degrees and indices)
    try:
        if isinstance(witness, dict):
            deg_K_E = witness['deg_K_E']
            deg_E_F = witness['deg_E_F']
            order_H = witness['order_H']
            index_G_H = witness['index_G_H']
        elif isinstance(witness, tuple) and len(witness) == 4:
            deg_K_E, deg_E_F, order_H, index_G_H = witness
        else:
            return [False, False, False]
            
        order_G = deg_K_E * deg_E_F
        h1 = (order_G == order_H * index_G_H) and order_G > 0
        h2 = deg_K_E > 0 and deg_E_F > 0
        
        q = (deg_K_E == order_H) and (deg_E_F == index_G_H)
        return [bool(h1), bool(h2), not q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: K over F is a finite Galois extension with Galois group G",
    "H_2: E is an intermediate field such that F is a subfield of E and E is a subfield of K",
    "not Q: The degree of K over E != |H| or degree of E over F != index of H in G"
]

N_HYP = 2
NEG_Q_INDEX = 2