import sympy
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
Q = sympy.S.Rationals
R = sympy.S.Reals
N = sympy.S.Naturals
Z = sympy.S.Integers

def conditions(witness) -> list[bool]:
    h1_ok = False
    neg_q_ok = False
    
    try:
        # The witness is expected to be a tuple (X, sequence)
        # where X is the space (e.g., sympy.S.Rationals)
        # and sequence is either a callable U(n) returning the n-th open dense set,
        # or a callable q(n) returning the n-th removed point,
        # or an iterable of such sets/points.
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
            
        X, second = witness
        is_rats = (X == sympy.S.Rationals)
        
        generated = set()
        if callable(second):
            is_U_n = False
            start_idx = 1
            try:
                val1 = second(1)
            except Exception:
                try:
                    val1 = second(0)
                    start_idx = 0
                except Exception:
                    val1 = None
            
            if val1 is not None:
                if isinstance(val1, sympy.Set):
                    is_U_n = True
                
                for n in range(start_idx, start_idx + 5000):
                    try:
                        if is_U_n:
                            val = second(n)
                            if isinstance(val, sympy.Complement):
                                if val.args[0] == sympy.S.Rationals and isinstance(val.args[1], sympy.FiniteSet):
                                    for pt in val.args[1]:
                                        generated.add(pt)
                        else:
                            generated.add(second(n))
                    except Exception:
                        pass
        elif hasattr(second, '__iter__'):
            iterator = iter(second)
            for _ in range(5000):
                try:
                    val = next(iterator)
                    if isinstance(val, sympy.Complement):
                        if val.args[0] == sympy.S.Rationals and isinstance(val.args[1], sympy.FiniteSet):
                            for pt in val.args[1]:
                                generated.add(pt)
                    else:
                        generated.add(val)
                except StopIteration:
                    break
                except Exception:
                    pass

        # Filter to only valid sympy Rationals
        rats = [x for x in generated if isinstance(x, sympy.Rational)]
                
        # H_1: {U_n} is a countable collection of dense open subsets of X
        # If X is Q, removing a finite set of points leaves an open dense subset.
        if is_rats and len(rats) > 10:
            h1_ok = True
            
        # neg_Q: The intersection of U_n is not dense in X
        # To verify the intersection is not dense, the removed points must form a dense subset
        # in some interval. We check if the generated points densely cover a sub-interval.
        if h1_ok:
            denominators = set(x.q for x in rats)
            if len(denominators) > 10:
                max_den = max(denominators)
                # A true enumeration of Q will have a high ratio of distinct denominators
                # compared to the maximum denominator reached. A discrete grid (like n/K) will not.
                if len(denominators) > max_den * 0.4:
                    valid_floats = [float(x) for x in rats]
                    for start_val in [0, -1, 1, 2, -2]:
                        in_interval = sorted([f for f in valid_floats if start_val <= f <= start_val + 1])
                        if len(in_interval) > 20:
                            gaps = [in_interval[i+1] - in_interval[i] for i in range(len(in_interval)-1)]
                            # If the maximum gap is small and it spans a significant width, it's dense
                            if max(gaps) < 0.05 and (in_interval[-1] - in_interval[0]) > 0.2:
                                neg_q_ok = True
                                break
                                
    except Exception:
        pass
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: {U_n} is a countable collection of dense open subsets of X",
    "¬Q: The intersection of U_n is not dense in X"
]
N_HYP = 1
NEG_Q_INDEX = 1