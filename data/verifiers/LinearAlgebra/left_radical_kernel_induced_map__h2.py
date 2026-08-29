import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference.
v1, v2, w1, w2 = sp.symbols('v1 v2 w1 w2')
v1_sym, v2_sym, w1_sym, w2_sym = v1, v2, w1, w2

def evaluate_B(witness, v, w):
    """Evaluates the witness bilinear-like form B(v, w)."""
    if callable(witness):
        res = witness(v, w)
        if isinstance(res, sp.Matrix):
            res = res[0]
        return sp.sympify(res)
    elif isinstance(witness, sp.Matrix):
        res = v.T * witness * w
        return sp.sympify(res[0])
    else:
        res = witness.subs({v1: v[0], v2: v[1], w1: w[0], w2: w[1]})
        return sp.sympify(res)

def is_nonzero(diff):
    """Safely checks if a sympy expression is non-zero, accounting for float inaccuracies."""
    diff = sp.simplify(diff)
    if diff == 0:
        return False
    try:
        return abs(float(diff)) > 1e-12
    except TypeError:
        return True

def conditions(witness) -> list[bool]:
    # H1 and H2 are structural properties of the vector spaces and dual spaces.
    # We fix V = R^2 and W = R^2 for the evaluation, making these trivially true.
    h1 = True
    h2 = True
    
    # Test vectors and scalars
    vs = [sp.Matrix([1, 0]), sp.Matrix([0, 1]), sp.Matrix([2, -3]), sp.Matrix([-1, 4])]
    ws = [sp.Matrix([1, 0]), sp.Matrix([0, 1]), sp.Matrix([-1, 4]), sp.Matrix([3, 2])]
    scalars = [sp.Rational(2, 1), sp.Rational(-1, 3)]
    
    # H3: L_B is a map from V to W^* defined by L_B(v)(w) = B(v,w).
    # For L_B(v) to be in W^*, B(v, w) must be linear in w.
    try:
        h3 = True
        for v in vs:
            for w_a in ws:
                for w_b in ws:
                    diff = evaluate_B(witness, v, w_a + w_b) - (evaluate_B(witness, v, w_a) + evaluate_B(witness, v, w_b))
                    if is_nonzero(diff):
                        h3 = False
                        break
                if not h3: break
            if not h3: break
            
            for w_a in ws:
                for c in scalars:
                    diff = evaluate_B(witness, v, c * w_a) - c * evaluate_B(witness, v, w_a)
                    if is_nonzero(diff):
                        h3 = False
                        break
                if not h3: break
            if not h3: break
    except Exception:
        h3 = False

    # neg_Q: The conclusion states "The kernel of the linear map L_B is equal to the left radical of B."
    # If B is linear in v, L_B is a linear map and its kernel is ALWAYS the left radical.
    # The conclusion fails if and only if L_B is NOT a linear map (i.e., B is not linear in v).
    try:
        is_linear_v = True
        for w_a in ws:
            for v_a in vs:
                for v_b in vs:
                    diff = evaluate_B(witness, v_a + v_b, w_a) - (evaluate_B(witness, v_a, w_a) + evaluate_B(witness, v_b, w_a))
                    if is_nonzero(diff):
                        is_linear_v = False
                        break
                if not is_linear_v: break
            if not is_linear_v: break
            
            for v_a in vs:
                for c in scalars:
                    diff = evaluate_B(witness, c * v_a, w_a) - c * evaluate_B(witness, v_a, w_a)
                    if is_nonzero(diff):
                        is_linear_v = False
                        break
                if not is_linear_v: break
            if not is_linear_v: break
            
        neg_q = not is_linear_v
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "H_2: W^* is the dual space of W",
    "H_3: L_B is a map from V to W^* defined by L_B(v)(w) = B(v,w)",
    "¬Q: The linear map L_B does not exist (B is not linear in v) or its kernel is not the left radical"
]

N_HYP = 3
NEG_Q_INDEX = 3