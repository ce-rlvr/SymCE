import sympy
from sympy import symbols, Rational, Integer
from sympy.abc import x, y, z
import math

# Top-level setup for potential witness expressions
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z10 = 10
Z12 = 12
ZZ = 0

def parse_witness(witness):
    """
    Parses the witness into a modulus n (where n=0 means Z) and a normalized list of elements S.
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        R, S = witness
        if isinstance(R, int):
            n = abs(R)
        elif hasattr(R, 'is_IntegerRing') and R.is_IntegerRing:
            n = 0
        elif hasattr(R, 'modulus'):
            n = int(R.modulus)
        else:
            sR = str(R)
            if sR in ('ZZ', 'Integers', 'Z'):
                n = 0
            else:
                try:
                    n = abs(int(R))
                except Exception:
                    n = 0
    elif isinstance(witness, (list, set, tuple)):
        n = 0
        S = witness
    else:
        raise ValueError("Invalid witness format")
        
    if n > 0:
        S_norm = list(set(e % n for e in S))
    else:
        S_norm = list(set(S))
        
    return n, S_norm

def conditions(witness) -> list[bool]:
    try:
        n, S = parse_witness(witness)
    except Exception:
        return [False, False, False]
    
    # H_1: S is a multiplicatively closed subset of R
    try:
        if n == 0:
            h1 = all((a * b) in S for a in S for b in S)
        else:
            h1 = all(((a * b) % n) in S for a in S for b in S)
    except Exception:
        h1 = False

    # H_2: \phi: R \to S^{-1}R is the canonical map given by \phi(r) = r/1
    # This implies that 1 must be in S for the map to be defined in this form.
    try:
        if n == 0:
            h2 = 1 in S
        elif n == 1:
            h2 = 0 in S  # In the zero ring, 1 = 0
        else:
            h2 = 1 in S
    except Exception:
        h2 = False

    # Conclusion: The map \phi is injective if and only if no element of S is a zero divisor in R
    try:
        # Check if S contains any zero divisors of R
        # (Standard definition: a zero divisor is a NONZERO element that kills a nonzero element)
        has_zd = False
        if n > 0:
            for s in S:
                if s != 0 and math.gcd(s, n) > 1:
                    has_zd = True
                    break
        else:
            has_zd = False  # Z has no nonzero zero divisors
        
        no_zd_in_S = not has_zd

        # Check if phi is injective
        # phi(r) = 0/1 iff there exists t in S such that t*r = 0
        is_injective = True
        if n > 0:
            for r in range(1, n):
                killed = False
                for t in S:
                    if (t * r) % n == 0:
                        killed = True
                        break
                if killed:
                    is_injective = False
                    break
        else:
            # In Z, phi is injective iff 0 is not in S
            if 0 in S:
                is_injective = False
            else:
                is_injective = True
        
        # The conjecture claims these two properties are equivalent
        conclusion = (is_injective == no_zd_in_S)
        
        # We want the negated conclusion (True if the conjecture fails at the witness)
        neg_q = not conclusion

    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: phi is the canonical map given by phi(r) = r/1 (implies 1 in S)",
    "¬Q: phi is injective XOR no element of S is a zero divisor in R"
]

N_HYP = 2
NEG_Q_INDEX = 2