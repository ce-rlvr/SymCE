import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Standard group theory and linear algebra objects
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
    k_provided = False
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            if 'k' in witness:
                k = witness['k']
                k_provided = True
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                p, k = witness
                k_provided = True
            elif len(witness) == 1:
                p = witness[0]
            else:
                return [False, False]
        elif hasattr(witness, 'p'):
            p = witness.p
            if hasattr(witness, 'k'):
                k = witness.k
                k_provided = True
        else:
            p = witness
    except Exception:
        return [False, False]

    # H1: p is an odd prime number
    try:
        h1 = bool(sympy.isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False

    # neg_Q: The multiplicative group of units (Z/p^k Z)* is NOT a cyclic group
    if not k_provided:
        # If k is not provided, the universal statement over k is false (e.g., fails for k = -1)
        neg_q = True
    else:
        try:
            n = p**k
            
            # Attempt to safely cast to integer if mathematically an integer
            if isinstance(n, (int, sympy.Integer)):
                pass
            elif hasattr(n, 'is_integer') and n.is_integer:
                n = int(n)
            elif isinstance(n, float) and n.is_integer():
                n = int(n)
            else:
                try:
                    if int(n) == n:
                        n = int(n)
                except Exception:
                    pass

            # Check if n is a valid modulus for a cyclic group of units
            if not isinstance(n, (int, sympy.Integer)):
                neg_q = True
            elif n <= 0:
                neg_q = True
            elif n == 1:
                # Z/1Z has unit group {0}, which is cyclic
                neg_q = False
            else:
                # For n >= 2, the group of units is cyclic iff n = 2, 4, q^m, or 2q^m for odd prime q.
                if n in (2, 4):
                    neg_q = False
                else:
                    temp_n = n
                    if temp_n % 2 == 0:
                        temp_n = temp_n // 2
                    
                    factors = sympy.factorint(temp_n)
                    if len(factors) == 1:
                        q = list(factors.keys())[0]
                        if q % 2 != 0:
                            neg_q = False
                        else:
                            neg_q = True
                    else:
                        neg_q = True
        except Exception:
            neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "¬Q: The multiplicative group of units (Z/p^k Z)* is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1