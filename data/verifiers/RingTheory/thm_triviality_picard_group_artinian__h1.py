import sympy
from sympy import sqrt, IndexedBase, Function

# Top-level setup: named object bindings that the witness expression may reference.
# We provide standard examples of rings (specifically, rings of integers of number fields)
# that have non-trivial ideal class groups, and hence non-trivial Picard groups.
Z_sqrt_m5 = "Z[sqrt(-5)]"
Z_sqrt_m6 = "Z[sqrt(-6)]"
Z_sqrt_m10 = "Z[sqrt(-10)]"

# Known square-free integers d where the ring of integers of Q(sqrt(d)) has class number > 1.
KNOWN_D = {
    -5, -6, -10, -13, -14, -15, -17, -21, -22, -23, -26, -29, -30, -31, 
    10, 15, 26, 30, 34, 35, 39, 42, 51, 55, 58, 65, 66, 70, 74, 78, 79, 82, 85, 87, 91, 95
}

# String representations of rings with non-trivial Picard groups.
NON_TRIVIAL_PICARD_RINGS = {
    "Z[sqrt(-5)]", "Z[sqrt(-6)]", "Z[sqrt(-10)]", "Z[sqrt(-13)]",
    "Z[sqrt(-14)]", "Z[sqrt(-15)]", "Z[sqrt(-17)]", "Z[sqrt(-21)]",
    "Z[sqrt(-22)]", "Z[sqrt(-23)]", "Z[sqrt(-26)]", "Z[sqrt(-29)]",
    "Z[sqrt(-30)]", "Z[sqrt(-31)]", "Z[sqrt(10)]", "Z[sqrt(15)]",
    "Z[sqrt(26)]", "Z[sqrt(30)]", "Z[sqrt(34)]", "Z[sqrt(35)]",
    "Z[sqrt(39)]", "Z[sqrt(42)]", "Z[sqrt(51)]", "Z[sqrt(55)]",
    "Z[sqrt(58)]", "Z[sqrt(65)]", "Z[sqrt(66)]", "Z[sqrt(70)]",
    "Z[sqrt(74)]", "Z[sqrt(78)]", "Z[sqrt(79)]", "Z[sqrt(82)]",
    "Z[sqrt(85)]", "Z[sqrt(87)]", "Z[sqrt(91)]", "Z[sqrt(95)]",
    "C[x,y]/(y^2-x^3-x)", "Z[x,y]/(x^2+y^2-1)", "R[x,y]/(x^2+y^2-1)"
}

def conditions(witness) -> list[bool]:
    neg_q = False
    try:
        if isinstance(witness, str):
            # Check if the string matches a known ring with non-trivial Picard group
            neg_q = witness.replace(" ", "") in NON_TRIVIAL_PICARD_RINGS
        elif isinstance(witness, tuple) and len(witness) == 2 and witness[0] in ("Z_sqrt", "Q_sqrt"):
            # Check if it's a tuple like ("Z_sqrt", -5)
            neg_q = witness[1] in KNOWN_D
        elif isinstance(witness, int) or (hasattr(witness, 'is_Integer') and witness.is_Integer):
            # Check if the witness is just the integer d
            neg_q = int(witness) in KNOWN_D
        elif hasattr(witness, 'base') and str(witness.base) == 'Z':
            # Check if it's an IndexedBase expression like Z[sqrt(-5)]
            arg = witness.indices[0]
            d = (arg**2)
            if d.is_Integer and int(d) in KNOWN_D:
                neg_q = True
        elif hasattr(witness, 'func') and str(witness.func) == 'Z':
            # Check if it's a Function expression like Z(sqrt(-5))
            arg = witness.args[0]
            d = (arg**2)
            if d.is_Integer and int(d) in KNOWN_D:
                neg_q = True
        elif hasattr(witness, 'ext'):
            # Check if it's a SymPy AlgebraicField
            d = witness.ext**2
            if d.is_Integer and int(d) in KNOWN_D:
                neg_q = True
    except Exception:
        pass
    
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The Picard group Pic(R) is not trivial"
]

N_HYP = 0
NEG_Q_INDEX = 0