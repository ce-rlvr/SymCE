import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

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

CONDITION_LABELS = [
    "H_1: G is a finite subgroup of U(R)",
    "¬Q: G is not cyclic"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1_ok = False
    neg_q_ok = False
    
    try:
        if hasattr(witness, 'elements'):
            raw_G = list(witness.elements)
        elif hasattr(witness, 'generate') and callable(witness.generate):
            raw_G = list(witness.generate())
        else:
            raw_G = list(witness)
            
        if not raw_G:
            return [False, False]
            
        # Remove duplicates
        G = []
        for x in raw_G:
            if x not in G:
                G.append(x)
                
        n = len(G)
        if n == 0:
            return [False, False]
            
        # Check closure
        closed = True
        for a in G:
            for b in G:
                c = a * b
                if c not in G:
                    closed = False
                    break
            if not closed:
                break
                
        if closed:
            # Find identity
            identity = None
            for e in G:
                is_id = True
                for a in G:
                    if e * a != a or a * e != a:
                        is_id = False
                        break
                if is_id:
                    identity = e
                    break
            
            if identity is not None:
                # Check inverses
                inverses_ok = True
                for a in G:
                    has_inv = False
                    for b in G:
                        if a * b == identity and b * a == identity:
                            has_inv = True
                            break
                    if not has_inv:
                        inverses_ok = False
                        break
                
                if inverses_ok:
                    h1_ok = True
                    
                    # Now check if it's cyclic
                    is_cyclic = False
                    for a in G:
                        curr = a
                        order = 1
                        while curr != identity and order <= n:
                            curr = curr * a
                            order += 1
                        if order == n:
                            is_cyclic = True
                            break
                    
                    neg_q_ok = not is_cyclic

    except Exception:
        pass

    return [h1_ok, neg_q_ok]