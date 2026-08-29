import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        h1 = bool(witness.is_square and witness.is_symmetric())
    except Exception:
        h1 = False

    try:
        # LHS: A is positive definite
        # Evaluated by checking if all eigenvalues are strictly positive real numbers.
        # This extends the concept to non-Hermitian matrices, which is necessary here
        # because the dropped hypothesis is "A is a real matrix".
        evs = witness.eigenvals()
        lhs = True
        for ev in evs:
            if getattr(ev, 'is_real', False) != True:
                lhs = False
                break
            try:
                if not bool(ev > 0):
                    lhs = False
                    break
            except TypeError:
                lhs = False
                break
                
        # RHS: exists an invertible n x n real matrix P such that A = P^T P
        # If such P exists, P^T P is a real matrix, so A must be a real matrix.
        is_real = True
        for e in witness:
            if getattr(e, 'is_real', False) != True:
                is_real = False
                break
                
        if is_real:
            # For real matrices, P exists iff A is symmetric and positive definite.
            rhs = bool(witness.is_symmetric() and lhs)
        else:
            rhs = False
            
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a symmetric matrix",
    "¬Q: A is positive definite iff there exists an invertible n x n real matrix P such that A = P^T P fails"
]

N_HYP = 1
NEG_Q_INDEX = 1