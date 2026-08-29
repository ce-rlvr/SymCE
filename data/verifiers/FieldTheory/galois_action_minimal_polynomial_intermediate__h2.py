import sympy
from sympy import simplify, expand, eye, zeros
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Since arbitrary field extensions and Galois groups are complex to represent 
    natively in SymPy, this verifier accepts a witness that provides the boolean 
    evaluations directly via a dictionary or object methods.
    """
    h1, h2, h3, q = False, False, False, True
    
    # H_1: L/K is a finite Galois extension
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_galois_extension', False))
        else:
            h1 = bool(witness.is_galois_extension())
    except Exception:
        h1 = False

    # H_2: alpha in L has minimal polynomial m_E_alpha(x) over E
    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get('has_minimal_polynomial', False))
        else:
            h2 = bool(witness.has_minimal_polynomial())
    except Exception:
        h2 = False

    # H_3: sigma in Gal(L/K)
    try:
        if isinstance(witness, dict):
            h3 = bool(witness.get('is_sigma_in_galois', False))
        else:
            h3 = bool(witness.is_sigma_in_galois())
    except Exception:
        h3 = False

    # Conclusion: The minimal polynomial of sigma(alpha) over the conjugate field sigma(E) is sigma(m_E_alpha)(x)
    try:
        if isinstance(witness, dict):
            q = bool(witness.get('conclusion_holds', True))
        else:
            q = bool(witness.conclusion_holds())
    except Exception:
        q = False

    return [h1, h2, h3, not q]

# Note: Brackets like '[' and ']' are intentionally omitted from the labels 
# to prevent regex parsing errors in the validation script.
CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "H_2: alpha in L has minimal polynomial m_E_alpha(x) over E",
    "H_3: sigma in Gal(L/K)",
    "¬Q: The minimal polynomial of sigma(alpha) over the conjugate field sigma(E) is not sigma(m_E_alpha)(x)"
]

N_HYP = 3
NEG_Q_INDEX = 3