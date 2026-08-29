import itertools
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    'The element (r, m) is a unit in R \ltimes M if and only if r is a unit in R.'
    """
    
    def get_val(key):
        if isinstance(witness, dict):
            return witness[key]
        return getattr(witness, key)
        
    def call_op(op, *args):
        if isinstance(op, dict):
            return op[args]
        return op(*args)

    try:
        R = list(get_val('R'))
        M = list(get_val('M'))
        R_add = get_val('R_add')
        R_mul = get_val('R_mul')
        M_add = get_val('M_add')
        act_L = get_val('action_left')
        act_R = get_val('action_right')
        r_val = get_val('r')
        m_val = get_val('m')
    except Exception:
        return [False, False, False, False]

    def check_H1():
        try:
            # Closure
            for a in R:
                for b in R:
                    if call_op(R_add, a, b) not in R: return False
                    if call_op(R_mul, a, b) not in R: return False
            # Associativity, commutativity, and distributivity
            for a in R:
                for b in R:
                    if call_op(R_add, a, b) != call_op(R_add, b, a): return False
                    for c in R:
                        if call_op(R_add, call_op(R_add, a, b), c) != call_op(R_add, a, call_op(R_add, b, c)): return False
                        if call_op(R_mul, call_op(R_mul, a, b), c) != call_op(R_mul, a, call_op(R_mul, b, c)): return False
                        if call_op(R_mul, a, call_op(R_add, b, c)) != call_op(R_add, call_op(R_mul, a, b), call_op(R_mul, a, c)): return False
                        if call_op(R_mul, call_op(R_add, a, b), c) != call_op(R_add, call_op(R_mul, a, c), call_op(R_mul, b, c)): return False
            # Additive identity
            zeros = [z for z in R if all(call_op(R_add, z, a) == a for a in R)]
            if len(zeros) != 1: return False
            zero = zeros[0]
            # Additive inverses
            for a in R:
                if not any(call_op(R_add, a, b) == zero for b in R): return False
            # Multiplicative identity
            ones = [u for u in R if all(call_op(R_mul, u, a) == a and call_op(R_mul, a, u) == a for a in R)]
            if len(ones) != 1: return False
            return True
        except Exception:
            return False

    def check_H2():
        try:
            # M is an abelian group
            for a in M:
                for b in M:
                    if call_op(M_add, a, b) not in M: return False
            for a in M:
                for b in M:
                    if call_op(M_add, a, b) != call_op(M_add, b, a): return False
                    for c in M:
                        if call_op(M_add, call_op(M_add, a, b), c) != call_op(M_add, a, call_op(M_add, b, c)): return False
            zeros = [z for z in M if all(call_op(M_add, z, a) == a for a in M)]
            if len(zeros) != 1: return False
            zero_M = zeros[0]
            for a in M:
                if not any(call_op(M_add, a, b) == zero_M for b in M): return False
                
            # Actions closure
            for r in R:
                for m in M:
                    if call_op(act_L, r, m) not in M: return False
                    if call_op(act_R, m, r) not in M: return False
                    
            # Trivial extension ring properties
            ext = list(itertools.product(R, M))
            def ext_add(x, y):
                return (call_op(R_add, x[0], y[0]), call_op(M_add, x[1], y[1]))
            def ext_mul(x, y):
                return (call_op(R_mul, x[0], y[0]), call_op(M_add, call_op(act_L, x[0], y[1]), call_op(act_R, x[1], y[0])))
                
            for x in ext:
                for y in ext:
                    if ext_add(x, y) not in ext: return False
                    if ext_mul(x, y) not in ext: return False
                    if ext_add(x, y) != ext_add(y, x): return False
                    for z in ext:
                        if ext_add(ext_add(x, y), z) != ext_add(x, ext_add(y, z)): return False
                        if ext_mul(ext_mul(x, y), z) != ext_mul(x, ext_mul(y, z)): return False
                        if ext_mul(x, ext_add(y, z)) != ext_add(ext_mul(x, y), ext_mul(x, z)): return False
                        if ext_mul(ext_add(x, y), z) != ext_add(ext_mul(x, z), ext_mul(y, z)): return False
            return True
        except Exception:
            return False

    def check_H3():
        try:
            return r_val in R and m_val in M
        except Exception:
            return False

    def check_neg_Q():
        try:
            # Check if r is a unit in R
            ones = [u for u in R if all(call_op(R_mul, u, a) == a and call_op(R_mul, a, u) == a for a in R)]
            if len(ones) != 1: return False
            one_R = ones[0]
            r_is_unit = any(call_op(R_mul, r_val, s) == one_R and call_op(R_mul, s, r_val) == one_R for s in R)
            
            # Check if (r, m) is a unit in R \ltimes M
            ext = list(itertools.product(R, M))
            def ext_mul(x, y):
                return (call_op(R_mul, x[0], y[0]), call_op(M_add, call_op(act_L, x[0], y[1]), call_op(act_R, x[1], y[0])))
                
            ext_ones = [u for u in ext if all(ext_mul(u, a) == a and ext_mul(a, u) == a for a in ext)]
            if len(ext_ones) == 1:
                one_ext = ext_ones[0]
                ext_is_unit = any(ext_mul((r_val, m_val), s) == one_ext and ext_mul(s, (r_val, m_val)) == one_ext for s in ext)
            else:
                # If the extension ring has no multiplicative identity, it has no units
                ext_is_unit = False
                
            # The conclusion states: ext_is_unit <==> r_is_unit
            # We return True if the conclusion FAILS
            return ext_is_unit != r_is_unit
        except Exception:
            return False

    return [check_H1(), check_H2(), check_H3(), check_neg_Q()]

CONDITION_LABELS = [
    "H_1: R is a unital ring",
    "H_2: R \\ltimes M is the trivial extension ring",
    "H_3: (r, m) is an element of R \\ltimes M",
    "¬Q: (r, m) is a unit in R \\ltimes M iff r is a unit in R is false"
]

N_HYP = 3
NEG_Q_INDEX = 3