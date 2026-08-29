import sympy
from sympy import Matrix, eye, zeros
import itertools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should provide the ring R, and the ideals I and J.
    It can be a tuple (R, I, J) or an object with attributes R, I, J.
    """
    try:
        if hasattr(witness, 'R') and hasattr(witness, 'I') and hasattr(witness, 'J'):
            R_set = list(witness.R)
            I_set = list(witness.I)
            J_set = list(witness.J)
        else:
            R_set = list(witness[0])
            I_set = list(witness[1])
            J_set = list(witness[2])
    except Exception:
        return [False, False, False]

    def eq(a, b):
        if a is b: return True
        try:
            if a == b: return True
        except Exception:
            pass
        try:
            if (a - b) == 0: return True
        except Exception:
            pass
        try:
            if (a - b).is_zero_matrix: return True
        except Exception:
            pass
        try:
            if hasattr(a, 'equals') and a.equals(b): return True
        except Exception:
            pass
        return False

    def contains(lst, elem):
        for x in lst:
            if eq(x, elem):
                return True
        return False

    def is_ring(R):
        if not R: return False
        for a in R:
            for b in R:
                if not contains(R, a + b): return False
                if not contains(R, a * b): return False
                if not contains(R, a - b): return False
        return True

    def is_subgroup(S):
        if not S: return False
        for x in S:
            for y in S:
                if not contains(S, x - y): return False
        return True

    def is_left_ideal(S):
        if not is_subgroup(S): return False
        for r in R_set:
            for x in S:
                if not contains(S, r * x): return False
        return True

    def is_right_ideal(S):
        if not is_subgroup(S): return False
        for r in R_set:
            for x in S:
                if not contains(S, x * r): return False
        return True

    # H_1: I and J are ideals of R
    # We accept if they are both left ideals or both right ideals
    try:
        h1 = False
        if is_ring(R_set):
            if is_left_ideal(I_set) and is_left_ideal(J_set):
                h1 = True
            elif is_right_ideal(I_set) and is_right_ideal(J_set):
                h1 = True
    except Exception:
        h1 = False

    # H_2: R is the internal direct sum of I and J as R-modules
    try:
        zero = R_set[0] - R_set[0]
        
        # Check I \cap J = {0}
        intersection = [x for x in I_set if contains(J_set, x)]
        cap_is_zero = all(eq(x, zero) for x in intersection)
        
        # Check I + J = R
        sums = []
        for i in I_set:
            for j in J_set:
                sums.append(i + j)
                
        sum_contains_R = all(contains(sums, r) for r in R_set)
        R_contains_sum = all(contains(R_set, s) for s in sums)
        
        h2 = cap_is_zero and sum_contains_R and R_contains_sum
    except Exception:
        h2 = False

    # ¬Q: The product ideal IJ is not the zero ideal
    try:
        zero = R_set[0] - R_set[0]
        ij_is_zero = True
        for i in I_set:
            for j in J_set:
                if not eq(i * j, zero):
                    ij_is_zero = False
                    break
            if not ij_is_zero:
                break
        neg_q = not ij_is_zero
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: R is the internal direct sum of I and J as R-modules",
    "¬Q: The product ideal IJ is not the zero ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2