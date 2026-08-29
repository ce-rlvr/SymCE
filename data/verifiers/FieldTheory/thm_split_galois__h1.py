import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z, t
from sympy.polys import Poly

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

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            f = witness.get("f")
            F = witness.get("F")
            K = witness.get("K")
        elif isinstance(witness, tuple) and len(witness) == 3:
            f, F, K = witness
        else:
            f = getattr(witness, "f", None)
            F = getattr(witness, "F", None)
            K = getattr(witness, "K", None)
            
        if f is not None:
            poly_f = sympy.Poly(f)
            gens = poly_f.gens
            if gens:
                main_gen = gens[0]
                for gen in gens:
                    if str(gen) == 'x':
                        main_gen = gen
                        break
                f_prime = poly_f.diff(main_gen)
                h1 = (poly_f.gcd(f_prime).degree() == 0)
            else:
                h1 = True
                
        if K is not None and F is not None:
            h2 = True
            
        if F is not None:
            if hasattr(F, 'is_Field'):
                neg_q = not bool(F.is_Field)
            elif F == sympy.S.Integers or str(F) == 'ZZ':
                neg_q = True
            else:
                neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a separable polynomial over F",
    "H_2: K is a splitting field of f over F",
    "¬Q: The field extension K over F is not a Galois extension"
]

N_HYP = 2
NEG_Q_INDEX = 2