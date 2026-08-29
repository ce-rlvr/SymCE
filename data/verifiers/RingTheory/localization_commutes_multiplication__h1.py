import sympy as sp
from sympy import Matrix
import itertools

class MatrixRing:
    """
    A helper class to represent the ring of n x n matrices over Z/pZ.
    Elements are represented as tuples of tuples for hashability and performance.
    """
    def __init__(self, n, p):
        self.n = n
        self.p = p
        self.elements = []
        for entries in itertools.product(range(p), repeat=n*n):
            mat = tuple(tuple(entries[i*n + j] for j in range(n)) for i in range(n))
            self.elements.append(mat)
            
    def add(self, A, B):
        n = self.n
        p = self.p
        return tuple(tuple((A[i][j] + B[i][j]) % p for j in range(n)) for i in range(n))
        
    def mul(self, A, B):
        n = self.n
        p = self.p
        res = []
        for i in range(n):
            row = []
            for j in range(n):
                val = sum(A[i][k] * B[k][j] for k in range(n)) % p
                row.append(val)
            res.append(tuple(row))
        return tuple(res)
        
    def zero(self):
        return tuple(tuple(0 for _ in range(self.n)) for _ in range(self.n))
        
    def one(self):
        return tuple(tuple(1 if i == j else 0 for j in range(self.n)) for i in range(self.n))

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: I and J are ideals of R",
    "¬Q: S^{-1}(IJ) != (S^{-1}I)(S^{-1}J) as ideals in S^{-1}R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness can either be a custom object with methods:
      - is_multiplicatively_closed()
      - is_ideal_I()
      - is_ideal_J()
      - localization_commutes()
    OR a tuple (R, S, I, J) where R is a ring object (like MatrixRing) 
    and S, I, J are lists of elements from R.
    """
    # Support for custom witness objects
    if hasattr(witness, 'is_multiplicatively_closed'):
        try:
            h1 = bool(witness.is_multiplicatively_closed())
        except Exception:
            h1 = False
        try:
            h2 = bool(witness.is_ideal_I() and witness.is_ideal_J())
        except Exception:
            h2 = False
        try:
            neg_q = not bool(witness.localization_commutes())
        except Exception:
            neg_q = False
        return [h1, h2, neg_q]

    # Support for tuple witness (R, S, I, J)
    try:
        R, S, I, J = witness
    except Exception:
        return [False, False, False]

    # H1: S is multiplicatively closed
    try:
        h1 = True
        if R.one() not in S:
            h1 = False
        else:
            for x in S:
                for y in S:
                    if R.mul(x, y) not in S:
                        h1 = False
                        break
                if not h1: break
    except Exception:
        h1 = False

    # H2: I and J are ideals
    try:
        def is_ideal(subset):
            if R.zero() not in subset: return False
            for x in subset:
                for y in subset:
                    if R.add(x, y) not in subset: return False
            for x in subset:
                for r in R.elements:
                    if R.mul(r, x) not in subset: return False
                    if R.mul(x, r) not in subset: return False
            return True
            
        h2 = is_ideal(I) and is_ideal(J)
    except Exception:
        h2 = False

    # neg_Q: S^{-1}(IJ) != (S^{-1}I)(S^{-1}J)
    try:
        # Check left Ore condition
        is_ore = True
        for r in R.elements:
            for s in S:
                found = False
                for r_prime in R.elements:
                    for s_prime in S:
                        if R.mul(s_prime, r) == R.mul(r_prime, s):
                            found = True
                            break
                    if found: break
                if not found:
                    is_ore = False
                    break
            if not is_ore: break
            
        if not is_ore:
            # If S is not an Ore set, S^{-1}R is not a ring of fractions,
            # so the conclusion "as ideals in S^{-1}R" fails.
            neg_q = True
        else:
            # Compute equivalence classes for left fractions (s, r) representing s^{-1} r
            def fractions_equal(s1, r1, s2, r2):
                for u1 in R.elements:
                    us1 = R.mul(u1, s1)
                    if us1 not in S: continue
                    ur1 = R.mul(u1, r1)
                    for u2 in R.elements:
                        if us1 == R.mul(u2, s2):
                            if ur1 == R.mul(u2, r2):
                                return True
                return False
                
            classes = []
            for s in S:
                for r in R.elements:
                    found = False
                    for cls in classes:
                        s_c, r_c = cls[0]
                        if fractions_equal(s, r, s_c, r_c):
                            cls.append((s, r))
                            found = True
                            break
                    if not found:
                        classes.append([(s, r)])
                        
            def get_localized_ideal(subset):
                loc = []
                for cls in classes:
                    if any(pair[1] in subset for pair in cls):
                        loc.append(cls)
                return loc
                
            # Compute IJ
            products = [R.mul(i, j) for i in I for j in J]
            closure = set(products)
            added = True
            while added:
                added = False
                new_elements = set()
                for x in closure:
                    for y in closure:
                        s_val = R.add(x, y)
                        if s_val not in closure and s_val not in new_elements:
                            new_elements.add(s_val)
                if new_elements:
                    closure.update(new_elements)
                    added = True
            IJ = list(closure)
            
            loc_IJ = get_localized_ideal(IJ)
            loc_I = get_localized_ideal(I)
            loc_J = get_localized_ideal(J)
            
            def multiply_classes(cls1, cls2):
                s1, r1 = cls1[0]
                s2, r2 = cls2[0]
                for r1_prime in R.elements:
                    for s2_prime in S:
                        if R.mul(s2_prime, r1) == R.mul(r1_prime, s2):
                            num = R.mul(r1_prime, r2)
                            den = R.mul(s2_prime, s1)
                            for cls in classes:
                                if fractions_equal(den, num, cls[0][0], cls[0][1]):
                                    return cls
                return None
                
            def add_classes(cls1, cls2):
                s1, r1 = cls1[0]
                s2, r2 = cls2[0]
                for u1 in R.elements:
                    us1 = R.mul(u1, s1)
                    if us1 not in S: continue
                    ur1 = R.mul(u1, r1)
                    for u2 in R.elements:
                        if us1 == R.mul(u2, s2):
                            num = R.add(ur1, R.mul(u2, r2))
                            den = us1
                            for cls in classes:
                                if fractions_equal(den, num, cls[0][0], cls[0][1]):
                                    return cls
                return None
                
            # Compute (S^{-1}I)(S^{-1}J)
            prod_classes = []
            failed = False
            for c1 in loc_I:
                for c2 in loc_J:
                    p = multiply_classes(c1, c2)
                    if p is None:
                        failed = True
                        break
                    if p not in prod_classes:
                        prod_classes.append(p)
                if failed: break
                
            if failed:
                neg_q = True
            else:
                closure_classes = list(prod_classes)
                added = True
                while added:
                    added = False
                    new_classes = []
                    for x in closure_classes:
                        for y in closure_classes:
                            s_val = add_classes(x, y)
                            if s_val is None:
                                failed = True
                                break
                            if s_val not in closure_classes and s_val not in new_classes:
                                new_classes.append(s_val)
                        if failed: break
                    if failed: break
                    if new_classes:
                        closure_classes.extend(new_classes)
                        added = True
                        
                if failed:
                    neg_q = True
                else:
                    def classes_equal(A, B):
                        if len(A) != len(B): return False
                        for a in A:
                            if a not in B: return False
                        return True
                        
                    neg_q = not classes_equal(loc_IJ, closure_classes)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]