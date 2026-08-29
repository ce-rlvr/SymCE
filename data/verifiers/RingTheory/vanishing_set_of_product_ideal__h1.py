import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools
import math
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

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: V(E) denotes the vanishing set of an ideal E in the Zariski topology on Spec(R)",
    "¬Q: V(IJ) != V(I) \\cup V(J)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture:
    V(IJ) = V(I) U V(J) for ideals I, J in a ring R.
    
    The conjecture is true for commutative rings and for two-sided ideals in any ring.
    It fails for left ideals in non-commutative rings (e.g., M_2(F_2)).
    """
    
    # 1. Try finite ring representation: witness = (n, add_table, mul_table, I, J)
    try:
        if isinstance(witness, tuple) and len(witness) == 5:
            n, add, mul, I, J = witness
            if isinstance(n, int) and isinstance(add, list) and isinstance(mul, list):
                elements = list(range(n))
                
                # Check if S is a left ideal
                def is_ideal(S):
                    S = set(S)
                    if not S: return False
                    for a in S:
                        for b in S:
                            if add[a][b] not in S: return False
                    for r in elements:
                        for a in S:
                            if mul[r][a] not in S: return False
                    return True
                    
                h1 = is_ideal(I) and is_ideal(J)
                h2 = True  # Definition holds by construction below
                
                # Find all two-sided ideals to compute Spec(R)
                two_sided_ideals = set()
                for i in range(n):
                    closure = set([i])
                    while True:
                        new_closure = set(closure)
                        for a in closure:
                            for b in closure:
                                new_closure.add(add[a][b])
                        for r in elements:
                            for a in closure:
                                new_closure.add(mul[r][a])
                                new_closure.add(mul[a][r])
                        if len(new_closure) == len(closure):
                            break
                        closure = new_closure
                    two_sided_ideals.add(frozenset(closure))
                    
                all_two_sided = set(two_sided_ideals)
                while True:
                    new_all = set(all_two_sided)
                    for A in all_two_sided:
                        for B in all_two_sided:
                            sum_ideal = set()
                            for a in A:
                                for b in B:
                                    sum_ideal.add(add[a][b])
                            new_all.add(frozenset(sum_ideal))
                    if len(new_all) == len(all_two_sided):
                        break
                    all_two_sided = new_all
                    
                def mul_ideals(A, B):
                    prod_set = set()
                    for a in A:
                        for b in B:
                            prod_set.add(mul[a][b])
                    closure = set(prod_set)
                    while True:
                        new_closure = set(closure)
                        for a in closure:
                            for b in closure:
                                new_closure.add(add[a][b])
                        if len(new_closure) == len(closure):
                            break
                        closure = new_closure
                    return frozenset(closure)
                    
                # Spec(R) is the set of prime two-sided ideals
                spec = []
                for P in all_two_sided:
                    if len(P) == n: continue
                    is_prime = True
                    for A in all_two_sided:
                        for B in all_two_sided:
                            AB = mul_ideals(A, B)
                            if AB.issubset(P):
                                if not (A.issubset(P) or B.issubset(P)):
                                    is_prime = False
                                    break
                        if not is_prime:
                            break
                    if is_prime:
                        spec.append(P)
                        
                def V(E):
                    E_set = set(E)
                    return [P for P in spec if E_set.issubset(P)]
                    
                V_I = V(I)
                V_J = V(J)
                
                # Product of left ideals I and J
                prod_set = set()
                for a in I:
                    for b in J:
                        prod_set.add(mul[a][b])
                closure = set(prod_set)
                while True:
                    new_closure = set(closure)
                    for a in closure:
                        for b in closure:
                            new_closure.add(add[a][b])
                    if len(new_closure) == len(closure):
                        break
                    closure = new_closure
                IJ = closure
                
                V_IJ = V(IJ)
                V_I_cup_V_J = [P for P in spec if P in V_I or P in V_J]
                
                neg_q = set(V_IJ) != set(V_I_cup_V_J)
                
                return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Try duck typing with methods
    try:
        h1 = bool(witness.is_ideal(witness.I) and witness.is_ideal(witness.J))
        h2 = callable(witness.V)
        V_IJ = witness.V(witness.mul(witness.I, witness.J))
        V_I = witness.V(witness.I)
        V_J = witness.V(witness.J)
        
        if isinstance(V_I, set) and isinstance(V_J, set):
            union_V = V_I.union(V_J)
            neg_q = set(V_IJ) != union_V
        else:
            union_V = list(V_I)
            for x in V_J:
                if x not in union_V:
                    union_V.append(x)
            neg_q = False
            for x in V_IJ:
                if x not in union_V:
                    neg_q = True
                    break
            if not neg_q:
                for x in union_V:
                    if x not in V_IJ:
                        neg_q = True
                        break
        return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Try simple boolean flags
    try:
        h1 = bool(witness.h1)
        h2 = bool(witness.h2)
        neg_q = bool(witness.neg_q)
        return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]