import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1, h2, h3, h4, neg_q = False, False, False, False, False
    
    # 1. Try SymPy ideals (tuple of 3: I, J, K)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            I, J, K = witness
            if hasattr(I, 'ring') and hasattr(I, 'gens'):
                h1 = True
                h2 = hasattr(J, 'ring') and hasattr(J, 'gens') and J.ring == I.ring
                h3 = hasattr(K, 'ring') and hasattr(K, 'gens') and K.ring == I.ring
                
                if h1 and h2 and h3:
                    h4 = all(J.contains(g) for g in I.gens)
                    
                    IK = I * K
                    JK = J * K
                    
                    q = all(JK.contains(g) for g in IK.gens)
                    neg_q = not q
                    return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    # 2. Try SymPy ideals (tuple of 4: R, I, J, K)
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            R, I, J, K = witness
            if hasattr(I, 'ring') and I.ring == R:
                h1 = True
                h2 = hasattr(J, 'ring') and J.ring == R
                h3 = hasattr(K, 'ring') and K.ring == R
                
                if h1 and h2 and h3:
                    h4 = all(J.contains(g) for g in I.gens)
                    
                    IK = I * K
                    JK = J * K
                    
                    q = all(JK.contains(g) for g in IK.gens)
                    neg_q = not q
                    return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    # 3. Try dictionary representation of finite ring
    try:
        if isinstance(witness, dict) and 'elements' in witness:
            elements = witness['elements']
            add_func = witness['add']
            mul_func = witness['mul']
            
            def add(x, y):
                if isinstance(add_func, dict): return add_func[(x, y)]
                if isinstance(add_func, list): return add_func[x][y]
                return add_func(x, y)
                
            def mul(x, y):
                if isinstance(mul_func, dict): return mul_func[(x, y)]
                if isinstance(mul_func, list): return mul_func[x][y]
                return mul_func(x, y)
                
            I = witness['I']
            J = witness['J']
            K = witness['K']
            
            def is_ideal(subset):
                if not subset: return False
                if not all(x in elements for x in subset): return False
                for x in subset:
                    for y in subset:
                        if add(x, y) not in subset: return False
                for r in elements:
                    for x in subset:
                        if mul(r, x) not in subset: return False
                        if mul(x, r) not in subset: return False
                return True
                
            h1 = is_ideal(I)
            h2 = is_ideal(J)
            h3 = is_ideal(K)
            
            h4 = all(x in J for x in I)
            
            def ideal_mul(A, B):
                products = set()
                for a in A:
                    for b in B:
                        products.add(mul(a, b))
                closure = list(products)
                changed = True
                while changed:
                    changed = False
                    n = len(closure)
                    for i in range(n):
                        for j in range(n):
                            s = add(closure[i], closure[j])
                            if s not in closure:
                                closure.append(s)
                                changed = True
                return closure
                
            IK = ideal_mul(I, K)
            JK = ideal_mul(J, K)
            
            q = all(x in JK for x in IK)
            neg_q = not q
            
            return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    # 4. Try generic object with methods
    try:
        if isinstance(witness, tuple) and len(witness) in (3, 4):
            if len(witness) == 3:
                I, J, K = witness
            else:
                R, I, J, K = witness
                
            if hasattr(I, 'is_ideal'):
                h1 = bool(I.is_ideal)
                h2 = bool(getattr(J, 'is_ideal', False))
                h3 = bool(getattr(K, 'is_ideal', False))
                
                if hasattr(I, 'issubset'):
                    h4 = I.issubset(J)
                else:
                    h4 = all(x in J for x in I)
                    
                IK = I * K
                JK = J * K
                
                if hasattr(IK, 'issubset'):
                    q = IK.issubset(JK)
                else:
                    q = all(x in JK for x in IK)
                    
                return [h1, h2, h3, h4, not q]
    except Exception:
        pass

    return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: J is an ideal of R",
    "H_3: K is an ideal of R",
    "H_4: I is a subset of J",
    "¬Q: IK is not a subset of JK"
]

N_HYP = 4
NEG_Q_INDEX = 4