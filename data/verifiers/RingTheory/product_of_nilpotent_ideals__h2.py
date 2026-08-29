import sympy
from sympy import Matrix, zeros, eye
import itertools
import math
import functools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, I, J, n) or (R, I, J) where:
      - R is a list of sympy matrices representing the commutative ring.
      - I is a list of sympy matrices representing the set I.
      - J is a list of sympy matrices representing the nilpotent ideal J.
      - n is an optional integer modulus for matrix arithmetic (default 0).
    """
    try:
        if len(witness) == 4:
            R, I, J, n = witness
            n = int(n)
        elif len(witness) == 3:
            R, I, J = witness
            n = 0
        else:
            return [False, False, False]
            
        if not isinstance(R, (list, tuple, set)):
            R = [R]
        if not isinstance(I, (list, tuple, set)):
            I = [I]
        if not isinstance(J, (list, tuple, set)):
            J = [J]
            
        R = list(R)
        I = list(I)
        J = list(J)
        
        # Prevent timeouts from excessively large inputs
        if len(R) > 100 or len(I) > 100 or len(J) > 100:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def mod_mat(M):
        if n > 0:
            def mod_n(x):
                try:
                    return x % n
                except Exception:
                    return x
            return M.applyfunc(mod_n)
        return M

    def is_zero(A):
        M = mod_mat(A)
        try:
            M = M.applyfunc(sympy.expand)
        except Exception:
            pass
        return M.is_zero_matrix == True

    def eq_mat(A, B):
        diff = mod_mat(A - B)
        try:
            diff = diff.applyfunc(sympy.expand)
        except Exception:
            pass
        return diff.is_zero_matrix == True

    def mult(A, B):
        return mod_mat(A * B)

    def add(A, B):
        return mod_mat(A + B)

    def unique_matrices(lst):
        res = []
        seen = set()
        for M in lst:
            t = tuple(mod_mat(M))
            if t not in seen:
                seen.add(t)
                res.append(M)
        return res

    def check_H1():
        if not R: return False
        R_tuples = set(tuple(mod_mat(a)) for a in R)
        
        # Closed under addition
        for a in R:
            for b in R:
                if tuple(add(a, b)) not in R_tuples: return False
                
        # Closed under multiplication
        for a in R:
            for b in R:
                if tuple(mult(a, b)) not in R_tuples: return False
        
        # Contains zero
        zero_found = False
        for a in R:
            if is_zero(a):
                zero_found = True
                break
        if not zero_found: return False
        
        # Commutative multiplication
        for a in R:
            for b in R:
                if not eq_mat(mult(a, b), mult(b, a)): return False
                
        # Additive inverse exists
        for a in R:
            has_inv = False
            for b in R:
                if is_zero(add(a, b)):
                    has_inv = True
                    break
            if not has_inv: return False
            
        return True

    def check_H2():
        if not J: return False
        R_tuples = set(tuple(mod_mat(a)) for a in R)
        J_tuples = set(tuple(mod_mat(a)) for a in J)
        
        # Subset of R
        if not J_tuples.issubset(R_tuples): return False
        
        # Closed under addition
        for a in J:
            for b in J:
                if tuple(add(a, b)) not in J_tuples: return False
                
        # Ideal property: R * J \subseteq J
        for r in R:
            for j in J:
                if tuple(mult(r, j)) not in J_tuples: return False
                
        # Nilpotent
        current_products = J
        for k in range(1, 10):
            if all(is_zero(M) for M in current_products):
                return True
            next_products = []
            for A in current_products:
                for B in J:
                    next_products.append(mult(A, B))
            current_products = unique_matrices(next_products)
            if len(current_products) > 32:
                current_products = current_products[:32]
        return False

    def check_neg_Q():
        if not R or not J: return False
        if not I: return False
        
        # Compute products of elements in I and J
        P = []
        for a in I:
            for b in J:
                P.append(mult(a, b))
        P = unique_matrices(P)
        
        # Compute the additive span of P to form the product ideal IJ
        try:
            shape = R[0].shape
            zero_mat = mod_mat(sympy.zeros(*shape))
            queue = [zero_mat]
            span_tuples = {tuple(zero_mat)}
            
            while queue:
                if len(span_tuples) > 64:
                    return False
                curr = queue.pop(0)
                for p in P:
                    nxt = add(curr, p)
                    nxt_t = tuple(nxt)
                    if nxt_t not in span_tuples:
                        span_tuples.add(nxt_t)
                        queue.append(nxt)
                        
            span = [sympy.Matrix(*shape, t) for t in span_tuples]
        except Exception:
            return False

        R_tuples = set(tuple(mod_mat(a)) for a in R)
        span_set = set(tuple(mod_mat(a)) for a in span)
        
        # Check if IJ is an ideal of R
        is_ideal = True
        if not span_set.issubset(R_tuples):
            is_ideal = False
        else:
            for r in R:
                for x in span:
                    if tuple(mult(r, x)) not in span_set:
                        is_ideal = False
                        break
                if not is_ideal:
                    break
                    
        # Check if IJ is nilpotent
        is_nilp = False
        current_products = span
        for k in range(1, 10):
            if all(is_zero(M) for M in current_products):
                is_nilp = True
                break
            next_products = []
            for A in current_products:
                for B in span:
                    next_products.append(mult(A, B))
            current_products = unique_matrices(next_products)
            if len(current_products) > 32:
                current_products = current_products[:32]
                
        # The conclusion fails if IJ is NOT an ideal of R, or if it is NOT nilpotent
        return not (is_ideal and is_nilp)

    try:
        h1 = check_H1()
    except Exception:
        h1 = False

    try:
        h2 = check_H2()
    except Exception:
        h2 = False

    try:
        nq = check_neg_Q()
    except Exception:
        nq = False

    return [h1, h2, nq]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is a nilpotent ideal of R",
    "¬Q: The product ideal IJ is not a nilpotent ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2