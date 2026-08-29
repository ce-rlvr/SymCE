import sympy
from sympy import ZZ, QQ, S
from sympy.abc import x

# Top-level setup
class InfiniteDomainRing:
    def __init__(self, name="Z"):
        self.name = name
    def __str__(self):
        return self.name

class PrincipalIdeal:
    def __init__(self, gen, ring):
        self.gen = gen
        self.ring = ring

Z_ring = InfiniteDomainRing("Z")
Z_ideal = PrincipalIdeal(1, Z_ring)

try:
    Qx_ring = QQ[x]
except Exception:
    Qx_ring = None

def is_ring(R):
    if R in (ZZ, S.Integers): return True
    if hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing: return True
    if isinstance(R, InfiniteDomainRing): return True
    return False

def get_I_R(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        a, b = witness
        if is_ring(b): return a, b
        if is_ring(a): return b, a
        return a, b
    if is_ring(witness):
        if witness in (ZZ, S.Integers):
            return 1, witness
        if isinstance(witness, InfiniteDomainRing):
            return PrincipalIdeal(1, witness), witness
        if hasattr(witness, 'one'):
            return witness.one, witness
        return witness, witness
    if isinstance(witness, PrincipalIdeal):
        return witness, witness.ring
    return witness, None

def conditions(witness) -> list[bool]:
    I, R = get_I_R(witness)
    
    try:
        if R is None:
            h1 = False
        elif R in (ZZ, S.Integers):
            if isinstance(I, (int, sympy.Integer)):
                h1 = (int(I) != 0)
            else:
                h1 = False
        elif hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing:
            h1 = (R(I) != R.zero)
        elif isinstance(R, InfiniteDomainRing):
            if isinstance(I, PrincipalIdeal) and I.ring == R:
                h1 = (I.gen != 0)
            elif isinstance(I, (int, sympy.Integer)):
                h1 = (int(I) != 0)
            else:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if R in (ZZ, S.Integers):
            # The ring of integers is not Artinian and has no minimal non-zero ideals
            contains_min = False
        elif hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing:
            # Polynomial rings over a field are not Artinian and have no minimal non-zero ideals
            contains_min = False
        elif isinstance(R, InfiniteDomainRing):
            # Custom infinite domain ring (like Z) has no minimal non-zero ideals
            contains_min = False
        else:
            # If we don't recognize the ring, assume it might contain one to fail the counterexample check
            contains_min = True
            
        neg_q = not contains_min
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is a non-zero right ideal of R",
    "¬Q: I does not contain a minimal non-zero right ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1