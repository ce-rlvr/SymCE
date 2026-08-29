import sympy
from sympy import isprime
from sympy.polys.domains import ZZ, QQ

# Top-level setup
# In this module, an integer n >= 0 represents the commutative ring Z/nZ.
# (n = 0 represents Z, n = 1 represents the trivial ring, n > 1 represents Z/nZ).
# A tuple of integers represents the direct product of such rings.
# SymPy domains like ZZ and QQ are also supported.

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool):
            n = int(witness)
            if n >= 0:
                h1 = True
                if n == 0:
                    neg_q = False
                else:
                    neg_q = not isprime(n)
                    
        elif isinstance(witness, tuple) and len(witness) > 0 and all(isinstance(x, (int, sympy.Integer)) and not isinstance(x, bool) and int(x) >= 0 for x in witness):
            h1 = True
            non_trivial = [int(x) for x in witness if int(x) != 1]
            if len(non_trivial) > 1:
                # A product of multiple non-trivial rings has zero divisors,
                # so it cannot embed in a field.
                neg_q = True
            elif len(non_trivial) == 1:
                n = non_trivial[0]
                if n == 0:
                    neg_q = False
                else:
                    neg_q = not isprime(n)
            else:
                # The trivial ring does not embed in a field (1 != 0 in fields)
                neg_q = True
                
        elif hasattr(witness, 'is_Ring') and witness.is_Ring:
            h1 = True
            if witness.__class__.__name__ == 'IntegerModRing':
                neg_q = not isprime(witness.mod)
            else:
                # Standard SymPy domains (ZZ, QQ, RR, CC, K[x]) are integral domains
                # and therefore embed in their field of fractions.
                neg_q = False
                
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: There does not exist a field F and an injective ring homomorphism from R to F"
]

N_HYP = 1
NEG_Q_INDEX = 1