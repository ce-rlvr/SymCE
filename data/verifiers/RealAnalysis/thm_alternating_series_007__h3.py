import sympy
import math
import itertools
import functools

# Top-level setup
n = sympy.Symbol('n', integer=True, positive=True)

def conditions(witness):
    try:
        witness = sympy.sympify(witness)
    except Exception:
        pass

    # H1: (a_n) is a sequence of real numbers
    h1_ok = True
    for i in range(1, 101):
        try:
            val = witness.subs(n, i).evalf()
            if not val.is_real or not val.is_finite:
                h1_ok = False
                break
        except Exception:
            h1_ok = False
            break

    # H2: a_n >= 0 for all n
    h2_ok = True
    for i in range(1, 101):
        try:
            val = witness.subs(n, i).evalf()
            if not val.is_real or val < -1e-12:
                h2_ok = False
                break
        except Exception:
            h2_ok = False
            break
            
    if h2_ok:
        for i in [1000, 10000, 100000]:
            try:
                val = witness.subs(n, i).evalf()
                if not val.is_real or val < -1e-12:
                    h2_ok = False
                    break
            except Exception:
                pass

    # H3: The limit of a_n as n approaches infinity is 0
    h3_ok = False
    lim_evaluated = False
    try:
        lim = sympy.limit(witness, n, sympy.oo)
        lim_evaluated = True
        if lim == 0:
            h3_ok = True
    except Exception:
        pass
        
    if not lim_evaluated:
        try:
            val = witness.subs(n, 100000).evalf()
            if val.is_real and abs(val) < 1e-4:
                h3_ok = True
        except Exception:
            pass

    # neg_Q: The alternating series sum_{n=1}^infty (-1)^n a_n diverges
    # We check this by verifying if the grouped series sum (a_{2k} - a_{2k-1}) diverges.
    # Since a_n -> 0, the alternating series converges iff the grouped series converges.
    neg_q = False
    k = sympy.Symbol('k', integer=True, positive=True)
    try:
        a_2k = witness.subs(n, 2*k)
        a_2k_minus_1 = witness.subs(n, 2*k - 1)
        
        try:
            a_2k = sympy.simplify(a_2k)
            a_2k_minus_1 = sympy.simplify(a_2k_minus_1)
        except Exception:
            pass
            
        term = a_2k - a_2k_minus_1
        
        conv = None
        try:
            conv = sympy.Sum(term, (k, 1, sympy.oo)).is_convergent()
            if conv is sympy.S.false:
                neg_q = True
            elif conv is sympy.S.true:
                neg_q = False
        except Exception:
            pass
            
        if not neg_q and conv is not sympy.S.true:
            # Fallback 1: Limit comparison with 1/k
            try:
                lim1 = sympy.limit(k * term, k, sympy.oo)
                if lim1.is_extended_real and lim1 != 0:
                    neg_q = True
            except Exception:
                pass
                
        if not neg_q and conv is not sympy.S.true:
            # Fallback 2: Limit comparison with 1/(k log k)
            try:
                lim2 = sympy.limit(k * sympy.log(k) * term, k, sympy.oo)
                if lim2.is_extended_real and lim2 != 0:
                    neg_q = True
            except Exception:
                pass
                
        if not neg_q and conv is not sympy.S.true:
            # Fallback 3: n-th term test for the grouped series
            try:
                lim3 = sympy.limit(term, k, sympy.oo)
                if lim3.is_extended_real and lim3 != 0:
                    neg_q = True
            except Exception:
                pass
                
    except Exception:
        pass

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: (a_n) is a sequence of real numbers",
    "H_2: a_n >= 0 for all n",
    "H_3: The limit of a_n as n approaches infinity is 0",
    "¬Q: The alternating series sum_{n=1}^infty (-1)^n a_n diverges"
]

N_HYP = 3
NEG_Q_INDEX = 3