import sympy
from sympy import eye, zeros
import itertools
import math
import functools

# Top-level setup for standard objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Extract witness components
        if isinstance(witness, dict):
            R_elems = witness.get('R_elements', [])
            R_add = witness.get('R_add', {})
            R_mul = witness.get('R_mul', {})
            S_elems = witness.get('S_elements', [])
            S_add = witness.get('S_add', {})
            S_mul = witness.get('S_mul', {})
            f = witness.get('f', {})
            n = witness.get('n', 0)
            F = witness.get('F', None)
        elif isinstance(witness, tuple) and len(witness) == 9:
            R_elems, R_add, R_mul, S_elems, S_add, S_mul, f, n, F = witness
        else:
            R_elems = getattr(witness, 'R_elements', [])
            R_add = getattr(witness, 'R_add', {})
            R_mul = getattr(witness, 'R_mul', {})
            S_elems = getattr(witness, 'S_elements', [])
            S_add = getattr(witness, 'S_add', {})
            S_mul = getattr(witness, 'S_mul', {})
            f = getattr(witness, 'f', {})
            n = getattr(witness, 'n', 0)
            F = getattr(witness, 'F', None)

        # Helpers to normalize functions/lists to dictionaries
        def to_dict_1(func, elems):
            if isinstance(func, dict): return func
            if callable(func): return {a: func(a) for a in elems}
            if isinstance(func, (list, tuple)): return {a: func[a] for a in elems}
            return func
            
        def to_dict_2(func, elems):
            if isinstance(func, dict): return func
            if callable(func): return {(a, b): func(a, b) for a in elems for b in elems}
            if isinstance(func, (list, tuple)): return {(a, b): func[a][b] for a in elems for b in elems}
            return func

        R_add = to_dict_2(R_add, R_elems)
        R_mul = to_dict_2(R_mul, R_elems)
        S_add = to_dict_2(S_add, S_elems)
        S_mul = to_dict_2(S_mul, S_elems)
        f = to_dict_1(f, R_elems)

        # H1: R and S are rings
        def is_ring(elements, add, mul):
            if not elements: return False
            elements = set(elements)
            # Closure
            for a in elements:
                for b in elements:
                    if (a, b) not in add or add[(a, b)] not in elements: return False
                    if (a, b) not in mul or mul[(a, b)] not in elements: return False
            # Addition commutativity
            for a in elements:
                for b in elements:
                    if add[(a, b)] != add[(b, a)]: return False
            # Addition associativity
            for a in elements:
                for b in elements:
                    for c in elements:
                        if add[(add[(a, b)], c)] != add[(a, add[(b, c)])]: return False
            # Additive identity
            zero = None
            for e in elements:
                if all(add[(e, a)] == a for a in elements):
                    zero = e
                    break
            if zero is None: return False
            # Additive inverses
            for a in elements:
                if not any(add[(a, b)] == zero for b in elements): return False
            # Multiplication associativity
            for a in elements:
                for b in elements:
                    for c in elements:
                        if mul[(mul[(a, b)], c)] != mul[(a, mul[(b, c)])]: return False
            # Distributivity
            for a in elements:
                for b in elements:
                    for c in elements:
                        if mul[(a, add[(b, c)])] != add[(mul[(a, b)], mul[(a, c)])]: return False
                        if mul[(add[(a, b)], c)] != add[(mul[(a, c)], mul[(b, c)])]: return False
            return True

        h1 = is_ring(R_elems, R_add, R_mul) and is_ring(S_elems, S_add, S_mul)
    except Exception:
        h1 = False

    try:
        # H2: f is a ring homomorphism from R to S
        def is_homomorphism(elements, add, mul, S_add, S_mul, f):
            for a in elements:
                if a not in f: return False
                for b in elements:
                    if f[add[(a, b)]] != S_add[(f[a], f[b])]: return False
                    if f[mul[(a, b)]] != S_mul[(f[a], f[b])]: return False
            return True
            
        h2 = is_homomorphism(R_elems, R_add, R_mul, S_add, S_mul, f)
    except Exception:
        h2 = False

    try:
        # H3: n is a positive integer
        h3 = isinstance(n, int) and n > 0
    except Exception:
        h3 = False

    try:
        # ¬Q: The kernel of F is not the matrix ring M_n(K)
        def get_zero(elements, add):
            for e in elements:
                if all(add[(e, a)] == a for a in elements):
                    return e
            return None
        
        R_zero = get_zero(R_elems, R_add)
        S_zero = get_zero(S_elems, S_add)
        
        M_n_R = set(itertools.product(*[list(itertools.product(R_elems, repeat=n)) for _ in range(n)]))
        M_n_S = set(itertools.product(*[list(itertools.product(S_elems, repeat=n)) for _ in range(n)]))
        
        # If F is not provided, assume it's the induced homomorphism
        if F is None:
            F_dict = {}
            for A in M_n_R:
                F_dict[A] = tuple(tuple(f[x] for x in row) for row in A)
            F = F_dict
        elif callable(F):
            F_dict = {}
            for A in M_n_R:
                F_dict[A] = F(A)
            F = F_dict
            
        zero_matrix = tuple(tuple(S_zero for _ in range(n)) for _ in range(n))
        
        ker_F = set()
        for A, F_A in F.items():
            if F_A == zero_matrix:
                ker_F.add(A)
                
        K = {a for a in R_elems if f[a] == S_zero}
        M_n_K = set(itertools.product(*[list(itertools.product(K, repeat=n)) for _ in range(n)]))
        
        if set(F.keys()) != M_n_R:
            neg_Q = False
        elif not all(v in M_n_S for v in F.values()):
            neg_Q = False
        else:
            neg_Q = (ker_F != M_n_K)
            
    except Exception:
        neg_Q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a ring homomorphism from R to S",
    "H_3: n is a positive integer",
    "¬Q: The kernel of F is not the matrix ring M_n(K) consisting of all n by n matrices with entries in the kernel of f"
]

N_HYP = 3
NEG_Q_INDEX = 3