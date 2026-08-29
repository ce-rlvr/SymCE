import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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
    Checks if the witness is a valid counterexample to the false conjecture.
    """
    # H_1: f: R \to S is a surjective ring homomorphism
    try:
        if isinstance(witness, dict):
            if 'is_surjective_homomorphism' in witness:
                h1 = bool(witness['is_surjective_homomorphism'])
            elif 'is_surjective' in witness and 'is_homomorphism' in witness:
                h1 = bool(witness['is_surjective'] and witness['is_homomorphism'])
            else:
                h1 = False
        else:
            if hasattr(witness, 'is_surjective_homomorphism'):
                h1 = bool(witness.is_surjective_homomorphism)
            elif hasattr(witness, 'is_surjective') and hasattr(witness, 'is_homomorphism'):
                h1 = bool(witness.is_surjective and witness.is_homomorphism)
            else:
                h1 = False
    except Exception:
        h1 = False

    # neg_Q: The Krull dimension of S is strictly greater than the Krull dimension of R
    try:
        if isinstance(witness, dict):
            if 'dim_R' in witness and 'dim_S' in witness:
                dim_R = witness['dim_R']
                dim_S = witness['dim_S']
            elif 'R' in witness and 'S' in witness:
                dim_R = witness['R']['krull_dimension']
                dim_S = witness['S']['krull_dimension']
            else:
                dim_R = 0
                dim_S = -1
        else:
            if hasattr(witness, 'dim_R') and hasattr(witness, 'dim_S'):
                dim_R = witness.dim_R
                dim_S = witness.dim_S
            elif hasattr(witness, 'domain') and hasattr(witness, 'codomain'):
                dim_R = witness.domain.krull_dimension
                dim_S = witness.codomain.krull_dimension
            elif hasattr(witness, 'R') and hasattr(witness, 'S'):
                dim_R = witness.R.krull_dimension
                dim_S = witness.S.krull_dimension
            else:
                dim_R = 0
                dim_S = -1
                
        neg_q = float(dim_S) > float(dim_R)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f: R to S is a surjective ring homomorphism",
    "¬Q: The Krull dimension of S is strictly greater than the Krull dimension of R"
]

N_HYP = 1
NEG_Q_INDEX = 1