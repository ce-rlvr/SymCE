import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: standard groups and matrices
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

def has_finite_order(M, max_k=60):
    try:
        if hasattr(M, 'is_Identity') and M.is_Identity:
            return True
        if hasattr(M, 'shape'):
            I = eye(M.shape[0])
            if M == I:
                return True
            P = M
            for k in range(2, max_k + 1):
                P = P * M
                if P == I:
                    return True
            return False
        if isinstance(M, (int, float, sympy.Expr)):
            if M == 1: 
                return True
            P = M
            for k in range(2, max_k + 1):
                P = P * M
                if P == 1:
                    return True
            return False
        if hasattr(M, 'order'):
            return M.order() < float('inf')
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    # H_1: G is a group (witness provides valid generators for a group)
    h1_ok = False
    try:
        if hasattr(witness, 'generators') or hasattr(witness, 'elements'):
            h1_ok = True
        else:
            if not isinstance(witness, (list, tuple)):
                items = [witness]
            else:
                items = witness
                
            is_valid = True
            for m in items:
                if hasattr(m, 'shape'):
                    if m.shape[0] != m.shape[1]:
                        is_valid = False
                        break
                    if hasattr(m, 'det') and m.det() == 0:
                        is_valid = False
                        break
                elif isinstance(m, (int, float, sympy.Expr)):
                    if m == 0:
                        is_valid = False
                        break
                elif hasattr(m, 'order'):
                    pass
                else:
                    is_valid = False
                    break
            h1_ok = is_valid
    except Exception:
        h1_ok = False

    # neg_Q: T is not a subgroup of G
    # (There exist elements of finite order whose product has infinite order)
    neg_q = False
    try:
        if hasattr(witness, 'generators'):
            gens = list(witness.generators)
        elif hasattr(witness, 'elements'):
            gens = list(witness.elements)
        else:
            if not isinstance(witness, (list, tuple)):
                gens = [witness]
            else:
                gens = list(witness)
                
        all_gens = []
        for g in gens:
            all_gens.append(g)
            try:
                inv_g = g.inv() if hasattr(g, 'inv') else g**-1
                all_gens.append(inv_g)
            except Exception:
                pass
        
        unique_gens = []
        for g in all_gens:
            if g not in unique_gens:
                unique_gens.append(g)
                
        # Generate words of length up to 2
        words = list(unique_gens)
        for w in unique_gens:
            for g in unique_gens:
                try:
                    words.append(w * g)
                except Exception:
                    pass
                    
        # Find all elements of finite order among the generated words
        T_elements = []
        for w in words:
            if has_finite_order(w, max_k=60):
                T_elements.append(w)
                
        # Check if any product of two finite-order elements has infinite order
        for t1 in T_elements:
            for t2 in T_elements:
                try:
                    if not has_finite_order(t1 * t2, max_k=60):
                        neg_q = True
                        break
                except Exception:
                    pass
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group (witness provides valid generators)",
    "¬Q: T is not a subgroup of G (product of two finite-order elements has infinite order)"
]

N_HYP = 1
NEG_Q_INDEX = 1