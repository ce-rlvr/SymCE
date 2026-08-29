import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# Custom group descriptions for infinite groups and simple modular arithmetic
Z = "Z"

def Zn(n):
    return ("Zn", n)

def Sn(n):
    return ("Sn", n)

def get_group(desc):
    """
    Returns a tuple of (op, inv, id_el, contains_func, sample_func) for the given group description.
    """
    if desc == "Z":
        def op(a, b): return a + b
        def inv(a): return -a
        id_el = 0
        def contains(a): return isinstance(a, int)
        def sample(): return list(range(-20, 21))
        return op, inv, id_el, contains, sample
        
    elif isinstance(desc, tuple) and len(desc) == 2 and desc[0] == "Zn":
        n = desc[1]
        def op(a, b): return (a + b) % n
        def inv(a): return (-a) % n
        id_el = 0
        def contains(a): return isinstance(a, int) and 0 <= a < n
        def sample(): return list(range(n))
        return op, inv, id_el, contains, sample
        
    elif isinstance(desc, tuple) and len(desc) == 2 and desc[0] == "Sn":
        n = desc[1]
        S = SymmetricGroup(n)
        def op(a, b): return a * b
        def inv(a): return ~a
        id_el = S.identity
        def contains(a): return a in S
        def sample():
            elts = []
            gen = S.generate() if hasattr(S, 'generate') and callable(S.generate) else S.elements
            for i, e in enumerate(gen):
                if i >= 100: break
                elts.append(e)
            return elts
        return op, inv, id_el, contains, sample
        
    elif isinstance(desc, PermutationGroup):
        def op(a, b): return a * b
        def inv(a): return ~a
        id_el = desc.identity
        def contains(a): return a in desc
        def sample():
            elts = []
            gen = desc.generate() if hasattr(desc, 'generate') and callable(desc.generate) else desc.elements
            for i, e in enumerate(gen):
                if i >= 100: break
                elts.append(e)
            return elts
        return op, inv, id_el, contains, sample
        
    else:
        raise ValueError("Unknown group description")

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (G_desc, H_desc, phi, g), checks if it is a valid counterexample.
    """
    try:
        G_desc, H_desc, phi, g = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G and H are groups
    try:
        G_op, G_inv, G_id, G_contains, G_sample = get_group(G_desc)
        H_op, H_inv, H_id, H_contains, H_sample = get_group(H_desc)
        h1 = True
    except Exception:
        h1 = False
        return [False, False, False]
        
    # H_2: phi is a group homomorphism from G to H
    try:
        h2 = True
        if not G_contains(g):
            h2 = False
            
        if isinstance(phi, dict):
            def phi_func(x): return phi[x]
        else:
            phi_func = phi
            
        sample = G_sample()
        for a in sample:
            phi_a = phi_func(a)
            if not H_contains(phi_a):
                h2 = False
                break
            for b in sample:
                phi_b = phi_func(b)
                ab = G_op(a, b)
                phi_ab = phi_func(ab)
                if phi_ab != H_op(phi_a, phi_b):
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False
        
    # neg_Q: The order of phi(g) in H is finite and divides the order of g (MUST FAIL)
    try:
        def get_order(el, op, id_el, max_order=1000):
            if hasattr(el, 'order') and callable(el.order):
                try:
                    return el.order()
                except Exception:
                    pass
            if el == id_el:
                return 1
            curr = el
            for i in range(2, max_order + 1):
                curr = op(curr, el)
                if curr == id_el:
                    return i
            return float('inf')
            
        order_g = get_order(g, G_op, G_id)
        phi_g = phi_func(g)
        order_phi_g = get_order(phi_g, H_op, H_id)
        
        if order_phi_g == float('inf'):
            conclusion_holds = False
        elif order_g == float('inf'):
            # Divisibility is defined for integers; a finite integer cannot divide infinity.
            conclusion_holds = False
        else:
            conclusion_holds = (order_g % order_phi_g == 0)
            
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: phi is a group homomorphism from G to H",
    "¬Q: The order of phi(g) in H is not finite, or does not divide the order of g"
]

N_HYP = 2
NEG_Q_INDEX = 2