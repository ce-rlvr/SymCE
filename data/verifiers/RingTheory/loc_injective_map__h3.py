import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    witness is expected to be a tuple (n, S) representing the ring R = Z/nZ 
    (or Z if n=0) and a subset S of R.
    """
    try:
        if hasattr(witness, 'n') and hasattr(witness, 'S'):
            n = witness.n
            S = witness.S
        elif isinstance(witness, tuple) and len(witness) == 2:
            ring, S = witness
            if ring == sympy.ZZ:
                n = 0
            elif hasattr(ring, 'mod'):
                n = ring.mod
            else:
                n = int(ring)
        else:
            return [False, False, False]
            
        n = abs(int(n))
        S = list(set(int(x) for x in S))
    except Exception:
        return [False, False, False]

    # H1: R is a commutative ring with identity
    # Z and Z/nZ are always commutative rings with identity.
    h1 = True

    # H2: S is a multiplicatively closed subset of R
    try:
        h2 = True
        if not S:
            h2 = False
        else:
            # Check if 1 is in S
            if n == 0:
                if 1 not in S:
                    h2 = False
            else:
                if not any((s % n) == (1 % n) for s in S):
                    h2 = False
            
            # Check closure under multiplication
            if h2:
                for x in S:
                    for y in S:
                        if n == 0:
                            prod = x * y
                            if prod not in S:
                                h2 = False
                                break
                        else:
                            prod = (x * y) % n
                            if not any(prod == (s % n) for s in S):
                                h2 = False
                                break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # Negated Conclusion: The map phi is injective iff no element of S is a zero divisor in R
    try:
        # Check if phi is injective
        # phi is injective iff ker(phi) == {0}
        # ker(phi) = {r in R | exists s in S, s*r = 0}
        if n == 0:
            phi_injective = (0 not in S)
        else:
            phi_injective = True
            for r in range(1, n):
                for s in S:
                    if (s * r) % n == 0:
                        phi_injective = False
                        break
                if not phi_injective:
                    break
                    
        # Check if no element of S is a zero divisor
        # Definition: a is a zero divisor if a != 0 and exists b != 0 such that a*b = 0
        no_zero_divisors = True
        for s in S:
            if n == 0:
                # In Z, there are no zero divisors (0 is not a zero divisor by this definition)
                pass
            else:
                s_mod = s % n
                if s_mod == 0:
                    continue
                is_zd = False
                for b in range(1, n):
                    if (s_mod * b) % n == 0:
                        is_zd = True
                        break
                if is_zd:
                    no_zero_divisors = False
                    break
                    
        # The conclusion is (phi_injective == no_zero_divisors)
        # We want the negated conclusion
        neg_q = bool(phi_injective != no_zero_divisors)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The map phi is injective XOR no element of S is a zero divisor in R"
]

N_HYP = 2
NEG_Q_INDEX = 2