import sympy
from sympy import Interval, FiniteSet, Union, Intersection, Symbol, S, Lambda

# Top-level setup
n = Symbol('n', integer=True, positive=True)
x, y, z = sympy.symbols('x y z')

def is_compact(S_obj):
    if S_obj == sympy.S.EmptySet:
        return True
    if isinstance(S_obj, sympy.Interval):
        return (not S_obj.left_open) and (not S_obj.right_open) and S_obj.inf.is_finite == True and S_obj.sup.is_finite == True
    if isinstance(S_obj, sympy.FiniteSet):
        for e in S_obj:
            if isinstance(e, sympy.Tuple):
                if not all(getattr(val, 'is_finite', None) == True for val in e):
                    return False
            else:
                if getattr(e, 'is_finite', None) != True:
                    return False
        return True
    if isinstance(S_obj, sympy.Union):
        return all(is_compact(arg) for arg in S_obj.args)
    if isinstance(S_obj, sympy.Intersection):
        return all(is_compact(arg) for arg in S_obj.args)
    if hasattr(sympy, 'ProductSet') and isinstance(S_obj, sympy.ProductSet):
        return all(is_compact(arg) for arg in S_obj.sets)
    return False

def is_subset_Rd(S_obj):
    if S_obj == sympy.S.EmptySet:
        return True
    if isinstance(S_obj, (sympy.Interval, sympy.FiniteSet, sympy.Union, sympy.Intersection)):
        return True
    if hasattr(sympy, 'ProductSet') and isinstance(S_obj, sympy.ProductSet):
        return True
    if S_obj == sympy.S.Reals:
        return True
    try:
        if S_obj.is_subset(sympy.S.Reals):
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    h1_ok = True
    h2_ok = True
    neg_q_ok = False
    
    def get_S(i):
        if callable(witness):
            return witness(i)
        elif isinstance(witness, sympy.Lambda):
            return witness(i)
        elif hasattr(witness, 'free_symbols'):
            n_syms = [s for s in witness.free_symbols if s.name == 'n']
            if n_syms:
                return witness.subs(n_syms[0], i)
            else:
                return witness
        elif hasattr(witness, 'subs'):
            return witness.subs(n, i)
        else:
            idx = i - 1
            if idx < len(witness):
                return witness[idx]
            else:
                return witness[-1]

    try:
        for i in range(1, 101):
            S_obj = get_S(i)
            
            if S_obj == sympy.S.EmptySet or getattr(S_obj, 'is_empty', None) == True:
                h1_ok = False
            if not is_subset_Rd(S_obj):
                h1_ok = False
                
            if not is_compact(S_obj):
                h2_ok = False
                
            if not h1_ok and not h2_ok:
                break
    except Exception:
        h1_ok = False
        h2_ok = False

    try:
        current_intersection = get_S(1)
        if current_intersection == sympy.S.EmptySet or getattr(current_intersection, 'is_empty', None) == True:
            neg_q_ok = True
        else:
            for i in range(2, 101):
                S_obj = get_S(i)
                current_intersection = sympy.Intersection(current_intersection, S_obj)
                if current_intersection == sympy.S.EmptySet or getattr(current_intersection, 'is_empty', None) == True:
                    neg_q_ok = True
                    break
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: For each positive integer n, K_n is a non-empty subset of R^d",
    "H_2: For each positive integer n, K_n is compact",
    "¬Q: The intersection of all sets K_n from n=1 to infinity is empty"
]

N_HYP = 2
NEG_Q_INDEX = 2