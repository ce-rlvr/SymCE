import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    try:
        G, phi = witness
    except Exception:
        return [False, False]
    
    # Extract elements of G
    try:
        if isinstance(G, (list, set, tuple)):
            elements = list(G)
        elif hasattr(G, 'elements'):
            elements = list(G.elements)
        elif hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = list(G)
            
        # Attempt to make elements hashable if they are not (e.g., mutable matrices)
        if elements:
            try:
                hash(elements[0])
            except TypeError:
                elements = [x.as_immutable() if hasattr(x, 'as_immutable') else x for x in elements]
    except Exception:
        return [False, False]

    # Build phi_dict
    try:
        if callable(phi):
            phi_dict = {x: phi(x) for x in elements}
        elif isinstance(phi, dict):
            phi_dict = phi
        else:
            phi_dict = {}
    except Exception:
        phi_dict = {}

    # H_1: phi is an automorphism of G
    h1_ok = False
    try:
        if phi_dict:
            # Check bijection
            is_bijection = (set(phi_dict.keys()) == set(elements) and 
                            set(phi_dict.values()) == set(elements))
            
            # Check homomorphism
            is_homo = True
            for x in elements:
                for y in elements:
                    try:
                        xy = x * y
                    except Exception:
                        xy = x + y
                    
                    try:
                        phix_phiy = phi_dict[x] * phi_dict[y]
                    except Exception:
                        phix_phiy = phi_dict[x] + phi_dict[y]
                        
                    if xy not in phi_dict or phi_dict[xy] != phix_phiy:
                        is_homo = False
                        break
                if not is_homo:
                    break
            h1_ok = is_bijection and is_homo
    except Exception:
        h1_ok = False

    # ¬Q: The set S = {x in G | phi(x) = x} is NOT a subgroup of G
    neg_q_ok = False
    try:
        S = set()
        for x in elements:
            if x in phi_dict and phi_dict[x] == x:
                S.add(x)
                
        if not S:
            is_sub = False
        else:
            is_sub = True
            for x in S:
                # Check inverse
                try:
                    inv = x**-1
                except Exception:
                    try:
                        inv = ~x
                    except Exception:
                        inv = -x
                if inv not in S:
                    is_sub = False
                    break
                
                # Check closure
                for y in S:
                    try:
                        prod = x * y
                    except Exception:
                        prod = x + y
                    if prod not in S:
                        is_sub = False
                        break
                if not is_sub:
                    break
        neg_q_ok = not is_sub
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: phi is an automorphism of G",
    "¬Q: The set S = {x in G | phi(x) = x} is not a subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1