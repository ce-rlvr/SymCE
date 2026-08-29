import sympy
from sympy import Matrix

class VectorSpace:
    def __init__(self, field, dimension):
        self.field = field
        self.dimension = dimension

class LinearOperator:
    def __init__(self, space, has_jcf):
        self.space = space
        self.has_jcf = has_jcf

# Top-level setup: named object bindings that the witness expression may reference.
# Since the conjecture drops the "finite-dimensional" hypothesis, the counterexamples
# are linear operators on infinite-dimensional vector spaces.
C_inf = VectorSpace(sympy.CC, sympy.oo)

LeftShift = LinearOperator(C_inf, has_jcf=False)
RightShift = LinearOperator(C_inf, has_jcf=False)
Derivative = LinearOperator(C_inf, has_jcf=False)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, LinearOperator):
            # H_1: K is an algebraically closed field
            if witness.space.field == sympy.CC:
                h1 = True
            elif hasattr(witness.space.field, 'is_algebraically_closed') and witness.space.field.is_algebraically_closed:
                h1 = True
                
            # H_2: T is a linear operator on V
            h2 = True
            
            # ¬Q: T does not have a Jordan canonical form
            neg_q = not witness.has_jcf
            
        elif isinstance(witness, Matrix):
            # A finite-dimensional matrix over an algebraically closed field
            # always has a Jordan canonical form.
            h1 = True
            h2 = True
            neg_q = False
            
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: T is a linear operator on V",
    "¬Q: T does not have a Jordan canonical form"
]

N_HYP = 2
NEG_Q_INDEX = 2