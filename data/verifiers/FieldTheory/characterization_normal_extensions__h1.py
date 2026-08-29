import sympy
from sympy import Symbol, QQ
from sympy.polys.domains import FractionField, AlgebraicField, RationalField

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x')
QQ_x = QQ.frac_field(x)

def conditions(witness) -> list[bool]:
    """
    Given a witness (e.g., a field extension represented as a tuple (E, F) or just E),
    checks if it is a counterexample to the false conjecture.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            E, F = witness
        else:
            E = witness
            F = None

        is_normal_ext = False
        splits_condition = False

        if E == F and F is not None:
            # Trivial extension is algebraic and normal
            is_normal_ext = True
            splits_condition = True
        elif isinstance(E, FractionField):
            # Transcendental extension (e.g., Q(x)/Q)
            # Not algebraic, hence not normal.
            is_normal_ext = False
            # The algebraic closure of F in F(x) is F.
            # Irreducible polynomials in F[t] with a root in F(x) must have a root in F.
            # Since they are irreducible, they must be linear, hence split completely.
            splits_condition = True
        elif isinstance(E, AlgebraicField):
            # Algebraic extension
            # For algebraic extensions, the splitting condition is equivalent to being normal.
            is_normal_ext = True
            splits_condition = True
        elif isinstance(E, RationalField):
            is_normal_ext = True
            splits_condition = True
        elif isinstance(E, str):
            if "x" in E or "t" in E or "transcendental" in E.lower() or "frac" in E.lower():
                is_normal_ext = False
                splits_condition = True
            else:
                is_normal_ext = True
                splits_condition = True
        else:
            from sympy import Expr
            if isinstance(E, Expr):
                if E.is_algebraic is False:
                    # Transcendental numbers like pi, E
                    is_normal_ext = False
                    splits_condition = True
                elif E.is_algebraic is True:
                    # Algebraic numbers like sqrt(2)
                    is_normal_ext = True
                    splits_condition = True
                elif not E.is_number:
                    # Symbolic expressions like x
                    is_normal_ext = False
                    splits_condition = True
                else:
                    return [False]
            else:
                return [False]

        # The conjecture claims: is_normal_ext <==> splits_condition
        iff_holds = (is_normal_ext == splits_condition)
        
        # The conclusion fails if the iff statement does not hold
        neg_Q = not iff_holds

        return [neg_Q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The equivalence between normal extension and the splitting condition fails (e.g., for transcendental extensions)"
]

N_HYP = 0
NEG_Q_INDEX = 0