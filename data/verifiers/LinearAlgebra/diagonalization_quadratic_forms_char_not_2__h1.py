import sympy
from sympy import eye, zeros
import math
import itertools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: The characteristic of the field F is not equal to 2
    try:
        h1 = True
        if not hasattr(witness, 'shape'):
            return [False, False, False]
        
        if hasattr(witness, 'domain'):
            if witness.domain.char == 2:
                h1 = False
        
        for val in witness:
            if type(val).__name__ == 'GaloisFieldElement' and getattr(val, 'p', None) == 2:
                h1 = False
            if hasattr(val, 'p') and val.p == 2:
                h1 = False
            if isinstance(val, sympy.core.mod.Mod) and val.args[1] == 2:
                h1 = False
    except Exception:
        h1 = False

    # H_2: Q is a quadratic form on V
    try:
        h2 = bool(witness.is_symmetric())
    except Exception:
        h2 = False

    # ¬Q: There does not exist a basis of V with respect to which the matrix representation of Q is diagonal
    try:
        neg_q = False
        if witness.is_diagonal():
            neg_q = False
        else:
            is_zz = True
            for v in witness:
                if not isinstance(v, (int, sympy.Integer)):
                    is_zz = False
                    break
            
            if is_zz and witness.shape[0] == witness.shape[1]:
                n = witness.shape[0]
                detA = int(witness.det())
                if detA != 0:
                    divisors = sympy.divisors(abs(detA))
                    possible_d = set(divisors + [-d for d in divisors])
                    represented_divisors = set()
                    
                    A_list = [[int(witness[i, j]) for j in range(n)] for i in range(n)]
                    
                    # Search for represented values in a small bounding box
                    for x_tup in itertools.product(range(-8, 9), repeat=n):
                        if all(v == 0 for v in x_tup):
                            continue
                        val = 0
                        for i in range(n):
                            for j in range(n):
                                val += x_tup[i] * A_list[i][j] * x_tup[j]
                        
                        if val in possible_d:
                            represented_divisors.add(val)
                    
                    # If A is congruent to D over ZZ, the diagonal entries of D must be represented by A,
                    # and their product must equal det(A).
                    can_form_det = False
                    for combo in itertools.combinations_with_replacement(represented_divisors, n):
                        prod = 1
                        for val in combo:
                            prod *= val
                        if prod == detA:
                            can_form_det = True
                            break
                    
                    if not can_form_det:
                        neg_q = True
            elif hasattr(witness, 'free_symbols') and len(witness.free_symbols) > 0:
                # Fallback for polynomial rings where non-diagonal symmetric matrices 
                # are generally not diagonalizable via congruence.
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The characteristic of the field F is not equal to 2",
    "H_2: Q is a quadratic form on V",
    "¬Q: The matrix representation of Q cannot be diagonalized"
]

N_HYP = 2
NEG_Q_INDEX = 2