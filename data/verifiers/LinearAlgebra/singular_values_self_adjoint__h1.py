import sympy as sp

# Top-level setup: named object bindings
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, neg_Q_ok].
    """
    # H_1: Let T be a self-adjoint linear operator on V.
    try:
        if not isinstance(witness, sp.Matrix):
            h1 = False
        elif witness.rows != witness.cols:
            h1 = False
        else:
            # In a standard inner product space, self-adjoint means Hermitian (T = T^H)
            h1 = bool(witness == witness.H)
    except Exception:
        h1 = False

    # ¬Q: The singular values of T are NOT the absolute values of the eigenvalues of T.
    try:
        if not isinstance(witness, sp.Matrix) or witness.rows != witness.cols:
            neg_q = False
        else:
            svals = witness.singular_values()
            evals = witness.eigenvals()
            
            abs_evals = []
            for val, mult in evals.items():
                for _ in range(mult):
                    abs_evals.append(sp.Abs(val))
            
            # Try numerical evaluation first for robustness against symbolic forms
            try:
                svals_num = sorted([float(sp.re(sp.N(v))) for v in svals])
                abs_evals_num = sorted([float(sp.re(sp.N(v))) for v in abs_evals])
                
                q = len(svals_num) == len(abs_evals_num) and all(
                    abs(s - e) <= 1e-7 for s, e in zip(svals_num, abs_evals_num)
                )
            except Exception:
                # Fallback to symbolic comparison if numerical evaluation fails
                q = len(svals) == len(abs_evals)
                if q:
                    unmatched = list(abs_evals)
                    for s in svals:
                        match_found = False
                        for i, e in enumerate(unmatched):
                            if sp.simplify(s - e) == 0:
                                unmatched.pop(i)
                                match_found = True
                                break
                        if not match_found:
                            q = False
                            break
            
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: T is a self-adjoint linear operator",
    "¬Q: The singular values of T are not the absolute values of its eigenvalues"
]

N_HYP = 1
NEG_Q_INDEX = 1