import sympy
from sympy import Interval, FiniteSet, ProductSet, S, Tuple, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: U is an open subset of R^n that contains x",
    "¬Q: There does NOT exist a compact set K subset R^n such that x is in the interior of K, and K subset U"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # Extract U, x, n from the witness
        if isinstance(witness, dict):
            U = witness.get('U')
            x = witness.get('x')
            n = witness.get('n')
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            U, x, n = witness
        else:
            U = getattr(witness, 'U', None)
            x = getattr(witness, 'x', None)
            n = getattr(witness, 'n', None)
            
        if U is None or x is None or n is None:
            return [False, False]
            
        def is_open_set(S_set):
            if isinstance(S_set, Interval):
                return bool(S_set.left_open and S_set.right_open)
            if S_set == S.Reals or S_set == sympy.EmptySet:
                return True
            if isinstance(S_set, FiniteSet):
                return False
            if isinstance(S_set, sympy.Union) or isinstance(S_set, sympy.Intersection):
                return all(is_open_set(s) for s in S_set.args)
            if isinstance(S_set, ProductSet):
                return all(is_open_set(s) for s in S_set.sets)
            if hasattr(S_set, 'is_open'):
                val = S_set.is_open() if callable(S_set.is_open) else S_set.is_open
                if val == True or val == S.true:
                    return True
            return False
            
        def contains_pt(S_set, pt):
            if isinstance(S_set, ProductSet) and isinstance(pt, (list, tuple)):
                pt = Tuple(*pt)
            if hasattr(S_set, 'contains'):
                try:
                    res = S_set.contains(pt)
                    if res == True or res == S.true:
                        return True
                except Exception:
                    pass
            if hasattr(S_set, '__contains__'):
                try:
                    if pt in S_set:
                        return True
                except Exception:
                    pass
            if S_set == S.Reals:
                if getattr(pt, 'is_real', False) or isinstance(pt, (int, float)):
                    return True
            return False

        def in_interior(pt, S_set, dim):
            # Infinite dimensional Euclidean spaces (like R^oo) are not locally compact
            if dim == sympy.oo or dim == S.Infinity or str(dim) == 'oo' or getattr(dim, 'is_infinite', False):
                return False
                
            if isinstance(S_set, Interval):
                interior = Interval(S_set.start, S_set.end, True, True)
                return contains_pt(interior, pt)
                
            if S_set == S.Reals:
                return True
                
            if isinstance(S_set, FiniteSet):
                return False
                
            if isinstance(S_set, ProductSet):
                if not isinstance(pt, (tuple, list, Tuple)):
                    return False
                if len(pt) != len(S_set.sets):
                    return False
                return all(in_interior(p, s, 1) for p, s in zip(pt, S_set.sets))
                
            if hasattr(S_set, 'interior'):
                int_S = S_set.interior() if callable(S_set.interior) else S_set.interior
                return contains_pt(int_S, pt)
                
            if is_open_set(S_set):
                return contains_pt(S_set, pt)
                
            return False

        # Evaluate Hypothesis 1
        h1 = is_open_set(U) and contains_pt(U, x)
        
        # Evaluate Negated Conclusion
        # The conclusion fails if x does not have a compact neighborhood contained in U.
        # This happens if x is not in the interior of U, or if the space is infinite-dimensional.
        neg_q = not in_interior(x, U, n)
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]