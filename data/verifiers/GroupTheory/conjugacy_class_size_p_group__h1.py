import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings that the witness expression may reference.
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

def is_power_of_p(n, p):
    try:
        n = int(n)
        p = int(p)
        if n < 1:
            return False
        if p == 1:
            return n == 1
        if p in (0, -1):
            return n == 1
        if p <= 1 and n > 1:
            return False
        while n % p == 0:
            n = n // p
        return n == 1
    except Exception:
        return False

def get_class_size(G, x):
    # Try using the built-in centralizer if available
    try:
        C = G.centralizer(x)
        return G.order() // C.order()
    except Exception:
        pass
    
    # Fallback to computing the orbit of x under conjugation by generators
    try:
        orbit = {x}
        queue = [x]
        gens = G.generators
        while queue:
            curr = queue.pop(0)
            for g in gens:
                conj = (g**-1) * curr * g
                if conj not in orbit:
                    orbit.add(conj)
                    queue.append(conj)
        return len(orbit)
    except TypeError:
        # If elements are unhashable (e.g. mutable matrices)
        orbit = [x]
        queue = [x]
        gens = G.generators
        while queue:
            curr = queue.pop(0)
            for g in gens:
                conj = (g**-1) * curr * g
                if conj not in orbit:
                    orbit.append(conj)
                    queue.append(conj)
        return len(orbit)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)):
            return [False, False, False]
            
        if len(witness) not in (2, 3):
            return [False, False, False]
            
        # Identify the group G in the witness
        G_idx = -1
        for i, item in enumerate(witness):
            if hasattr(item, 'order') and hasattr(item, 'generators'):
                G_idx = i
                break
        if G_idx == -1:
            return [False, False, False]
            
        G = witness[G_idx]
        other_items = [witness[i] for i in range(len(witness)) if i != G_idx]
        
        # Determine possible assignments for x and p
        if len(witness) == 3:
            possible_assignments = [
                (other_items[0], other_items[1]),
                (other_items[1], other_items[0])
            ]
        else:
            # If p is omitted, infer it as the order of the group
            possible_assignments = [
                (other_items[0], G.order())
            ]
            
        best_result = [False, False, False]
        for x_cand, p_cand in possible_assignments:
            if not isinstance(p_cand, (int, sympy.Integer)):
                continue
                
            p_val = int(p_cand)
            
            # H_1: G is a finite p-group
            try:
                order = G.order()
                if order < 1:
                    h1 = False
                else:
                    h1 = is_power_of_p(order, p_val)
            except Exception:
                h1 = False
                
            # H_2: x is an element of G
            try:
                if hasattr(G, 'contains'):
                    h2 = bool(G.contains(x_cand))
                elif hasattr(G, 'elements'):
                    h2 = x_cand in G.elements
                else:
                    h2 = x_cand in G
            except Exception:
                h2 = False
                
            # ¬Q: The size of the conjugacy class of x in G is NOT a power of p
            try:
                c_size = get_class_size(G, x_cand)
                neg_q = not is_power_of_p(c_size, p_val)
            except Exception:
                neg_q = False
                
            result = [h1, h2, neg_q]
            if result == [True, True, True]:
                return result
            if sum(result) > sum(best_result):
                best_result = result
                
        return best_result

    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G is a finite p-group",
    "H_2: x is an element of G",
    "¬Q: The size of the conjugacy class of x in G is not a power of p"
]

N_HYP = 2
NEG_Q_INDEX = 2