import sympy
from sympy import symbols, Poly
from sympy.ntheory import factorint
from sympy.abc import x, y, z

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, (int, sympy.Integer)):
            n = abs(int(witness))
            if n <= 1:
                return [False, False, False, False]
                
            h1 = (n != 2)
            h2 = (n != 3)
            h3 = not any((a**2 + 3) % n == 0 for a in range(n))
            
            factors = factorint(n)
            if len(factors) > 1:
                neg_q = True
            else:
                neg_q = any((k**2 - k + 1) % n == 0 for k in range(n))
                
            return [h1, h2, h3, neg_q]
            
        else:
            try:
                char = witness.characteristic()
                h1 = (char != 2)
            except Exception:
                h1 = False
                
            try:
                char = witness.characteristic()
                h2 = (char != 3)
            except Exception:
                h2 = False
                
            try:
                p_z = Poly(z**2 + 3, z, domain=witness)
                rts = p_z.ground_roots()
                h3 = (len(rts) == 0)
            except Exception:
                h3 = False
                
            try:
                p = Poly(x**2 - x*y + y**2, x, y, domain=witness)
                neg_q = not p.is_irreducible
            except Exception:
                neg_q = False
                
            return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: The characteristic of K is not 2",
    "H_2: The characteristic of K is not 3",
    "H_3: There is no element a in K such that a^2 + 3 = 0",
    "¬Q: The polynomial x^2 - xy + y^2 is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3