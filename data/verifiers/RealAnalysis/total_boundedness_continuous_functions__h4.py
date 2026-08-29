import sympy
import math

# Top-level setup: named object bindings that the witness expression may reference.
# We define common symbols for real variables (space) and integer variables (index).
x, y, t, z = sympy.symbols('x y t z', real=True)
n, m, k, i, j = sympy.symbols('n m k i j', integer=True, positive=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    Hypotheses:
      1. K is a compact metric space
      2. C(K) is the space of continuous real-valued functions on K equipped with the supremum norm
      3. A is a subset of C(K)
      4. A is equicontinuous on K
    Conclusion:
      A is totally bounded in C(K)
    """
    # Parse witness
    if isinstance(witness, dict):
        K = witness.get('K', [0, 1])
        A = witness.get('A', witness)
    else:
        K = [0, 1]
        A = witness

    try:
        A = sympy.sympify(A)
        free_syms = A.free_symbols
        var_x = x
        var_n = n
        for sym in free_syms:
            if sym.name in ['n', 'm', 'k', 'i', 'j']:
                var_n = sym
            elif sym.name in ['x', 'y', 't', 'z']:
                var_x = sym
    except Exception:
        var_x = x
        var_n = n

    # H_1: K is a compact metric space
    try:
        h1 = isinstance(K, list) and len(K) == 2 and K[0] < K[1]
        h1 = bool(h1)
    except Exception:
        h1 = False

    # H_2: C(K) is the space of continuous real-valued functions on K equipped with the supremum norm
    # This is a definitional hypothesis.
    h2 = True

    # H_3: A is a subset of C(K)
    try:
        h3 = True
        for n_val in [1, 2, 3]:
            for step in range(11):
                x_val = K[0] + step * (K[1] - K[0]) / 10
                val = float(A.subs({var_n: n_val, var_x: x_val}))
                if math.isnan(val) or math.isinf(val):
                    h3 = False
                    break
    except Exception:
        h3 = False

    # Check equicontinuity (used for H_4 and neg_Q)
    is_equicont = False
    try:
        deriv = sympy.diff(A, var_x)
        if var_n not in deriv.free_symbols:
            is_equicont = True
        else:
            max_deriv = 0
            for n_val in [1, 10, 100, 1000, 10000]:
                for step in range(11):
                    x_val = K[0] + step * (K[1] - K[0]) / 10
                    try:
                        val = abs(float(deriv.subs({var_n: n_val, var_x: x_val})))
                        if val > max_deriv:
                            max_deriv = val
                    except Exception:
                        pass
            if max_deriv <= 2000:
                is_equicont = True
    except Exception:
        pass

    if not is_equicont:
        try:
            for d in [1e-3, 1e-4, 1e-5]:
                max_diff = 0
                for n_val in [1, 10, 100, 1000, 10000]:
                    for step in range(21):
                        x_val = K[0] + step * (K[1] - K[0]) / 20
                        if x_val + d <= K[1]:
                            val1 = float(A.subs({var_n: n_val, var_x: x_val}))
                            val2 = float(A.subs({var_n: n_val, var_x: x_val + d}))
                            diff_val = abs(val1 - val2)
                            if diff_val > max_diff:
                                max_diff = diff_val
                if max_diff < 0.1:
                    is_equicont = True
                    break
        except Exception:
            pass

    h4 = is_equicont

    # Check pointwise boundedness (used for neg_Q)
    is_pw_bounded = True
    try:
        for step in range(11):
            x_val = K[0] + step * (K[1] - K[0]) / 10
            expr_x = A.subs(var_x, x_val)
            try:
                lim = sympy.limit(sympy.Abs(expr_x), var_n, sympy.oo)
                if lim == sympy.oo:
                    is_pw_bounded = False
                    break
            except Exception:
                pass
        
        if is_pw_bounded:
            for step in range(11):
                x_val = K[0] + step * (K[1] - K[0]) / 10
                vals = []
                for n_val in [1, 10, 100, 1000, 10000, 100000]:
                    try:
                        vals.append(abs(float(A.subs({var_n: n_val, var_x: x_val}))))
                    except Exception:
                        pass
                if len(vals) >= 2 and max(vals) > 1000 and max(vals) > 2 * min(vals):
                    is_pw_bounded = False
                    break
    except Exception:
        is_pw_bounded = False

    # neg_Q: A is not totally bounded in C(K)
    # By Arzelà-Ascoli, a set is totally bounded in C(K) iff it is equicontinuous and pointwise bounded.
    neg_q = not (is_equicont and is_pw_bounded)

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: K is a compact metric space",
    "H_2: C(K) is the space of continuous real-valued functions on K equipped with the supremum norm",
    "H_3: A is a subset of C(K)",
    "H_4: A is equicontinuous on K",
    "¬Q: A is not totally bounded in C(K)"
]

N_HYP = 4
NEG_Q_INDEX = 4