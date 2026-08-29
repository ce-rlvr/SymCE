import sympy
from sympy import symbols

# Standard symbols that might be used
x, y, z = symbols('x y z')

class RingProfile:
    """
    Represents homological properties of a ring R and a module k = R/m.
    Since SymPy does not natively compute global and projective dimensions 
    for arbitrary rings, witnesses can be provided as instances of this class 
    or as dictionaries with equivalent keys.
    """
    def __init__(self, is_residue_field, global_dim, proj_dim_k):
        self.is_residue_field = is_residue_field
        self.global_dim = global_dim
        self.proj_dim_k = proj_dim_k

# Pre-defined counterexample:
# R = C[x] x C[x,y], m = (x) x C[x,y]
# k = R/m = C (a field, so is_residue_field is True)
# global_dim(R) = max(global_dim(C[x]), global_dim(C[x,y])) = max(1, 2) = 2
# proj_dim_R(k) = proj_dim_{C[x]}(C) = 1
# Thus global_dim(R) != proj_dim_R(k)
Counterexample1 = RingProfile(is_residue_field=True, global_dim=2, proj_dim_k=1)

def conditions(witness) -> list[bool]:
    # H_1: k = R/\mathfrak{m} is the residue field of R
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_residue_field', False))
        else:
            h1 = bool(witness.is_residue_field)
    except Exception:
        h1 = False

    # ¬Q: The global dimension of R is NOT equal to the projective dimension of k as an R-module
    try:
        if isinstance(witness, dict):
            neg_q = witness.get('global_dim') != witness.get('proj_dim_k')
        else:
            neg_q = witness.global_dim != witness.proj_dim_k
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k = R/\\mathfrak{m} is the residue field of R",
    "¬Q: The global dimension of R is not equal to the projective dimension of k as an R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1