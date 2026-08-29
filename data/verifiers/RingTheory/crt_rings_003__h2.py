import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: I_i + I_j = R for all i != j",
    "¬Q: The quotient R/(cap I_k) is not isomorphic to prod R/I_k as rings (e.g., some I_k is not an ideal)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_ops(sample, m):
    if isinstance(sample, (int, sympy.Integer)):
        if m is not None:
            def add(a, b): return (a + b) % m
            def mul(a, b): return (a * b) % m
            def neg(a): return (-a) % m
            def to_std(a): return int(a) % m
        else:
            def add(a, b): return a + b
            def mul(a, b): return a * b
            def neg(a): return -a
            def to_std(a): return int(a)
        return add, mul, neg, to_std
    elif hasattr(sample, 'tolist'): # sympy Matrix
        n = sample.shape[0]
        if m is not None:
            def add(A, B):
                return tuple(tuple((a + b) % m for a, b in zip(rA, rB)) for rA, rB in zip(A, B))
            def mul(A, B):
                res = []
                for i in range(n):
                    row = []
                    for j in range(n):
                        val = sum(A[i][k] * B[k][j] for k in range(n)) % m
                        row.append(val)
                    res.append(tuple(row))
                return tuple(res)
            def neg(A):
                return tuple(tuple((-a) % m for a in row) for row in A)
            def to_std(A):
                if isinstance(A, tuple): return A
                return tuple(tuple(int(x) % m for x in row) for row in A.tolist())
        else:
            def add(A, B):
                return tuple(tuple(sympy.expand(a + b) for a, b in zip(rA, rB)) for rA, rB in zip(A, B))
            def mul(A, B):
                res = []
                for i in range(n):
                    row = []
                    for j in range(n):
                        val = sympy.expand(sum(A[i][k] * B[k][j] for k in range(n)))
                        row.append(val)
                    res.append(tuple(row))
                return tuple(res)
            def neg(A):
                return tuple(tuple(sympy.expand(-a) for a in row) for row in A)
            def to_std(A):
                if isinstance(A, tuple): return A
                return tuple(tuple(sympy.expand(x) for x in row) for row in A.tolist())
        return add, mul, neg, to_std
    else:
        # General sympy objects
        if m is not None:
            def add(a, b): return sympy.Mod(sympy.expand(a + b), m)
            def mul(a, b): return sympy.Mod(sympy.expand(a * b), m)
            def neg(a): return sympy.Mod(sympy.expand(-a), m)
            def to_std(a): return sympy.Mod(sympy.expand(a), m)
        else:
            def add(a, b): return sympy.expand(a + b)
            def mul(a, b): return sympy.expand(a * b)
            def neg(a): return sympy.expand(-a)
            def to_std(a): return sympy.expand(a)
        return add, mul, neg, to_std

def conditions(witness):
    """
    witness format: (m, R_elements, I_elements_list)
    where:
      - m is the modulus (int) or None.
      - R_elements is a list of elements in the ring R.
      - I_elements_list is a list of lists, each containing elements of I_k.
    Elements can be integers, sympy Matrices, or general sympy expressions.
    """
    try:
        m, R_raw, I_raw_list = witness
        if not R_raw:
            return [False, False, False]
            
        sample = R_raw[0]
        add, mul, neg, to_std = get_ops(sample, m)
        
        R = set(to_std(x) for x in R_raw)
        I_list = [set(to_std(x) for x in I) for I in I_raw_list]
        
        # H1: R is a ring with identity
        h1 = True
        for a in R:
            if neg(a) not in R:
                h1 = False; break
            for b in R:
                if add(a, b) not in R:
                    h1 = False; break
                if mul(a, b) not in R:
                    h1 = False; break
        
        if h1:
            has_id = False
            for e in R:
                is_id = True
                for a in R:
                    if mul(e, a) != a or mul(a, e) != a:
                        is_id = False
                        break
                if is_id:
                    has_id = True
                    break
            if not has_id:
                h1 = False
                
        # H2: I_i + I_j = R for all i != j
        h2 = True
        n_I = len(I_list)
        if n_I < 2:
            h2 = False
        
        for i in range(n_I):
            for j in range(i + 1, n_I):
                sum_set = set()
                for a in I_list[i]:
                    for b in I_list[j]:
                        sum_set.add(add(a, b))
                if sum_set != R:
                    h2 = False
                    break
            if not h2:
                break
                
        for I in I_list:
            if not I.issubset(R):
                h2 = False
                break
                
        # neg_Q: The conclusion fails.
        # The conclusion is a ring isomorphism, which requires I_k to be two-sided ideals.
        # If any I_k is not a two-sided ideal, the quotient R/I_k is not a ring, so the conclusion fails.
        def is_ideal(I):
            if not I: return False
            for a in I:
                if neg(a) not in I: return False
                for b in I:
                    if add(a, b) not in I: return False
            for a in I:
                for r in R:
                    if mul(a, r) not in I: return False
                    if mul(r, a) not in I: return False
            return True
            
        neg_q = not all(is_ideal(I) for I in I_list)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]