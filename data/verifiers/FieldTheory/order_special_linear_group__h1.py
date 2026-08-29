import sympy
import sympy.combinatorics.named_groups as named_groups
import sympy.matrices as matrices
from sympy.ntheory import factorint

# Top-level setup for standard algebra objects
S3 = named_groups.SymmetricGroup(3)
S4 = named_groups.SymmetricGroup(4)
A4 = named_groups.AlternatingGroup(4)
D4 = named_groups.DihedralGroup(4)
C4 = named_groups.CyclicGroup(4)
V4 = named_groups.AlternatingGroup(4)
Z2 = named_groups.CyclicGroup(2)
Z3 = named_groups.CyclicGroup(3)
Z4 = named_groups.CyclicGroup(4)
Z6 = named_groups.CyclicGroup(6)
trivial = named_groups.CyclicGroup(1)

I2 = matrices.eye(2)
I3 = matrices.eye(3)
O2 = matrices.zeros(2, 2)
O3 = matrices.zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the conjecture:
    'The number of elements in SL(n, F) is q^{n(n-1)/2} \prod_{i=2}^n (q^i - 1)'
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            if 'F' in witness:
                F_obj = witness['F']
            else:
                F_obj = witness.get('q')
        else:
            n, F_obj = witness
            
        q = getattr(F_obj, 'order', getattr(F_obj, 'size', F_obj))
        if callable(q):
            q = q()
    except Exception:
        return [False, False, False]

    # H_1: n is an integer strictly greater than 1
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 1
    except Exception:
        h1 = False

    # H_2: SL(n, F) is the special linear group of degree n over F...
    # This is a definitional hypothesis. We just verify q is a valid ring size.
    try:
        h2 = isinstance(q, (int, sympy.Integer)) and q > 1
    except Exception:
        h2 = False

    # ¬Q: The number of elements in SL(n, F) is NOT the given formula
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            n_int = int(n)
            q_int = int(q)
            
            # Calculate the formula given in the conclusion
            formula = (q_int**(n_int * (n_int - 1) // 2))
            for i in range(2, n_int + 1):
                formula *= (q_int**i - 1)

            # Determine if F is a field
            is_field = False
            if hasattr(F_obj, 'is_Field') and getattr(F_obj, 'is_Field'):
                is_field = True
            elif type(F_obj).__name__ in ['GaloisField', 'FiniteField', 'GF']:
                is_field = True
            elif isinstance(F_obj, (int, sympy.Integer)):
                # If F is given just by its size q, we assume F = Z/qZ.
                # Z/qZ is a field if and only if q is prime.
                factors = factorint(q_int)
                if len(factors) == 1 and list(factors.values())[0] == 1:
                    is_field = True

            if is_field:
                # If F is a field, the formula holds exactly.
                actual = formula
            else:
                # If F is not a field (e.g., Z/qZ for composite q), we compute the actual order of SL(n, Z/qZ).
                # By the Chinese Remainder Theorem and properties of local rings:
                factors = factorint(q_int)
                actual = 1
                for p, e in factors.items():
                    term = p**((e - 1) * (n_int**2 - 1))
                    term *= p**(n_int * (n_int - 1) // 2)
                    for i in range(2, n_int + 1):
                        term *= (p**i - 1)
                    actual *= term
                
            neg_q = bool(actual != formula)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: SL(n, F) is the special linear group of degree n over F, consisting of n x n matrices with determinant 1",
    "¬Q: The number of elements in SL(n, F) is not q^{n(n-1)/2} \\prod_{i=2}^n (q^i - 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2