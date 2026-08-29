import sympy as sp

# Top-level setup
# No specific named bindings needed for this field theory conjecture.

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) > 1:
            n_val = witness[0]
            zeta_val = witness[1]
            if type(n_val) is int or isinstance(n_val, sp.Integer):
                n = int(n_val)
                if n == 0:
                    h1 = False
                else:
                    abs_n = abs(n)
                    if sp.simplify(sp.expand(zeta_val**abs_n - 1)) != 0:
                        h1 = False
                    else:
                        is_prim = True
                        for k in range(1, abs_n):
                            if abs_n % k == 0:
                                if sp.simplify(sp.expand(zeta_val**k - 1)) == 0:
                                    is_prim = False
                                    break
                        h1 = is_prim
            else:
                h1 = False
        else:
            n_val = witness[0] if isinstance(witness, tuple) and len(witness) > 0 else witness
            if type(n_val) is int or isinstance(n_val, sp.Integer):
                n = int(n_val)
                h1 = (n != 0)
            else:
                h1 = False
    except Exception:
        h1 = False

    try:
        n_val = witness[0] if isinstance(witness, tuple) and len(witness) > 0 else witness
        if type(n_val) is int or isinstance(n_val, sp.Integer):
            n = int(n_val)
            # The conclusion states that x^n - 1 is a polynomial and its splitting field is Q(zeta_n).
            # If n < 0, x^n - 1 is not a polynomial, so the conclusion is false (neg_q is True).
            # If n > 0, x^n - 1 is a polynomial and the conclusion is true (neg_q is False).
            neg_q = (n < 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: zeta_n is a primitive n-th root of unity in C",
    "¬Q: Q(zeta_n) is not the splitting field of the polynomial x^n-1 over Q"
]

N_HYP = 1
NEG_Q_INDEX = 1