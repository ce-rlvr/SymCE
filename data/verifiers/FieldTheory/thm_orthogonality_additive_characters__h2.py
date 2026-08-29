import sympy
from sympy.matrices import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    Checks if the witness is a counterexample to the false conjecture.
    The witness should be a list, tuple, or dict representing the values of 
    an additive character psi on a finite prime field F = GF(p).
    For example, witness = [1, 1] represents the trivial character on GF(2).
    """
    try:
        if isinstance(witness, dict):
            p = len(witness)
            if set(witness.keys()) != set(range(p)):
                return [False, False]
            mapping = witness
        elif isinstance(witness, (list, tuple)):
            p = len(witness)
            mapping = {i: witness[i] for i in range(p)}
        else:
            return [False, False]
            
        if p < 2 or not sympy.isprime(p):
            h1 = False
        else:
            is_char = True
            for x in range(p):
                # A character maps to the multiplicative group of non-zero complex numbers
                if sympy.simplify(mapping[x]) == 0:
                    is_char = False
                    break
                for y in range(p):
                    val1 = mapping[(x + y) % p]
                    val2 = mapping[x] * mapping[y]
                    if sympy.simplify(val1 - val2) != 0:
                        is_char = False
                        break
                if not is_char:
                    break
            h1 = is_char
    except Exception:
        h1 = False

    try:
        total = sum(mapping.values())
        neg_q = bool(sympy.simplify(total) != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field and psi is an additive character on F",
    "¬Q: The sum of psi(x) over F is not equal to 0"
]

N_HYP = 1
NEG_Q_INDEX = 1