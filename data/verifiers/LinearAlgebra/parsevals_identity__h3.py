import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should provide the orthonormal basis E and the vector v.
    Expected format: witness = (E, v) or witness = (V, E, v) or witness = {'E': E, 'v': v}
    """
    try:
        if isinstance(witness, dict):
            E = witness.get('E')
            v = witness.get('v')
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                _, E, v = witness
            elif len(witness) == 2:
                E, v = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if E is None or v is None:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: Let V be a finite-dimensional inner product space.
    # We verify this by checking that E is a list/tuple of column vectors 
    # and v is a column vector of the same dimension.
    try:
        if not isinstance(E, (list, tuple)):
            h1_ok = False
        elif not isinstance(v, Matrix):
            h1_ok = False
        else:
            m = v.shape[0]
            h1_ok = (v.shape[1] == 1) and all(isinstance(e, Matrix) and e.shape == (m, 1) for e in E)
    except Exception:
        h1_ok = False

    # H_2: Let {e_1, e_2, ..., e_n} be an orthonormal basis for V.
    # Since V is implicitly the span of E, E is a basis for V if it is linearly independent.
    # Orthonormality implies linear independence, so we just check if E is an orthonormal set.
    try:
        if not h1_ok:
            h2_ok = False
        else:
            h2_ok = True
            for i in range(len(E)):
                for j in range(len(E)):
                    dot_prod = sympy.simplify(E[i].vdot(E[j]))
                    if i == j:
                        if dot_prod != 1:
                            h2_ok = False
                    else:
                        if dot_prod != 0:
                            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: The conclusion fails (i.e., ||v||^2 != sum_{i=1}^n |<v, e_i>|^2)
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            lhs = sympy.simplify(v.vdot(v))
            rhs = 0
            for e in E:
                # |<v, e>|^2 = <v, e> * <e, v>
                rhs += sympy.simplify(v.vdot(e) * e.vdot(v))
            
            neg_q_ok = bool(sympy.simplify(lhs - rhs) != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional inner product space",
    "H_2: {e_1, e_2, ..., e_n} is an orthonormal basis for V",
    "¬Q: ||v||^2 != sum_{i=1}^n |<v, e_i>|^2"
]

N_HYP = 2
NEG_Q_INDEX = 2