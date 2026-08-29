import sympy
from sympy import Matrix, eye, zeros, Dummy

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, Matrix):
            return [False]
        if not witness.is_square:
            return [False]
        
        # Check if the matrix has only rational entries
        is_rational_matrix = True
        for val in witness:
            if not getattr(val, 'is_Rational', False):
                is_rational_matrix = False
                break
        
        if is_rational_matrix:
            # For a rational matrix, it has a Jordan form over Q iff all eigenvalues are rational
            eigenvals = witness.eigenvals()
            splits = all(getattr(val, 'is_Rational', False) for val in eigenvals.keys())
            neg_q = not splits
        else:
            # Check if the matrix has only real entries
            is_real_matrix = True
            for val in witness:
                if getattr(val, 'is_real', None) is not True:
                    is_real_matrix = False
                    break
            
            if is_real_matrix:
                # For a real matrix, it has a Jordan form over R iff all eigenvalues are real
                eigenvals = witness.eigenvals()
                splits = all(getattr(val, 'is_real', False) for val in eigenvals.keys())
                neg_q = not splits
            else:
                # Fallback for symbolic or complex matrices: check if characteristic polynomial splits
                lam = Dummy('lambda')
                p = witness.charpoly(lam)
                factors = p.factor_list()
                splits = all(f.degree() == 1 for f, mult in factors[1])
                neg_q = not splits
            
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: A does not have a Jordan Normal Form over its base field (characteristic polynomial does not split)"
]

N_HYP = 0
NEG_Q_INDEX = 0