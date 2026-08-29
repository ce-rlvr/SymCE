import sympy
from sympy import S, Poly
from sympy.ntheory import factorint
import math

# Top-level setup
Z = S.Integers
Q = S.Rationals
x = sympy.Symbol('x')

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        # Extract the ideal generator from the witness
        if isinstance(witness, tuple) and len(witness) == 2:
            gen = witness[1]
        else:
            gen = witness
            
        # If it's a SymPy Ideal or similar object with 'gens'
        if hasattr(gen, 'gens'):
            gens = gen.gens
            if len(gens) == 1:
                gen = gens[0]
            else:
                # We only handle principal ideals in this verifier
                return [False, False]
                
        # If it's a collection of 1 element
        if isinstance(gen, (list, tuple, set)) and len(gen) == 1:
            gen = list(gen)[0]
            
        # Check if gen is an integer (ideal in Z)
        is_int = False
        if isinstance(gen, int):
            is_int = True
        elif hasattr(gen, 'is_Integer') and gen.is_Integer:
            is_int = True
            
        if is_int:
            n = int(gen)
            h1 = True
            if n == 0:
                rad = 0
            else:
                rad = math.prod(factorint(abs(n)).keys())
            neg_q = (abs(n) != rad)
            return [h1, neg_q]
            
        # Check if gen is a polynomial (ideal in F[x])
        if hasattr(gen, 'free_symbols') and len(gen.free_symbols) == 1:
            var = list(gen.free_symbols)[0]
            p = Poly(gen, var)
            sqf_part = p.sqf_part()
            h1 = True
            neg_q = (p.degree() != sqf_part.degree())
            return [h1, neg_q]
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "¬Q: The radical of I is not equal to I"
]

N_HYP = 1
NEG_Q_INDEX = 1