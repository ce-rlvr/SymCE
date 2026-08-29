import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and fails the conclusion.
    Witness is expected to be a tuple (G, H, P, p) or an object with these attributes.
    """
    if isinstance(witness, tuple):
        if len(witness) == 4:
            G, H, P, p = witness
        else:
            return [False, False, False]
    else:
        try:
            G = witness.G
            H = witness.H
            P = witness.P
            p = witness.p
        except AttributeError:
            return [False, False, False]

    def get_elements(group):
        if hasattr(group, 'order') and group.order() in (float('inf'), sympy.oo):
            raise ValueError("Group is infinite")
        if hasattr(group, 'generate') and callable(group.generate):
            return list(group.generate())
        elif hasattr(group, 'elements'):
            return list(group.elements)
        else:
            return list(group)

    def inverse(g):
        if hasattr(g, 'inv'):
            return g.inv()
        if isinstance(g, (int, sympy.Integer)):
            raise TypeError("Cannot invert integer without group context")
        try:
            return ~g
        except Exception:
            return g**-1

    def check_h1():
        try:
            # Fast path for SymPy PermutationGroup
            if hasattr(H, 'is_normal'):
                if hasattr(H, 'is_subgroup') and not H.is_subgroup(G):
                    return False
                return H.is_normal(G)
            
            # Custom object method
            if hasattr(G, 'is_normal_subgroup'):
                return G.is_normal_subgroup(H)
            
            # Fallback to element-wise check
            G_elems = get_elements(G)
            H_elems = get_elements(H)
            
            for h in H_elems:
                if h not in G_elems:
                    return False
                    
            for g in G_elems:
                for h in H_elems:
                    if g * h * inverse(g) not in H_elems:
                        return False
            return True
        except Exception:
            return False

    def check_h2():
        try:
            if not isprime(p):
                return False
            
            # Custom object method
            if hasattr(P, 'is_Sylow'):
                return P.is_Sylow(H, p)
                
            # Fast path for SymPy PermutationGroup
            if hasattr(P, 'is_subgroup') and hasattr(P, 'order') and hasattr(H, 'order'):
                if not P.is_subgroup(H):
                    return False
                order_H = H.order()
                order_P = P.order()
            else:
                # Fallback to element-wise check
                H_elems = get_elements(H)
                P_elems = get_elements(P)
                for p_elem in P_elems:
                    if p_elem not in H_elems:
                        return False
                order_H = len(H_elems)
                order_P = len(P_elems)
                
            if order_H == float('inf') or order_H == sympy.oo:
                return False
                
            k = 0
            temp = order_H
            while temp > 0 and temp % p == 0:
                k += 1
                temp //= p
                
            return order_P == p**k
        except Exception:
            return False

    def check_neg_q():
        try:
            # Custom object methods
            if hasattr(G, 'equals_H_N_G_P'):
                return not G.equals_H_N_G_P(H, P)
            if hasattr(G, 'Frattini_argument_holds'):
                return not G.Frattini_argument_holds(H, P)
            
            # Fallback to element-wise check
            G_elems = get_elements(G)
            H_elems = get_elements(H)
            P_elems = get_elements(P)
            
            # Compute N_G(P)
            N_G_P = []
            for g in G_elems:
                normalizes = True
                for p_elem in P_elems:
                    conj = g * p_elem * inverse(g)
                    if conj not in P_elems:
                        normalizes = False
                        break
                if normalizes:
                    N_G_P.append(g)
                    
            # Compute H N_G(P)
            H_N_G_P = []
            for h in H_elems:
                for n in N_G_P:
                    prod = h * n
                    if prod not in H_N_G_P:
                        H_N_G_P.append(prod)
                        
            # Unique elements in G
            G_elems_unique = []
            for g in G_elems:
                if g not in G_elems_unique:
                    G_elems_unique.append(g)
                    
            # G != H N_G(P)
            return len(H_N_G_P) != len(G_elems_unique)
        except Exception:
            return False

    return [check_h1(), check_h2(), check_neg_q()]

CONDITION_LABELS = [
    "H_1: H is a normal subgroup of G",
    "H_2: P is a Sylow p-subgroup of H",
    "¬Q: G != H N_G(P)"
]

N_HYP = 2
NEG_Q_INDEX = 2