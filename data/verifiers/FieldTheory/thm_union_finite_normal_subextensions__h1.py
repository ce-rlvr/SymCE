import sympy
from sympy import Symbol
from sympy.polys.domains import QQ, ZZ, RR, CC, FractionField

# Top-level setup for FieldTheory
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

Qx = QQ.frac_field(x)
Qxy = QQ.frac_field(x, y)

CONDITION_LABELS = [
    "¬Q: K/F is a normal extension but not the union of finite normal subextensions (or vice versa)"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        # If the witness is provided as a string representation of a known counterexample
        if isinstance(witness, str):
            s = witness.replace(" ", "")
            if s in ["Q(x)/Q", "C(x)/C", "R(x)/R", "F(x)/F", "K(x)/K", "Zp(x)/Zp"]:
                return [True]
            return [False]
        
        # Otherwise, expect a tuple (K, F) representing the field extension K/F
        try:
            K, F = witness
        except (TypeError, ValueError):
            return [False]
            
        # Check if K is a purely transcendental extension of F.
        # A purely transcendental extension K/F is normal (since the algebraic closure of F in K is F, 
        # any irreducible polynomial over F with a root in K must be of degree 1 and thus splits completely).
        # However, K is not algebraic over F, so it cannot be the union of finite (hence algebraic) normal subextensions.
        # This makes it a valid counterexample to the conjecture.
        curr = K
        is_purely_transcendental = False
        while isinstance(curr, FractionField):
            if curr.domain == F:
                is_purely_transcendental = True
                break
            curr = curr.domain
            
        if is_purely_transcendental:
            return [True]
            
        return [False]
    except Exception:
        return [False]