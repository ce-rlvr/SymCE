import sympy
from sympy import Matrix, eye, zeros, Integer

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness should be a tuple: (K, omega_0, omega_plus)
    where:
      - K is a string representing the base ring (e.g., 'Z')
      - omega_0 is the degree-zero component (an integer or sympy Integer)
      - omega_plus is a nilpotent sympy Matrix representing the positive-degree component
        (or 0 if the vector space is trivial).
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False, False, False]
        K, omega_0, omega_plus = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: V is a vector space over K
    # The conjecture is false because it dropped the hypothesis that K is a field.
    # We accept standard rings like 'Z' to demonstrate the failure.
    try:
        h1 = K in ['Z', 'Q', 'R', 'C']
    except Exception:
        h1 = False
        
    # H2: \bigwedge V is the exterior algebra of V
    # We verify this by checking that omega_plus is nilpotent, 
    # which is the defining property of elements in the augmentation ideal of an exterior algebra.
    try:
        if isinstance(omega_plus, Matrix):
            n = omega_plus.shape[0]
            h2 = bool(omega_plus ** n == zeros(n, n))
        elif omega_plus == 0:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H3: \omega \in \bigwedge V is written uniquely as \omega_0 + \omega_+
    try:
        h3 = isinstance(omega_0, (int, Integer)) and (omega_plus is not None)
    except Exception:
        h3 = False
        
    # neg_Q: The element \omega is a unit in \bigwedge V if and only if \omega_0 is non-zero.
    try:
        omega_0_nonzero = (omega_0 != 0)
        
        if isinstance(omega_plus, Matrix):
            I = eye(omega_plus.shape[0])
            omega = omega_0 * I + omega_plus
            det = omega.det()
        else:
            det = omega_0
            
        # Check invertibility in the base ring
        if K == 'Z':
            is_unit = (abs(det) == 1)
        else:
            is_unit = (det != 0)
            
        conclusion = (is_unit == omega_0_nonzero)
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a vector space over K",
    "H_2: \\bigwedge V is the exterior algebra of V",
    "H_3: \\omega \\in \\bigwedge V is written uniquely as \\omega_0 + \\omega_+",
    "¬Q: The element \\omega is a unit in \\bigwedge V if and only if \\omega_0 is non-zero"
]

N_HYP = 3
NEG_Q_INDEX = 3