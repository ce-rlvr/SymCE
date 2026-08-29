import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    # H_1: A is a 2x2 matrix over a commutative ring
    # Note: The original true theorem requires a commutative ring. The false conjecture 
    # dropped this requirement in its formal statement, allowing non-commutative entries.
    # We check that it is a 2x2 matrix.
    try:
        if hasattr(witness, 'shape') and witness.shape == (2, 2):
            if not isinstance(witness, sp.Matrix):
                A = sp.Matrix(witness)
            else:
                A = witness
            h1 = True
        else:
            A = witness
            h1 = False
    except Exception:
        h1 = False
        A = witness

    # H_2: tr(A) is the trace of A
    try:
        if hasattr(A, 'shape') and A.shape == (2, 2):
            _ = A[0, 0] + A[1, 1]
            h2 = True
        else:
            _ = A.trace()
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: A^2 - tr(A)A + det(A)I != 0
    try:
        if hasattr(A, 'shape') and A.shape == (2, 2):
            # Compute manually to safely handle non-commutative symbols without sympy det() issues
            tr = A[0, 0] + A[1, 1]
            det = A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]
        else:
            tr = A.trace()
            det = A.det()
            
        I = sp.eye(2)
        
        # Calculate the Cayley-Hamilton expression
        res = sp.expand(A**2 - tr * A + det * I)
        
        is_zero = True
        for i in range(2):
            for j in range(2):
                elem = res[i, j]
                if elem == 0:
                    continue
                if getattr(elem, 'is_zero', None) is True:
                    continue
                if sp.simplify(elem) == 0:
                    continue
                is_zero = False
                break
            if not is_zero:
                break
                
        neg_q = not is_zero
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a 2x2 matrix over a commutative ring",
    "H_2: tr(A) is the trace of A",
    "¬Q: A^2 - tr(A)A + det(A)I != 0"
]

N_HYP = 2
NEG_Q_INDEX = 2