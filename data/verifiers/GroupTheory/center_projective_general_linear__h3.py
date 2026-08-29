import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer, QQ, RR, CC
from sympy.ntheory import factorint
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_prime_power(q):
    try:
        if not isinstance(q, int) or q < 2:
            return False
        factors = factorint(q)
        return len(factors) == 1
    except Exception:
        return False

def extract_vars(witness):
    F, n, G = None, None, None
    if isinstance(witness, dict):
        F = witness.get('F', witness.get('f'))
        n = witness.get('n')
        G = witness.get('G', witness.get('g'))
        return F, n, G
    
    if isinstance(witness, (list, tuple)):
        if len(witness) == 3:
            F, n, G = witness
            # Attempt to reorder if the user provided them in a different order
            if not (hasattr(G, 'center') or hasattr(G, 'is_group')):
                for i, item in enumerate(witness):
                    if hasattr(item, 'center') or hasattr(item, 'is_group'):
                        G = item
                        others = [x for j, x in enumerate(witness) if j != i]
                        F, n = others[0], others[1]
                        break
            # Ensure n is the integer if F was passed as an integer
            if not isinstance(n, int) and isinstance(F, int):
                F, n = n, F
        else:
            raise ValueError("Witness must be a tuple of length 3")
            
    return F, n, G

def conditions(witness) -> list[bool]:
    try:
        F, n, G = extract_vars(witness)
    except Exception:
        return [False, False, False]
        
    # H_1: F is a field
    h1_ok = False
    try:
        if isinstance(F, str) and (F in ['QQ', 'RR', 'CC'] or F.startswith('GF')):
            h1_ok = True
        elif hasattr(F, 'is_Field') and F.is_Field:
            h1_ok = True
        elif hasattr(F, 'is_field') and F.is_field:
            h1_ok = True
        elif isinstance(F, int) and is_prime_power(F):
            h1_ok = True
        elif F in (QQ, RR, CC):
            h1_ok = True
    except Exception:
        pass

    # H_2: n is an integer such that n >= 2
    h2_ok = False
    try:
        n_val = int(n)
        if n_val >= 2 and n_val == n:
            h2_ok = True
    except Exception:
        pass

    # ¬Q: The center Z(G) is not the trivial subgroup
    neg_q_ok = False
    try:
        if hasattr(G, 'center'):
            C = G.center()
            if hasattr(C, 'order'):
                neg_q_ok = (C.order() > 1)
            elif hasattr(C, '__len__'):
                neg_q_ok = (len(C) > 1)
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: n is an integer such that n >= 2",
    "¬Q: The center Z(G) is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2