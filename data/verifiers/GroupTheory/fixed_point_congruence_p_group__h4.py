import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (G, p) or (G, X, p), or a dict 
    with keys 'P' (or 'G'), 'p', and optionally 'X'.
    """
    G = None
    p = None
    X_obj = None
    
    try:
        if isinstance(witness, dict):
            G = witness.get('P', witness.get('G'))
            p = witness.get('p')
            X_obj = witness.get('X')
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                G, p = witness
            elif len(witness) == 3:
                G, X_obj, p = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        if isinstance(G, list):
            G = PermutationGroup(G)
    except Exception:
        return [False, False, False, False]

    # H1: P is a finite p-group
    # In the context of the dropped hypothesis ("p is prime"), 
    # we check if the order of P is a power of the given p.
    h1 = False
    try:
        if p is not None:
            p_val = int(p)
            if p_val > 1 and hasattr(G, 'order'):
                order = int(G.order())
                temp = order
                while temp > 0 and temp % p_val == 0:
                    temp //= p_val
                if temp == 1:
                    h1 = True
    except Exception:
        h1 = False

    # H2: X is a finite set
    h2 = False
    X_size = 0
    try:
        if hasattr(G, 'degree'):
            X_size = int(G.degree)
            if X_obj is not None:
                if isinstance(X_obj, (int, sympy.Integer)):
                    X_size = max(X_size, int(X_obj))
                elif hasattr(X_obj, '__len__'):
                    X_size = max(X_size, len(X_obj))
            if X_size >= 0:
                h2 = True
    except Exception:
        h2 = False

    # H3: P acts on X
    h3 = False
    try:
        if isinstance(G, PermutationGroup):
            h3 = True
    except Exception:
        h3 = False

    # neg_Q: |X| \not\equiv |X^P| \pmod p
    neg_q = False
    try:
        if h2 and h3 and p is not None:
            p_val = int(p)
            # Any points in X beyond G.degree are implicitly fixed by G
            fixed_points = X_size - int(G.degree)
            for i in range(int(G.degree)):
                # A point is fixed if it is fixed by all generators of G
                if all(gen(i) == i for gen in G.generators):
                    fixed_points += 1
            
            if (X_size % p_val) != (fixed_points % p_val):
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: P is a finite p-group",
    "H_2: X is a finite set",
    "H_3: P acts on X",
    "¬Q: |X| is not congruent to |X^P| mod p"
]

N_HYP = 3
NEG_Q_INDEX = 3