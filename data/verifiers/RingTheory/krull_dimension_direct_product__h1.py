import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup
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
    neg_q = False
    try:
        dim_R1 = None
        dim_R2 = None
        dim_prod = None
        
        if isinstance(witness, dict):
            dim_R1 = witness.get('dim_R1')
            dim_R2 = witness.get('dim_R2')
            dim_prod = witness.get('dim_prod', witness.get('dim_R1xR2'))
        elif hasattr(witness, 'dim_R1'):
            dim_R1 = witness.dim_R1
            dim_R2 = witness.dim_R2
            dim_prod = getattr(witness, 'dim_prod', getattr(witness, 'dim_R1xR2', None))
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                try:
                    dim_R1 = witness[0].krull_dimension()
                    dim_R2 = witness[1].krull_dimension()
                    dim_prod = witness[2].krull_dimension()
                except AttributeError:
                    dim_R1, dim_R2, dim_prod = witness
            elif len(witness) == 2:
                dim_R1 = witness[0].krull_dimension()
                dim_R2 = witness[1].krull_dimension()
                try:
                    prod_ring = witness[0].product(witness[1])
                except AttributeError:
                    prod_ring = witness[0] * witness[1]
                dim_prod = prod_ring.krull_dimension()
        elif callable(witness):
            res = witness()
            if isinstance(res, (tuple, list)) and len(res) == 3:
                dim_R1, dim_R2, dim_prod = res
                
        if dim_R1 is not None and dim_R2 is not None and dim_prod is not None:
            neg_q = bool(dim_prod != max(dim_R1, dim_R2))
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The Krull dimension of R_1 x R_2 is not equal to max(dim(R_1), dim(R_2))"
]

N_HYP = 0
NEG_Q_INDEX = 0