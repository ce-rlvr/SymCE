import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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

def get_f(f, x):
    """Helper to evaluate the homomorphism whether it's a dict or a callable."""
    if callable(f):
        return f(x)
    return f[x]

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Witness is expected to be a tuple: (G, H, f, A)
    """
    try:
        G, H, f, A = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G and H are groups
    try:
        h1 = True
        # Extract elements for G
        if hasattr(G, "generate"):
            G_elems = list(G.generate())
        elif hasattr(G, "elements"):
            G_elems = list(G.elements)
        else:
            G_elems = list(G)
            
        # Extract elements for H
        if hasattr(H, "generate"):
            H_elems = list(H.generate())
        elif hasattr(H, "elements"):
            H_elems = list(H.elements)
        else:
            H_elems = list(H)
            
        if not G_elems or not H_elems:
            h1 = False
            
        # Verify group axioms for G
        G_id = None
        if h1:
            for g in G_elems:
                if all(g * x == x for x in G_elems):
                    G_id = g
                    break
            if G_id is None:
                h1 = False
                
        if h1:
            for g in G_elems:
                if not any(g * x == G_id for x in G_elems):
                    h1 = False
                    break
                    
        if h1:
            for x in G_elems:
                for y in G_elems:
                    if x * y not in G_elems:
                        h1 = False
                        break
                if not h1:
                    break
                    
        # Verify group axioms for H
        H_id = None
        if h1:
            for h in H_elems:
                if all(h * x == x for x in H_elems):
                    H_id = h
                    break
            if H_id is None:
                h1 = False
                
        if h1:
            for h in H_elems:
                if not any(h * x == H_id for x in H_elems):
                    h1 = False
                    break
                    
        if h1:
            for x in H_elems:
                for y in H_elems:
                    if x * y not in H_elems:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: f: G -> H is a group homomorphism
    try:
        h2 = True
        for x in G_elems:
            try:
                fx = get_f(f, x)
                if fx not in H_elems:
                    h2 = False
                    break
            except Exception:
                h2 = False
                break
        if h2:
            for x in G_elems:
                for y in G_elems:
                    if get_f(f, x * y) != get_f(f, x) * get_f(f, y):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # ¬Q: f^{-1}(f(A)) != A ker(f)
    try:
        try:
            if hasattr(A, "generate"):
                A_elems = list(A.generate())
            elif hasattr(A, "elements"):
                A_elems = list(A.elements)
            else:
                A_elems = list(A)
        except Exception:
            A_elems = []
            
        ker_f = {x for x in G_elems if get_f(f, x) == H_id}
        
        f_A = set()
        for a in A_elems:
            try:
                f_A.add(get_f(f, a))
            except Exception:
                pass
                
        preimage = {x for x in G_elems if get_f(f, x) in f_A}
        
        A_ker_f = set()
        for a in A_elems:
            for k in ker_f:
                try:
                    A_ker_f.add(a * k)
                except Exception:
                    pass
                    
        neg_q = preimage != A_ker_f
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G -> H is a group homomorphism",
    "¬Q: f^{-1}(f(A)) != A ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2