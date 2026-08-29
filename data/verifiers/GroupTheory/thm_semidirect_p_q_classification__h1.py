import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup for potential witness expressions
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

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        p, q = witness
        p = int(p)
        q = int(q)
    except Exception:
        return [False, False]
        
    try:
        h1 = ((p - 1) % q == 0)
    except Exception:
        h1 = False
        
    try:
        if p < 2 or q < 1:
            # If p < 2 or q < 1, there are 0 non-abelian semidirect products.
            # 0 != 1, so the conclusion fails.
            neg_q = True
        else:
            # The number of non-isomorphic non-abelian semidirect products of C_p by C_q
            # corresponds to the number of non-trivial cyclic subgroups of Aut(C_p) 
            # (which is isomorphic to U(p)) of order dividing q.
            subgroups = set()
            for k in range(1, p):
                if math.gcd(k, p) == 1:
                    # Check if the order of k divides q
                    if pow(k, q, p) == 1:
                        sg = set()
                        curr = 1
                        while curr not in sg:
                            sg.add(curr)
                            curr = (curr * k) % p
                        subgroups.add(frozenset(sg))
            
            non_trivial = [sg for sg in subgroups if len(sg) > 1]
            count = len(non_trivial)
            
            # The conclusion states there is EXACTLY ONE such group.
            # The negation is that the count is NOT exactly 1.
            neg_q = (count != 1)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: q divides p - 1",
    "¬Q: The number of non-abelian semidirect products of C_p by C_q up to isomorphism is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1