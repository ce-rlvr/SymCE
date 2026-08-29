import sympy
from sympy import Matrix, S, eye, zeros
import itertools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample.
    The witness should be a tuple (n, P) where:
      - n is the dimension of the vector space R^n (1 <= n <= 3)
      - P is a callable representing the operator P: R^n -> R^n
        which takes a sympy.Matrix of shape (n, 1) and returns one.
    """
    try:
        n, P = witness
        if not isinstance(n, int) or n < 1 or n > 3:
            return [False, False, False]
        if not callable(P):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: V is a vector space
    # By definition of our witness space (R^n), this is True.
    h1_ok = True

    try:
        test_scalars = [-2, -1, 0, 1, 2]
        test_vectors = [Matrix(v) for v in itertools.product(test_scalars, repeat=n)]
        
        # H_2: P^2 = P
        h2_ok = True
        for v in test_vectors:
            Pv = P(v.copy())
            PPv = P(Pv.copy())
            if Pv != PPv:
                h2_ok = False
                break
    except Exception:
        h2_ok = False

    try:
        # Check conclusion: im(P) and ker(P) are P-invariant subspaces of V.
        # We will test closure under addition and scalar multiplication.
        im_P = []
        ker_P = []
        zero_vec = zeros(n, 1)
        
        for v in test_vectors:
            Pv = P(v.copy())
            if Pv == v:
                im_P.append(v)
            if Pv == zero_vec:
                ker_P.append(v)
                
        conclusion_holds = True
        
        # A subspace must contain the zero vector
        if P(zero_vec.copy()) != zero_vec:
            conclusion_holds = False
            
        # Check if im(P) is a subspace (closed under addition)
        if conclusion_holds:
            for u in im_P:
                for v in im_P:
                    if P((u + v).copy()) != u + v:
                        conclusion_holds = False
                        break
                if not conclusion_holds:
                    break
                    
        # Check if im(P) is a subspace (closed under scalar multiplication)
        if conclusion_holds:
            scalars_for_mult = [-2, -1, -S(1)/2, S(1)/2, 1, 2, 3]
            for u in im_P:
                for c in scalars_for_mult:
                    if P((c * u).copy()) != c * u:
                        conclusion_holds = False
                        break
                if not conclusion_holds:
                    break

        # Check if ker(P) is a subspace (closed under addition)
        if conclusion_holds:
            for x in ker_P:
                for y in ker_P:
                    if P((x + y).copy()) != zero_vec:
                        conclusion_holds = False
                        break
                if not conclusion_holds:
                    break

        # Check if ker(P) is a subspace (closed under scalar multiplication)
        if conclusion_holds:
            for x in ker_P:
                for c in scalars_for_mult:
                    if P((c * x).copy()) != zero_vec:
                        conclusion_holds = False
                        break
                if not conclusion_holds:
                    break

        # P-invariance of ker(P) requires P(x) in ker(P) for x in ker(P).
        # Since P(x) = 0, this means 0 must be in ker(P), which is checked by P(0) == 0.
        # P-invariance of im(P) is always true if P^2 = P.

        neg_q_ok = not conclusion_holds

    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: P^2 = P",
    "¬Q: im(P) or ker(P) is not a P-invariant subspace"
]

N_HYP = 2
NEG_Q_INDEX = 2