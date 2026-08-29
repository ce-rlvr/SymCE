import sympy
import sympy.combinatorics
import sympy.matrices

# Top-level setup for standard objects
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def get_R_S_f(witness):
    if isinstance(witness, tuple) and len(witness) == 3:
        return witness[0], witness[1], witness[2]
    if isinstance(witness, dict):
        return witness['R'], witness['S'], witness['f']
    return witness.R, witness.S, witness.f

def conditions(witness):
    try:
        R, S, f = get_R_S_f(witness)
    except Exception:
        R, S, f = None, None, None

    # H_1: f is a surjective ring homomorphism from R to S
    try:
        h1 = False
        if hasattr(witness, 'is_surjective_homomorphism'):
            h1 = bool(witness.is_surjective_homomorphism() if callable(witness.is_surjective_homomorphism) else witness.is_surjective_homomorphism)
        elif isinstance(witness, dict) and 'is_surjective_homomorphism' in witness:
            val = witness['is_surjective_homomorphism']
            h1 = bool(val() if callable(val) else val)
        elif R is not None and S is not None and f is not None:
            if hasattr(f, 'is_surjective_homomorphism'):
                h1 = bool(f.is_surjective_homomorphism(R, S) if callable(f.is_surjective_homomorphism) else f.is_surjective_homomorphism)
            else:
                R_els = list(R.elements)
                S_els = list(S.elements)
                images = set(f(x) for x in R_els)
                if set(S_els) == images:
                    h1 = True
                    for x in R_els:
                        for y in R_els:
                            if f(R.add(x, y)) != S.add(f(x), f(y)):
                                h1 = False
                                break
                            if f(R.mul(x, y)) != S.mul(f(x), f(y)):
                                h1 = False
                                break
                        if not h1:
                            break
                    if h1 and hasattr(R, 'one') and hasattr(S, 'one'):
                        if f(R.one) != S.one:
                            h1 = False
    except Exception:
        h1 = False

    # H_2: R is an Artinian ring
    try:
        h2 = False
        if hasattr(witness, 'R_is_artinian'):
            h2 = bool(witness.R_is_artinian() if callable(witness.R_is_artinian) else witness.R_is_artinian)
        elif isinstance(witness, dict) and 'R_is_artinian' in witness:
            val = witness['R_is_artinian']
            h2 = bool(val() if callable(val) else val)
        elif R is not None:
            if hasattr(R, 'is_artinian'):
                h2 = bool(R.is_artinian() if callable(R.is_artinian) else R.is_artinian)
            elif isinstance(R, dict) and 'is_artinian' in R:
                val = R['is_artinian']
                h2 = bool(val() if callable(val) else val)
            else:
                if hasattr(R, 'is_Field') and R.is_Field:
                    h2 = True
                elif hasattr(R, 'is_Finite') and R.is_Finite:
                    h2 = True
                elif R == sympy.QQ:
                    h2 = True
    except Exception:
        h2 = False

    # ¬Q: S is not an Artinian ring
    try:
        neg_q = False
        if hasattr(witness, 'S_is_artinian'):
            is_art = bool(witness.S_is_artinian() if callable(witness.S_is_artinian) else witness.S_is_artinian)
            neg_q = not is_art
        elif isinstance(witness, dict) and 'S_is_artinian' in witness:
            val = witness['S_is_artinian']
            is_art = bool(val() if callable(val) else val)
            neg_q = not is_art
        elif S is not None:
            if hasattr(S, 'is_artinian'):
                is_art = bool(S.is_artinian() if callable(S.is_artinian) else S.is_artinian)
                neg_q = not is_art
            elif isinstance(S, dict) and 'is_artinian' in S:
                val = S['is_artinian']
                is_art = bool(val() if callable(val) else val)
                neg_q = not is_art
            else:
                if hasattr(S, 'is_Field') and S.is_Field:
                    neg_q = False
                elif hasattr(S, 'is_Finite') and S.is_Finite:
                    neg_q = False
                elif S == sympy.QQ:
                    neg_q = False
                elif S == sympy.ZZ:
                    neg_q = True
                elif hasattr(S, 'is_Poly') and S.is_Poly:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a surjective ring homomorphism from R to S",
    "H_2: R is an Artinian ring",
    "¬Q: S is not an Artinian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2