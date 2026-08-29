import sympy
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and if it FAILS the conclusion.
    """
    # Try to interpret witness as an FpGroup
    try:
        if hasattr(witness, 'generators') and hasattr(witness, 'relators'):
            G = witness
            X = G.generators
            R = G.relators
            n = len(X)
            
            # H1: X is a set of n distinct generators
            h1_ok = (len(set(X)) == n)
            
            # H2: R = {x_i x_j x_i^{-1} x_j^{-1} | 1 <= i < j <= n}
            expected_R = set()
            for i in range(n):
                for j in range(i + 1, n):
                    expected_R.add(X[i] * X[j] * X[i]**-1 * X[j]**-1)
                    
            h2_ok = (set(R) == expected_R)
            
            # Q: The group defined by <X | R> is isomorphic to the free abelian group of rank n.
            # Check if G is abelian and its abelian invariants are [0]*n
            invs = G.abelian_invariants()
            is_abelian = True
            for i in range(n):
                for j in range(i + 1, n):
                    word = X[i] * X[j] * X[i]**-1 * X[j]**-1
                    if not G.reduce(word).is_identity:
                        is_abelian = False
                        break
                if not is_abelian:
                    break
                    
            is_iso = is_abelian and (invs == [0]*n)
            neg_q_ok = not is_iso
            
            return [h1_ok, h2_ok, neg_q_ok]
    except Exception:
        pass

    # Try to interpret witness as a tuple (X, R)
    try:
        if len(witness) == 3:
            n_wit, X, R = witness
        else:
            X, R = witness
            
        n = len(X)
        
        # H1: X is a set of n distinct generators
        h1_ok = (len(set(X)) == n)
        
        # H2: R = {x_i x_j x_i^{-1} x_j^{-1} | 1 <= i < j <= n}
        expected_R = set()
        for i in range(n):
            for j in range(i + 1, n):
                expected_R.add(X[i] * X[j] * X[i]**-1 * X[j]**-1)
                
        h2_ok = (set(R) == expected_R)
        
        if n > 0:
            F = X[0].group
            G = FpGroup(F, R)
            invs = G.abelian_invariants()
            is_abelian = True
            for i in range(n):
                for j in range(i + 1, n):
                    word = X[i] * X[j] * X[i]**-1 * X[j]**-1
                    if not G.reduce(word).is_identity:
                        is_abelian = False
                        break
                if not is_abelian:
                    break
            is_iso = is_abelian and (invs == [0]*n)
        else:
            is_iso = True
            
        neg_q_ok = not is_iso
        
        return [h1_ok, h2_ok, neg_q_ok]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: X is a set of n distinct generators",
    "H_2: R is the set of commutator relations {x_i x_j x_i^{-1} x_j^{-1} | 1 <= i < j <= n}",
    "¬Q: The group defined by the presentation <X | R> is NOT isomorphic to the free abelian group of rank n"
]

N_HYP = 2
NEG_Q_INDEX = 2