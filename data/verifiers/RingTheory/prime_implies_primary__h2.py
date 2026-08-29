import sympy
from sympy import isprime

ZZ = sympy.ZZ
QQ = sympy.QQ

def get_n(witness):
    if isinstance(witness, int):
        return witness
    if hasattr(witness, 'is_Integer') and witness.is_Integer:
        return int(witness)
    if hasattr(witness, 'ring') and witness.ring == sympy.ZZ:
        if hasattr(witness, 'gens') and len(witness.gens) == 1:
            return int(witness.gens[0])
    if isinstance(witness, str):
        digits = ''.join(filter(str.isdigit, witness))
        if digits:
            return int(digits)
    if isinstance(witness, tuple) or isinstance(witness, list):
        if len(witness) == 2 and witness[0] == sympy.ZZ:
            return get_n(witness[1])
        for item in witness:
            if isinstance(item, int):
                return item
            if hasattr(item, 'is_Integer') and item.is_Integer:
                return int(item)
    raise ValueError("Could not parse witness")

def conditions(witness) -> list[bool]:
    try:
        n = get_n(witness)
        n = abs(n)
        
        # H_1: R is a commutative ring with identity
        # We evaluate the witness in the context of R = Z, which satisfies this.
        h1 = True
        
        # Conclusion Q: P is a P-primary ideal in R
        # An ideal P is P-primary iff it is primary and its radical is P.
        # This is equivalent to P being a prime ideal.
        # In Z, the ideal nZ is prime iff n == 0 or n is prime.
        q = (n == 0) or isprime(n)
        neg_q = not q
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: P is not a P-primary ideal in R"
]

N_HYP = 1
NEG_Q_INDEX = 1