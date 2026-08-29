import sympy
from sympy.matrices import eye, MatrixBase
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        # H1: G is finitely generated
        # We accept a PermutationGroup or a list/tuple of generators (matrices or permutations)
        if isinstance(witness, PermutationGroup):
            # Finite groups always satisfy the conclusion (T = G is a finite characteristic subgroup)
            return [True, True, False]
            
        if not isinstance(witness, (list, tuple)):
            return [False, False, False]
            
        if len(witness) == 0:
            return [False, False, False]
            
        if all(isinstance(g, Permutation) for g in witness):
            return [True, True, False]
            
        if not all(isinstance(g, MatrixBase) for g in witness):
            return [False, False, False]
            
        h1 = True
        
        # H2: T is the set of all elements of finite order in G
        # This is a definitional hypothesis, so it holds by definition in our evaluation.
        h2 = True
        
        I = eye(witness[0].shape[0])
        
        def is_finite_order(M):
            P = M
            for k in range(1, 300):
                if P == I:
                    return True
                P = P * M
            return False

        # BFS to find elements of finite order
        current_level = []
        for g in witness:
            if not any(g == x for x in current_level):
                current_level.append(g)
            try:
                ginv = g.inv()
                if not any(ginv == x for x in current_level):
                    current_level.append(ginv)
            except Exception:
                pass
                
        finite_order_elements = [g for g in current_level if is_finite_order(g)]
        
        neg_q = False
        
        # Check if the product of any two finite order elements has infinite order.
        # If so, T is not closed under multiplication, hence not a subgroup.
        for a in finite_order_elements:
            for b in finite_order_elements:
                if not is_finite_order(a * b):
                    neg_q = True
                    break
            if neg_q:
                break
                
        if not neg_q:
            # Expand one more level to catch cases where generators don't directly break closure
            next_level = []
            for g in current_level:
                for h in current_level:
                    gh = g * h
                    if not any(gh == x for x in next_level):
                        next_level.append(gh)
            
            new_finite = [g for g in next_level if is_finite_order(g)]
            for g in new_finite:
                if not any(g == x for x in finite_order_elements):
                    finite_order_elements.append(g)
            
            for a in finite_order_elements:
                for b in finite_order_elements:
                    if not is_finite_order(a * b):
                        neg_q = True
                        break
                if neg_q:
                    break

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G is finitely generated",
    "H_2: T is the set of all elements of finite order in G",
    "¬Q: T is not a finite characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2