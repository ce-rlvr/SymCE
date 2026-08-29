import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def check_normal(G, N):
    try:
        if not N.is_subgroup(G):
            return False
        if not G.is_normal(N):
            return False
        return True
    except Exception:
        pass

    # Fallback manual check if sympy methods fail (e.g., due to degree mismatch)
    try:
        for gen in N.generators:
            if not G.contains(gen):
                return False
        for g in G.generators:
            for n in N.generators:
                if not N.contains(g * n * (~g)):
                    return False
        return True
    except Exception:
        return False

def check_neg_Q(G, N):
    try:
        q_order = G.order() // N.order()
        if G.order() % N.order() != 0:
            return False
        if q_order == 1:
            return False # Trivial group is cyclic, so negation is False
        
        # Check if there is any element g in G whose coset gN has order q_order
        for g in G.generate():
            k = 1
            curr = g
            while True:
                try:
                    in_N = N.contains(curr)
                except Exception:
                    try:
                        in_N = any(curr == n for n in N.generate())
                    except Exception:
                        in_N = False
                
                if in_N:
                    break
                
                curr = curr * g
                k += 1
                if k > q_order:
                    break
            
            if k == q_order:
                # Found a generator for G/N, so G/N is cyclic. Negation is False.
                return False
                
        # No generator found, G/N is NOT cyclic. Negation is True.
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False]
    
    h1_ok = check_normal(G, N)
    neg_q_ok = check_neg_Q(G, N)
    
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: G/N is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1