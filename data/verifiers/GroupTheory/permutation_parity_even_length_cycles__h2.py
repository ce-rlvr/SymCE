import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def extract_sigma_k(witness):
    if isinstance(witness, dict):
        return witness.get('sigma'), witness.get('k')
    elif isinstance(witness, (tuple, list)) and len(witness) == 2:
        return witness[0], witness[1]
    return None, None

def conditions(witness) -> list[bool]:
    try:
        sigma, k = extract_sigma_k(witness)
        h1_ok = isinstance(sigma, Permutation)
    except Exception:
        h1_ok = False

    try:
        sigma, k = extract_sigma_k(witness)
        if isinstance(sigma, Permutation) and isinstance(k, (int, sympy.Integer)):
            sigma_even = bool(sigma.is_even)
            k_even = (k % 2 == 0)
            neg_q_ok = (sigma_even != k_even)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: sigma is a permutation in the symmetric group S_n",
    "¬Q: sigma is an even permutation XOR k is an even integer"
]

N_HYP = 1
NEG_Q_INDEX = 1