import sympy
from sympy import ZZ, QQ, S

# Top-level setup
class Ring:
    def __init__(self, name, is_commutative, is_noetherian, is_integral_domain, krull_dim, is_integrally_closed):
        self.name = name
        self.is_commutative = is_commutative
        self.is_noetherian = is_noetherian
        self.is_integral_domain = is_integral_domain
        self.krull_dim = krull_dim
        self.is_integrally_closed = is_integrally_closed

    def __str__(self):
        return self.name

Z = Ring("Z", True, True, True, 1, True)
Q = Ring("Q", True, True, True, 0, True)
Z_x = Ring("Z[x]", True, True, True, 2, True)
Q_x = Ring("Q[x]", True, True, True, 1, True)
Q_x_y = Ring("Q[x,y]", True, True, True, 2, True)
Z_sqrt_m3 = Ring("Z[sqrt(-3)]", True, True, True, 1, False)
Z_sqrt_m5 = Ring("Z[sqrt(-5)]", True, True, True, 1, True)
k_t2_t3 = Ring("k[t^2, t^3]", True, True, True, 1, False)
Z_i = Ring("Z[i]", True, True, True, 1, True)

def _parse_witness(witness):
    if witness == S.Integers:
        return ZZ
    if witness == S.Rationals:
        return QQ
    if isinstance(witness, str):
        mapping = {
            "Z": Z,
            "Q": Q,
            "Z[x]": Z_x,
            "Q[x]": Q_x,
            "Q[x,y]": Q_x_y,
            "Z[sqrt(-3)]": Z_sqrt_m3,
            "Z[sqrt(-5)]": Z_sqrt_m5,
            "k[t^2, t^3]": k_t2_t3,
            "Z[i]": Z_i
        }
        return mapping.get(witness, witness)
    return witness

def conditions(witness) -> list[bool]:
    witness = _parse_witness(witness)
    
    try:
        if isinstance(witness, Ring):
            h1 = witness.is_commutative and witness.is_noetherian and witness.is_integral_domain
        elif witness in [ZZ, QQ]:
            h1 = True
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            h1 = True
        elif hasattr(witness, 'is_PolyRing') and witness.is_PolyRing:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(witness, Ring):
            h2 = witness.krull_dim <= 1
        elif witness == ZZ:
            h2 = True
        elif witness == QQ:
            h2 = True
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            h2 = True
        elif hasattr(witness, 'is_PolyRing') and witness.is_PolyRing:
            if witness.domain.is_Field and len(witness.gens) == 1:
                h2 = True
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if isinstance(witness, Ring):
            is_dedekind = witness.is_noetherian and witness.is_integral_domain and witness.krull_dim <= 1 and witness.is_integrally_closed
        elif witness in [ZZ, QQ]:
            is_dedekind = True
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            is_dedekind = True
        elif hasattr(witness, 'is_PolyRing') and witness.is_PolyRing:
            if witness.domain.is_Field and len(witness.gens) == 1:
                is_dedekind = True
            else:
                is_dedekind = False
        else:
            is_dedekind = False
        neg_q = not is_dedekind
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian integral domain",
    "H_2: Every non-zero prime ideal of R is a maximal ideal",
    "¬Q: R is not a Dedekind domain"
]

N_HYP = 2
NEG_Q_INDEX = 2