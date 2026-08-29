import sympy

def check_h1(witness):
    if not callable(witness):
        return False
    try:
        for n in range(1, 15):
            I_n = witness(n)
            if not isinstance(I_n, sympy.Interval):
                return False
        return True
    except Exception:
        return False

def check_h2(witness):
    if not callable(witness):
        return False
    try:
        for n in range(1, 15):
            I_n = witness(n)
            if not isinstance(I_n, sympy.Interval):
                return False
            left_closed = (not I_n.left_open) or (I_n.start == sympy.S.NegativeInfinity)
            right_closed = (not I_n.right_open) or (I_n.end == sympy.S.Infinity)
            if not (left_closed and right_closed):
                return False
        return True
    except Exception:
        return False

def check_h3(witness):
    if not callable(witness):
        return False
    try:
        for n in range(1, 15):
            I_n = witness(n)
            I_n_plus_1 = witness(n+1)
            if not isinstance(I_n, sympy.Interval) or not isinstance(I_n_plus_1, sympy.Interval):
                return False
            if I_n_plus_1.is_subset(I_n) != True:
                return False
        return True
    except Exception:
        return False

def check_neg_q(witness):
    if not callable(witness):
        return False
    n = sympy.Symbol('n', integer=True, positive=True)
    try:
        I_n = witness(n)
        if isinstance(I_n, sympy.Interval):
            a_n = I_n.start
            b_n = I_n.end
            a_inf = sympy.limit(a_n, n, sympy.oo)
            b_inf = sympy.limit(b_n, n, sympy.oo)
            if a_inf == sympy.oo or b_inf == -sympy.oo:
                return True
            if not a_inf.has(sympy.Limit) and not b_inf.has(sympy.Limit):
                return False
    except Exception:
        pass
    
    # Fallback numeric check
    try:
        a_1000 = float(witness(1000).start)
        a_10000 = float(witness(10000).start)
        a_100000 = float(witness(100000).start)
        
        if a_100000 > a_10000 > a_1000 and (a_100000 - a_10000) > 0.1:
            return True
    except Exception:
        pass

    try:
        b_1000 = float(witness(1000).end)
        b_10000 = float(witness(10000).end)
        b_100000 = float(witness(100000).end)
        
        if b_100000 < b_10000 < b_1000 and (b_10000 - b_100000) > 0.1:
            return True
    except Exception:
        pass
        
    return False

def conditions(witness):
    return [
        check_h1(witness),
        check_h2(witness),
        check_h3(witness),
        check_neg_q(witness)
    ]

CONDITION_LABELS = [
    "H_1: (I_n) is a sequence of intervals in the real numbers",
    "H_2: Each interval I_n is closed",
    "H_3: I_{n+1} is a subset of I_n for all natural numbers n",
    "¬Q: The intersection of all intervals I_n is empty"
]

N_HYP = 3
NEG_Q_INDEX = 3