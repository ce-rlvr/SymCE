import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup([Permutation()])

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(G):
    if hasattr(G, 'elements'):
        if callable(G.elements):
            return list(G.elements())
        else:
            return list(G.elements)
    elif hasattr(G, 'generate'):
        return list(G.generate())
    return []

def get_identity(G, elements=None):
    if hasattr(G, 'identity'):
        return G.identity
    if elements is None:
        elements = get_elements(G)
    for g in elements:
        try:
            if g * g == g:
                return g
        except Exception:
            pass
    return None

def is_torsion_free_nilpotent(G):
    is_nilp = False
    if hasattr(G, 'is_nilpotent'):
        is_nilp = G.is_nilpotent() if callable(G.is_nilpotent) else G.is_nilpotent
    else:
        if hasattr(G, 'order'):
            order = G.order() if callable(G.order) else G.order
            if order == 1:
                is_nilp = True
                
    if not is_nilp:
        return False
        
    is_tf = True
    if hasattr(G, 'is_torsion_free'):
        is_tf = G.is_torsion_free() if callable(G.is_torsion_free) else G.is_torsion_free
    else:
        elements = get_elements(G)
        if elements:
            identity = get_identity(G, elements)
            for g in elements:
                if g != identity:
                    if hasattr(g, 'order'):
                        o = g.order() if callable(g.order) else g.order
                        if o > 1:
                            is_tf = False
                            break
        elif hasattr(G, 'order'):
            order = G.order() if callable(G.order) else G.order
            if order > 1:
                is_tf = False
                
    return is_tf

def conclusion_fails(G, H):
    if hasattr(G, 'isolator'):
        isolator = G.isolator(H)
    else:
        order = G.order() if callable(G.order) else G.order
        order = int(order)
        isolator = []
        elements = get_elements(G)
        for x in elements:
            curr = x
            found = False
            for n in range(1, order + 2):
                if curr in H:
                    found = True
                    break
                try:
                    curr = curr * x
                except Exception:
                    break
            if found:
                isolator.append(x)
                
    if hasattr(G, 'is_subgroup'):
        return not G.is_subgroup(isolator)
    else:
        if not isolator:
            return True
            
        identity = get_identity(G)
        if identity is not None and identity not in isolator:
            return True
            
        for a in isolator:
            for b in isolator:
                try:
                    if a * b not in isolator:
                        return True
                except Exception:
                    return True
        for a in isolator:
            try:
                if a**-1 not in isolator:
                    return True
            except Exception:
                return True
        return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, H) where G is a group and H is a subset.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            G = witness.G
            H = witness.H
    except Exception:
        return [False, False]
        
    h1 = False
    try:
        h1 = bool(is_torsion_free_nilpotent(G))
    except Exception:
        pass
        
    neg_q = False
    try:
        neg_q = bool(conclusion_fails(G, H))
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a torsion-free nilpotent group",
    "¬Q: I(H) is not a subgroup of G"
]
N_HYP = 1
NEG_Q_INDEX = 1