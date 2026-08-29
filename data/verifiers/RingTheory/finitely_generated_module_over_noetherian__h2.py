import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
from sympy.polys.rings import PolyRing
from sympy.polys.domains import Domain

# Top-level setup: named object bindings that the witness expression may reference
Z = ZZ
Q = QQ

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    try:
        # Determine R and M from the witness
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        elif isinstance(witness, PolyRing):
            M = witness
            R = M.domain
        elif isinstance(witness, Domain):
            M = witness
            R = witness
        else:
            R, M = None, None
            
        if R is not None and M is not None:
            # H1: R is a commutative Noetherian ring
            if R in (ZZ, QQ):
                h1 = True
            elif hasattr(R, 'is_Field') and R.is_Field:
                h1 = True
            elif isinstance(R, PolyRing):
                if R.domain in (ZZ, QQ) or (hasattr(R.domain, 'is_Field') and R.domain.is_Field):
                    h1 = True
                
            # H2: M is finitely generated over R (as an algebra)
            if isinstance(M, PolyRing):
                if M.domain == R:
                    h2 = True
                elif isinstance(R, PolyRing) and M.domain == R.domain:
                    if set(R.gens).issubset(set(M.gens)):
                        h2 = True
            elif M == R:
                h2 = True
                
            # neg_Q: M is not a Noetherian module over R
            if isinstance(M, PolyRing):
                if M.domain == R and len(M.gens) > 0:
                    neg_q = True
                elif isinstance(R, PolyRing) and M.domain == R.domain:
                    if set(R.gens).issubset(set(M.gens)) and len(set(M.gens) - set(R.gens)) > 0:
                        neg_q = True
            else:
                neg_q = False
    except Exception:
        pass

    # Fallback for custom objects
    try:
        if not h1 and hasattr(witness, 'is_commutative_Noetherian_ring'):
            h1 = bool(witness.is_commutative_Noetherian_ring())
    except Exception:
        pass

    try:
        if not h2 and hasattr(witness, 'is_finitely_generated_over_R'):
            h2 = bool(witness.is_finitely_generated_over_R())
    except Exception:
        pass

    try:
        if not neg_q and hasattr(witness, 'is_Noetherian_module'):
            neg_q = not bool(witness.is_Noetherian_module())
    except Exception:
        pass

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: M is finitely generated over R",
    "¬Q: M is not a Noetherian module"
]

N_HYP = 2
NEG_Q_INDEX = 2