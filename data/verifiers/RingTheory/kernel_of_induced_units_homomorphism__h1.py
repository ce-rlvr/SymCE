import itertools
from sympy import eye, zeros, Rational, Integer, Symbol
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def extract(witness, name):
    if isinstance(witness, dict):
        return witness.get(name)
    return getattr(witness, name, None)

def get_func(witness, name, default=None):
    obj = extract(witness, name)
    if obj is None:
        return default
    if isinstance(obj, dict):
        return lambda val: obj[val]
    return obj

def get_bin_op(witness, name):
    obj = extract(witness, name)
    if obj is None:
        return None
    if isinstance(obj, dict):
        return lambda a, b: obj[(a, b)]
    return obj

def conditions(witness):
    try:
        R = extract(witness, 'R')
        S = extract(witness, 'S')
        add_R = get_bin_op(witness, 'add_R')
        mul_R = get_bin_op(witness, 'mul_R')
        zero_R = extract(witness, 'zero_R')
        one_R = extract(witness, 'one_R')
        add_S = get_bin_op(witness, 'add_S')
        mul_S = get_bin_op(witness, 'mul_S')
        zero_S = extract(witness, 'zero_S')
        one_S = extract(witness, 'one_S')
        f = get_func(witness, 'f')

        if None in (R, S, add_R, mul_R, zero_R, one_R, add_S, mul_S, zero_S, one_S, f):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: f is a ring homomorphism such that f(1_R) = 1_S
    h1_ok = True
    try:
        if f(one_R) != one_S:
            h1_ok = False
        else:
            for a in R:
                for b in R:
                    if f(add_R(a, b)) != add_S(f(a), f(b)):
                        h1_ok = False
                        break
                    if f(mul_R(a, b)) != mul_S(f(a), f(b)):
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # H2: f^\times is the induced group homomorphism on the groups of units
    h2_ok = True
    try:
        # Find units of R
        R_units = []
        for u in R:
            for v in R:
                if mul_R(u, v) == one_R and mul_R(v, u) == one_R:
                    R_units.append(u)
                    break
                    
        # Find units of S
        S_units = []
        for u in S:
            for v in S:
                if mul_S(u, v) == one_S and mul_S(v, u) == one_S:
                    S_units.append(u)
                    break
                    
        # Check if f maps R_units to S_units
        for u in R_units:
            if f(u) not in S_units:
                h2_ok = False
                break
                
        f_times = get_func(witness, 'f_times')
        if f_times is None:
            f_times = f
        else:
            for u in R_units:
                if f_times(u) != f(u):
                    h2_ok = False
                    break
    except Exception:
        h2_ok = False

    # Negated Conclusion: ker(f^\times) != {u \in R^\times | u - 1 \in ker(f)}
    neg_q_ok = False
    try:
        # ker(f^\times)
        ker_f_times = []
        for u in R_units:
            if f_times(u) == one_S:
                ker_f_times.append(u)
                
        # Find -1_R
        neg_one_R = None
        for x in R:
            if add_R(one_R, x) == zero_R and add_R(x, one_R) == zero_R:
                neg_one_R = x
                break
                
        if neg_one_R is None:
            neg_q_ok = False
        else:
            set_conclusion = []
            for u in R_units:
                u_minus_1 = add_R(u, neg_one_R)
                if f(u_minus_1) == zero_S:
                    set_conclusion.append(u)
                    
            # Compare sets
            def same_set(l1, l2):
                for x in l1:
                    if x not in l2: return False
                for x in l2:
                    if x not in l1: return False
                return True
                
            is_subgroup = True
            # check closure under multiplication
            for a in set_conclusion:
                for b in set_conclusion:
                    if mul_R(a, b) not in set_conclusion:
                        is_subgroup = False
            # check identity
            if one_R not in set_conclusion:
                is_subgroup = False
            # check inverses
            for a in set_conclusion:
                inv_a = None
                for v in R_units:
                    if mul_R(a, v) == one_R and mul_R(v, a) == one_R:
                        inv_a = v
                        break
                if inv_a not in set_conclusion:
                    is_subgroup = False
                    
            if not is_subgroup or not same_set(ker_f_times, set_conclusion):
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism such that f(1_R) = 1_S",
    "H_2: f^x is the induced group homomorphism on the groups of units",
    "¬Q: The kernel of f^x is NOT the subgroup of R^x consisting of units u such that u - 1 in ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2