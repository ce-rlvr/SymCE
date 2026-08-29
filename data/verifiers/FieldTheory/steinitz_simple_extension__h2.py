import sympy
from sympy import *
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.matrices
from sympy.matrices import eye, zeros

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
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            h1 = bool(witness[0])
            h2 = bool(witness[1])
            is_simple = bool(witness[2])
            fin_inter = bool(witness[3])
            neg_q = (is_simple != fin_inter)
            return [h1, h2, neg_q]
            
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_field', False))
            h2 = bool(witness.get('is_finite_extension', False))
            is_simple = bool(witness.get('is_simple_extension', False))
            fin_inter = bool(witness.get('has_finite_intermediate_fields', False))
            neg_q = (is_simple != fin_inter)
        else:
            h1 = bool(getattr(witness, 'is_field', False))
            h2 = bool(getattr(witness, 'is_finite_extension', False))
            is_simple = bool(getattr(witness, 'is_simple_extension', False))
            fin_inter = bool(getattr(witness, 'has_finite_intermediate_fields', False))
            neg_q = (is_simple != fin_inter)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E is a field",
    "H_2: The degree of the field extension is finite",
    "¬Q: The equivalence (E is a simple extension iff the number of intermediate fields is finite) FAILS"
]

N_HYP = 2
NEG_Q_INDEX = 2