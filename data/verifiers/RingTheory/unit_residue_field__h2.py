import math
import sympy

# Top-level setup
# (No named bindings needed for number theory / Z/nZ rings; use integers directly)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness is expected to be a tuple (n, m_gen, x_val) where:
      - n represents the commutative ring R = Z/nZ (n=0 means R = Z)
      - m_gen represents the generator of a maximal ideal m = <m_gen> in R
      - x_val represents the element x in R
    """
    try:
        n, m_gen, x_val = witness
    except Exception:
        return [False, False, False]
    
    try:
        # H_1: R is a commutative ring
        # We also verify that m_gen generates a valid maximal ideal in R to match the theorem context.
        # For Z/nZ (n > 1) or Z (n = 0), an ideal <m_gen> is maximal iff m_gen is a prime dividing n (or any prime if n=0).
        h1 = (isinstance(n, (int, sympy.Integer)) and (n == 0 or n > 1) and 
              isinstance(m_gen, (int, sympy.Integer)) and (n % m_gen == 0) and 
              sympy.isprime(m_gen))
    except Exception:
        h1 = False

    try:
        # H_2: x is an element of R
        h2 = isinstance(x_val, (int, sympy.Integer))
    except Exception:
        h2 = False

    try:
        # Conclusion: x is a unit in R if and only if the image of x in R/m is non-zero
        # In Z/nZ (or Z), x is a unit iff gcd(x, n) == 1.
        is_unit = math.gcd(int(x_val), int(n)) == 1
        
        # The image of x in R/m is non-zero iff x is not in m, i.e., x is not a multiple of m_gen.
        is_nonzero_mod_m = (int(x_val) % int(m_gen)) != 0
        
        q = (is_unit == is_nonzero_mod_m)
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: x is an element of R",
    "¬Q: It is false that x is a unit in R if and only if the image of x in R/m is non-zero"
]

N_HYP = 2
NEG_Q_INDEX = 2