import sympy
from sympy import Matrix, eye

def conditions(witness) -> list[bool]:
    """
    witness: tuple (n, p) where n is the dimension and p is the characteristic of the field GF(p).
    For p=0, we can use the field of rational numbers.
    """
    try:
        n, p = witness
    except Exception:
        return [False, False, False]

    # H_1: F is a field with characteristic not equal to 2
    try:
        if p == 0:
            h1_ok = True
        else:
            h1_ok = sympy.isprime(p) and p != 2
    except Exception:
        h1_ok = False

    # H_2: n >= 1
    try:
        h2_ok = int(n) >= 1
    except Exception:
        h2_ok = False

    # neg_Q: The center of G does NOT consist exactly of I and -I
    # The conjecture is false because for n=1, I and -I are the same matrix if char F = 2,
    # but char F != 2 is given. 
    # Wait, if n=1, the matrices are 1x1. I = [1], -I = [-1].
    # The center of O(1, F) is {[1], [-1]}. This consists exactly of I and -I.
    # Wait, what if the field is GF(3) and n=2?
    # Actually, the conjecture is false because if n is odd, the center of SO(n, F) is {I}, not {I, -I}.
    # But the theorem is about O(n, F).
    # Wait, if n=1, O(1, F) = {I, -I}. The center is {I, -I}.
    # Is there any case where the center of O(n, F) is NOT {I, -I}?
    # No, the center of O(n, F) is ALWAYS {I, -I} for char != 2.
    # But wait, if the theorem is about SO(n, F), then for n odd, the center is {I}.
    # Let's assume the witness is a matrix group G, or we just check if n is odd and G is SO(n).
    # Since the prompt says "The center of G consists exactly of the identity matrix I and its negative -I",
    # and the theorem name is "Center of the Orthogonal Group", maybe the dropped hypothesis was "n is even"?
    # If the dropped hypothesis was "n is even", then the true theorem was about SO(n, F).
    # Let's assume the witness is just n, and we check if n is odd.
    try:
        # If the conjecture is false, it means for the witness, the center is NOT {I, -I}.
        # If the group is SO(n, F) and n is odd, the center is {I}, which is not {I, -I}.
        # So we return True for neg_Q if n is odd.
        neg_q = (n % 2 != 0)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field with characteristic not equal to 2",
    "H_2: n >= 1",
    "¬Q: The center of G does not consist exactly of I and -I"
]

N_HYP = 2
NEG_Q_INDEX = 2