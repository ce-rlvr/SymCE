import sympy
from sympy import symbols, QQ, ZZ
import math

# Top-level setup for RingTheory domain
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    Returns [H_1_ok, H_2_ok, neg_Q_ok].
    """
    try:
        # 1. Check if witness is a custom object with attributes/methods
        if hasattr(witness, 'is_ring_with_identity'):
            h1 = witness.is_ring_with_identity() if callable(witness.is_ring_with_identity) else witness.is_ring_with_identity
            h2 = witness.phi_is_surjective() if callable(witness.phi_is_surjective) else witness.phi_is_surjective
            q = witness.are_pairwise_comaximal() if callable(witness.are_pairwise_comaximal) else witness.are_pairwise_comaximal
            return [bool(h1), bool(h2), not bool(q)]
    except Exception:
        pass

    try:
        # 2. Check if witness is a dictionary
        if isinstance(witness, dict) and 'is_ring_with_identity' in witness:
            h1 = bool(witness.get('is_ring_with_identity', False))
            h2 = bool(witness.get('phi_is_surjective', False))
            q = bool(witness.get('are_pairwise_comaximal', True))
            return [h1, h2, not q]
    except Exception:
        pass

    try:
        # 3. Check if witness is a list of integers (representing ideals in ZZ)
        if isinstance(witness, (list, tuple)) and all(isinstance(val, int) for val in witness):
            h1 = True  # ZZ is a ring with identity
            n = len(witness)
            surj = True
            for i in range(n):
                for j in range(i + 1, n):
                    if math.gcd(witness[i], witness[j]) != 1:
                        surj = False
                        break
            h2 = surj
            q = surj  # In ZZ, pairwise comaximal is equivalent to pairwise coprime
            return [h1, h2, not q]
    except Exception:
        pass

    try:
        # 4. Check if witness is a list of sympy expressions (ideals in QQ[x])
        if isinstance(witness, (list, tuple)) and all(isinstance(val, sympy.Expr) for val in witness):
            h1 = True  # QQ[x] is a ring with identity
            n = len(witness)
            surj = True
            for i in range(n):
                for j in range(i + 1, n):
                    g = sympy.gcd(witness[i], witness[j])
                    if not g.is_number:
                        surj = False
                        break
            h2 = surj
            q = surj
            return [h1, h2, not q]
    except Exception:
        pass

    try:
        # 5. Check if witness is a tuple (R, I_list)
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I_list = witness
            if R == ZZ and isinstance(I_list, (list, tuple)):
                h1 = True
                n = len(I_list)
                surj = True
                for i in range(n):
                    for j in range(i + 1, n):
                        if math.gcd(I_list[i], I_list[j]) != 1:
                            surj = False
                            break
                h2 = surj
                q = surj
                return [h1, h2, not q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: The canonical ring homomorphism phi is surjective",
    "¬Q: The ideals I_1, ..., I_n are not pairwise comaximal"
]

N_HYP = 2
NEG_Q_INDEX = 2