import sympy
import sympy.ntheory
from sympy.polys.domains import ZZ, QQ, RR, CC, Domain
from sympy import Symbol

# Top-level setup
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

def conditions(witness):
    # Map common SymPy sets to their Domain equivalents for convenience
    if witness == sympy.S.Integers:
        witness = ZZ
    elif witness == sympy.S.Rationals:
        witness = QQ
    elif witness == sympy.S.Reals:
        witness = RR
    elif witness == sympy.S.Complexes:
        witness = CC

    # H_1: R is a commutative ring with identity
    try:
        # In SymPy, all implemented Domains are commutative rings with identity
        h1 = isinstance(witness, Domain)
    except Exception:
        h1 = False

    # H_2: The Jacobson radical of R is the zero ideal
    try:
        if getattr(witness, 'is_Field', False):
            h2 = True
        elif witness == ZZ:
            h2 = True
        elif witness.__class__.__name__ == 'IntegerModRing':
            # For Z/nZ, the Jacobson radical is zero iff n is square-free
            h2 = sympy.ntheory.is_squarefree(witness.mod)
        elif hasattr(witness, 'dom') and hasattr(witness, 'gens'):
            # Polynomial rings or fraction fields
            if getattr(witness, 'is_FractionField', False):
                h2 = True
            else:
                # R[x] has zero Jacobson radical if R is a field or ZZ
                h2 = getattr(witness.dom, 'is_Field', False) or witness.dom == ZZ
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: R is not isomorphic to a finite direct product of fields
    try:
        if getattr(witness, 'is_Field', False):
            is_fdpf = True
        elif witness.__class__.__name__ == 'IntegerModRing':
            # By the Chinese Remainder Theorem, Z/nZ is a finite direct product 
            # of fields iff n is square-free
            is_fdpf = sympy.ntheory.is_squarefree(witness.mod)
        else:
            # Other integral domains like ZZ or QQ[x] are not fields, 
            # hence not finite direct products of fields.
            is_fdpf = False
        
        neg_q = not is_fdpf
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: The Jacobson radical of R is the zero ideal",
    "¬Q: R is not isomorphic to a finite direct product of fields"
]

N_HYP = 2
NEG_Q_INDEX = 2