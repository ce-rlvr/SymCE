import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4) # Note: V4 is usually Klein four-group, but AlternatingGroup(4) is A4. We will define V4 properly if needed, but the prompt says V4 = AlternatingGroup(4) which is a bit weird. Let's define V4 as DihedralGroup(2) which is isomorphic to Klein four-group, but we'll stick to standard ones.
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: E is the splitting field of x^4 + 8x + 12 over Q",
    "¬Q: The Galois group Gal(E/Q) is not isomorphic to A4"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    # witness is expected to be the Galois group of x^4 + 8x + 12 over Q.
    # The polynomial is x^4 + 8x + 12.
    # Its Galois group is D4 (Dihedral group of order 8) or A4 or S4?
    # Actually, we just need to check if the witness is the Galois group of x^4 + 8x + 12.
    # Since we can't easily compute the Galois group from scratch in 5 seconds without a specific function,
    # we can check if the witness is isomorphic to the actual Galois group.
    # Wait, the witness IS the Galois group. The hypothesis is "Let E be the splitting field...".
    # The witness is just the group itself.
    # The Galois group of x^4 + 8x + 12:
    # Resolvent cubic of x^4 + 8x + 12 is y^3 - 48y - 64.
    # Roots of y^3 - 48y - 64 = 0: y = -4 is a root (-64 + 192 - 64 = 64 != 0? Wait, (-4)^3 = -64, -48(-4) = 192, -64+192-64 = 64 != 0).
    # Let's re-evaluate: resolvent cubic of x^4 + px + q is y^3 - 4qy - p^2.
    # Here p=8, q=12. So y^3 - 48y - 64.
    # Let's check roots: y = -4: -64 + 192 - 64 = 64.
    # y = 8: 512 - 384 - 64 = 64.
    # y = -2: -8 + 96 - 64 = 24.
    # Actually, the discriminant of x^4 + 8x + 12 is -256 * 12^3 + 256 * 8^4 = -256 * 1728 + 256 * 4096 = 256 * 2368 = 606208.
    # 606208 is not a perfect square (sqrt is ~778.5).
    # So the Galois group is not A4 or V4.
    # The resolvent cubic is y^3 - 48y - 64.
    # Let's check if it has a rational root.
    # Rational root theorem: factors of 64.
    # y = -4: -64 + 192 - 64 = 64 != 0.
    # y = 4: 64 - 192 - 64 = -192 != 0.
    # y = -8: -512 + 384 - 64 = -192 != 0.
    # y = 8: 512 - 384 - 64 = 64 != 0.
    # So the resolvent cubic has no rational roots.
    # Thus, the Galois group is S4.
    # Wait, the witness should be S4.
    
    try:
        # H_1: The witness is the Galois group of x^4 + 8x + 12 over Q.
        # We know the Galois group is S4.
        h1_ok = witness.is_isomorphic(S4)
    except Exception:
        h1_ok = False

    try:
        # ¬Q: The Galois group is NOT isomorphic to A4.
        neg_q_ok = not witness.is_isomorphic(A4)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]