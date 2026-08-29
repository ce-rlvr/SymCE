import sympy
from sympy import isprime, Symbol, Poly

# Top-level setup for potential witness expressions
ZZ = "ZZ"
QQ_x = "QQ[x]"
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "If R is a commutative ring with identity and P is a prime ideal of R, 
    then P is a maximal ideal of R."
    
    The witness can be an integer `n` (representing the ideal nZ in the ring ZZ),
    or a tuple `(ring_name, generator)` representing a principal ideal.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, (int, sympy.Integer)):
            # Assume R = ZZ, P = nZZ
            n = abs(int(witness))
            h1 = True  # ZZ is a commutative ring with identity
            h2 = (n == 0 or isprime(n))  # nZZ is prime iff n=0 or n is prime
            neg_q = not isprime(n)       # nZZ is not maximal iff n is not prime (0 is not maximal)
            
        elif isinstance(witness, tuple) and len(witness) == 2:
            ring, gen = witness
            
            if ring == "ZZ" or ring == sympy.S.Integers:
                n = abs(int(gen))
                h1 = True
                h2 = (n == 0 or isprime(n))
                neg_q = not isprime(n)
                
            elif str(ring) in ("QQ[x]", "RR[x]", "CC[x]"):
                p = Poly(gen, x)
                h1 = True
                is_zero = p.is_zero
                try:
                    is_irred = p.is_irreducible
                except Exception:
                    is_irred = False
                h2 = is_zero or is_irred
                neg_q = not is_irred
                
            elif str(ring) == "ZZ[x]":
                h1 = True
                if gen == 0 or gen == x:
                    h2 = True
                    neg_q = True
                else:
                    p = Poly(gen, x)
                    is_zero = p.is_zero
                    try:
                        is_irred = p.is_irreducible
                    except Exception:
                        is_irred = False
                    h2 = is_zero or is_irred
                    # No principal ideal in ZZ[x] is maximal
                    neg_q = True
    except Exception:
        pass

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: P is a prime ideal of R",
    "¬Q: P is not a maximal ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2