import sympy
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f: R -> S is a ring homomorphism",
    "H_2: e in R is an idempotent element (e^2 = e)",
    "¬Q: f(e) is not an idempotent element in S"
]

N_HYP = 2
NEG_Q_INDEX = 2

def safe_eq(x, y):
    """Safely compare two elements, handling numpy/sympy arrays."""
    try:
        res = (x == y)
        if isinstance(res, bool):
            return res
        if hasattr(res, 'all'):
            return bool(res.all())
        return bool(res)
    except Exception:
        return False

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture.
    The witness should provide:
      - R: iterable of domain elements
      - S: iterable of codomain elements
      - f: callable or dict mapping R to S
      - e: the element in R
      - add_R, mul_R, add_S, mul_S: optional callables for ring operations (default to +, *)
      - eq_R, eq_S: optional callables for equality (default to safe_eq)
      - one_R, one_S: optional identities to check unital homomorphism
    """
    try:
        if isinstance(witness, dict):
            R = list(witness.get('R', []))
            S = list(witness.get('S', []))
            f_raw = witness.get('f')
            e = witness.get('e')
            add_R = witness.get('add_R', lambda x, y: x + y)
            mul_R = witness.get('mul_R', lambda x, y: x * y)
            add_S = witness.get('add_S', lambda x, y: x + y)
            mul_S = witness.get('mul_S', lambda x, y: x * y)
            eq_R = witness.get('eq_R', safe_eq)
            eq_S = witness.get('eq_S', safe_eq)
            one_R = witness.get('one_R', None)
            one_S = witness.get('one_S', None)
        else:
            R = list(getattr(witness, 'R', []))
            S = list(getattr(witness, 'S', []))
            f_raw = getattr(witness, 'f', None)
            e = getattr(witness, 'e', None)
            add_R = getattr(witness, 'add_R', lambda x, y: x + y)
            mul_R = getattr(witness, 'mul_R', lambda x, y: x * y)
            add_S = getattr(witness, 'add_S', lambda x, y: x + y)
            mul_S = getattr(witness, 'mul_S', lambda x, y: x * y)
            eq_R = getattr(witness, 'eq_R', safe_eq)
            eq_S = getattr(witness, 'eq_S', safe_eq)
            one_R = getattr(witness, 'one_R', None)
            one_S = getattr(witness, 'one_S', None)
            
        if f_raw is None or e is None:
            return [False, False, False]

        if isinstance(f_raw, dict):
            def dict_f(x):
                for k, v in f_raw.items():
                    if eq_R(k, x):
                        return v
                raise KeyError(x)
            f = dict_f
        else:
            f = f_raw
            
    except Exception:
        return [False, False, False]

    def contains(collection, item, eq_func):
        for x in collection:
            if eq_func(x, item):
                return True
        return False

    # H_1: f: R -> S is a ring homomorphism
    try:
        h1 = True
        if one_R is not None and one_S is not None:
            if not eq_S(f(one_R), one_S):
                h1 = False
        
        if h1:
            for x in R:
                if not contains(S, f(x), eq_S):
                    h1 = False
                    break
                for y in R:
                    if not eq_S(f(add_R(x, y)), add_S(f(x), f(y))):
                        h1 = False
                        break
                    if not eq_S(f(mul_R(x, y)), mul_S(f(x), f(y))):
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: e in R is an idempotent element (e^2 = e)
    try:
        h2 = contains(R, e, eq_R) and eq_R(mul_R(e, e), e)
    except Exception:
        h2 = False

    # ¬Q: f(e) is NOT an idempotent element in S
    try:
        fe = f(e)
        neg_q = not eq_S(mul_S(fe, fe), fe)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]