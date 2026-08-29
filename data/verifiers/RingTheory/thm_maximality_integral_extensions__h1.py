import sympy
from sympy import Matrix, eye, zeros, Rational
import itertools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class ModMatrix:
    """Helper class for matrices over Z_n to easily construct finite ring counterexamples."""
    def __init__(self, mat, mod):
        self.mat = Matrix(mat).applyfunc(lambda x: x % mod)
        self.mod = mod
    def __add__(self, other):
        return ModMatrix(self.mat + other.mat, self.mod)
    def __sub__(self, other):
        return ModMatrix(self.mat - other.mat, self.mod)
    def __mul__(self, other):
        return ModMatrix(self.mat * other.mat, self.mod)
    def __eq__(self, other):
        if not isinstance(other, ModMatrix): return False
        return self.mat == other.mat and self.mod == other.mod
    def __hash__(self):
        return hash((tuple(self.mat), self.mod))
    def __repr__(self):
        return f"ModMatrix({self.mat.tolist()}, {self.mod})"

def conditions(witness):
    try:
        R = witness['R']
        S = witness['S']
        Q = witness['Q']
        P = witness['P']
        
        def contains(lst, item):
            return any(x == item for x in lst)
            
        def is_subset(sub, parent):
            return all(contains(parent, x) for x in sub)
            
        def is_equal(set1, set2):
            return is_subset(set1, set2) and is_subset(set2, set1)
            
        def intersection(set1, set2):
            return [x for x in set1 if contains(set2, x)]
            
        def is_closed_under_sub(subset):
            for a in subset:
                for b in subset:
                    if not contains(subset, a - b): return False
            return True
            
        def is_closed_under_mult(subset):
            for a in subset:
                for b in subset:
                    if not contains(subset, a * b): return False
            return True
            
        def is_subring(subset, parent):
            if not subset: return False
            if not is_subset(subset, parent): return False
            return is_closed_under_sub(subset) and is_closed_under_mult(subset)
            
        def is_ideal(subset, ring):
            if not is_subring(subset, ring): return False
            for x in subset:
                for r in ring:
                    if not contains(subset, x * r): return False
                    if not contains(subset, r * x): return False
            return True
            
        def is_prime_ideal(subset, ring):
            if not is_ideal(subset, ring): return False
            if is_equal(subset, ring): return False
            for a in ring:
                for b in ring:
                    if all(contains(subset, a * r * b) for r in ring):
                        if not contains(subset, a) and not contains(subset, b):
                            return False
            return True
            
        def is_maximal_ideal(subset, ring):
            if not is_ideal(subset, ring): return False
            if is_equal(subset, ring): return False
            for x in ring:
                if contains(subset, x): continue
                gen = list(subset)
                gen.append(x)
                changed = True
                while changed:
                    changed = False
                    new_els = []
                    for a in gen:
                        for b in gen:
                            s_add = a + b
                            if not contains(gen, s_add) and not contains(new_els, s_add):
                                new_els.append(s_add)
                            s_sub = a - b
                            if not contains(gen, s_sub) and not contains(new_els, s_sub):
                                new_els.append(s_sub)
                        for r in ring:
                            p1 = a * r
                            if not contains(gen, p1) and not contains(new_els, p1):
                                new_els.append(p1)
                            p2 = r * a
                            if not contains(gen, p2) and not contains(new_els, p2):
                                new_els.append(p2)
                    if new_els:
                        gen.extend(new_els)
                        changed = True
                if not is_equal(gen, ring):
                    return False
            return True
            
        def is_integral_extension(S_set, R_set):
            for s in S_set:
                found = False
                V = list(R_set)
                p = s
                if contains(V, p):
                    continue
                for n in range(2, len(S_set) + 2):
                    new_V = list(V)
                    for v in V:
                        for c in R_set:
                            term = v + c * p
                            if not contains(new_V, term):
                                new_V.append(term)
                    V = new_V
                    p = p * s
                    if contains(V, p):
                        found = True
                        break
                if not found:
                    return False
            return True

        h1 = is_subring(R, S)
        h2 = is_integral_extension(S, R)
        h3 = is_prime_ideal(Q, S)
        h4 = is_equal(P, intersection(Q, R))
        
        q_max = is_maximal_ideal(Q, S)
        p_max = is_maximal_ideal(P, R)
        
        neg_q = (q_max != p_max)
        
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a subring of S",
    "H_2: S is an integral extension of R",
    "H_3: Q is a prime ideal of S",
    "H_4: P = Q ∩ R",
    "¬Q: Q is a maximal ideal of S iff P is a maximal ideal of R is FALSE"
]

N_HYP = 4
NEG_Q_INDEX = 4