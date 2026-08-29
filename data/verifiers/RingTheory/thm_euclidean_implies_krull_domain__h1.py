import sympy
from sympy.polys.domains import ZZ, QQ, EX
from sympy.ntheory import isprime
from sympy import symbols
from sympy.matrices import Matrix, eye, zeros

# Top-level setup
x, y, z = symbols('x y z')
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Check if the witness is a Krull domain.
        # A Krull domain must be an integral domain.
        if hasattr(witness, 'is_IntegralDomain'):
            # SymPy domains (ZZ, QQ, poly rings, etc.) have this property.
            # All implemented SymPy integral domains are Krull domains.
            is_krull = bool(witness.is_IntegralDomain)
        elif isinstance(witness, int) or (hasattr(witness, 'is_integer') and witness.is_integer):
            # Integers can represent the ring Z/nZ.
            n = abs(int(witness))
            if n == 0:
                is_krull = True  # Z is a Krull domain
            else:
                is_krull = isprime(n)  # Z/nZ is a Krull domain iff it is a field (n is prime)
        elif hasattr(witness, 'is_Matrix') and witness.is_Matrix:
            # Matrix rings over a field/domain are not integral domains for n >= 2
            is_krull = (witness.shape == (1, 1))
        else:
            # If the witness type is unrecognized, we default to True 
            # so that neg_q becomes False, safely rejecting the invalid witness.
            is_krull = True
            
        neg_q = not is_krull
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is not a Krull domain"
]

N_HYP = 0
NEG_Q_INDEX = 0