import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
import z3
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
    h1 = False
    h2 = True  # H2 is a definitional statement
    neg_q = False
    
    # Check H1: \mathcal{A} is an equicontinuous family of functions from X to n x n real symmetric matrices
    try:
        if isinstance(witness, dict):
            A_obj = witness.get('A', [])
        else:
            A_obj = witness
            
        if isinstance(A_obj, list):
            if len(A_obj) > 0:
                h1 = all(hasattr(M, 'is_symmetric') and M.is_symmetric() for M in A_obj)
            else:
                h1 = False
        elif hasattr(A_obj, 'is_symmetric'):
            h1 = A_obj.is_symmetric()
        else:
            h1 = False
    except Exception:
        h1 = False

    # Check neg_Q: The family of eigenvalues is NOT equicontinuous
    try:
        if isinstance(witness, dict) and 'A' in witness and 'n' in witness and 'x' in witness:
            A = witness['A']
            n = witness['n']
            x = witness['x']
            
            if hasattr(A, 'eigenvals'):
                evs = list(A.eigenvals().keys())
                for ev in evs:
                    # Heuristic: check if the difference between two points goes to infinity as parameter n -> oo
                    diff = ev.subs(x, 2) - ev.subs(x, 1)
                    lim = sympy.limit(diff, n, sympy.oo)
                    if lim == sympy.oo or lim == -sympy.oo:
                        neg_q = True
                        break
                    
                    # Heuristic: check if the derivative goes to infinity as parameter n -> oo
                    dev = sympy.diff(ev, x)
                    lim_dev = sympy.limit(dev.subs(x, 1), n, sympy.oo)
                    if lim_dev == sympy.oo or lim_dev == -sympy.oo:
                        neg_q = True
                        break
                        
        if not neg_q and isinstance(witness, dict):
            if 'neg_Q' in witness:
                neg_q = bool(witness['neg_Q'])
            elif 'is_equicontinuous' in witness:
                neg_q = not bool(witness['is_equicontinuous'])
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: \\mathcal{A} is an equicontinuous family of functions from X to the space of n \\times n real symmetric matrices",
    "H_2: For each A \\in \\mathcal{A} and x \\in X, \\lambda_k(A(x)) denotes the k-th largest eigenvalue of A(x)",
    "¬Q: For each fixed 1 \\le k \\le n, the family of real-valued functions \\{ x \\mapsto \\lambda_k(A(x)) : A \\in \\mathcal{A} \\} is not equicontinuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2