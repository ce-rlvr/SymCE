import sympy
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide:
      - R: a list of elements representing the ring
      - ideals: a list of lists, each representing an ideal I_k
      - x: a list of elements x_k in R
    """
    try:
        if isinstance(witness, dict):
            R = witness['R']
            ideals = witness['ideals']
            x_list = witness['x']
        else:
            R = witness.R
            ideals = witness.ideals
            x_list = witness.x
    except Exception:
        return [False, False, False, False]

    def contains(lst, item):
        return any(x == item for x in lst)

    # H1: R is a ring with identity
    try:
        h1 = False
        closed_add = True
        for a in R:
            for b in R:
                if not contains(R, a + b):
                    closed_add = False; break
            if not closed_add: break
            
        closed_mul = True
        if closed_add:
            for a in R:
                for b in R:
                    if not contains(R, a * b):
                        closed_mul = False; break
                if not closed_mul: break

        if closed_add and closed_mul:
            comm_add = True
            for a in R:
                for b in R:
                    if a + b != b + a:
                        comm_add = False; break
                if not comm_add: break

            assoc_add = True
            if comm_add:
                for a in R:
                    for b in R:
                        ab = a + b
                        for c in R:
                            if ab + c != a + (b + c):
                                assoc_add = False; break
                        if not assoc_add: break
                    if not assoc_add: break

            assoc_mul = True
            if assoc_add:
                for a in R:
                    for b in R:
                        ab = a * b
                        for c in R:
                            if ab * c != a * (b * c):
                                assoc_mul = False; break
                        if not assoc_mul: break
                    if not assoc_mul: break

            dist_left = True
            if assoc_mul:
                for a in R:
                    for b in R:
                        ab = a * b
                        for c in R:
                            if a * (b + c) != ab + a * c:
                                dist_left = False; break
                        if not dist_left: break
                    if not dist_left: break

            dist_right = True
            if dist_left:
                for a in R:
                    for b in R:
                        ab = a + b
                        for c in R:
                            if ab * c != a * c + b * c:
                                dist_right = False; break
                        if not dist_right: break
                    if not dist_right: break
            
            if comm_add and assoc_add and assoc_mul and dist_left and dist_right:
                zero = None
                for z in R:
                    is_z = True
                    for a in R:
                        if a + z != a or z + a != a:
                            is_z = False; break
                    if is_z:
                        zero = z
                        break
                
                one = None
                for e in R:
                    is_e = True
                    for a in R:
                        if a * e != a or e * a != a:
                            is_e = False; break
                    if is_e:
                        one = e
                        break
                
                if zero is not None and one is not None:
                    has_inv = True
                    for a in R:
                        inv_found = False
                        for b in R:
                            if a + b == zero:
                                inv_found = True; break
                        if not inv_found:
                            has_inv = False; break
                    if has_inv:
                        h1 = True
    except Exception:
        h1 = False

    # H2: I_1, ..., I_n are ideals of R
    try:
        h2 = True
        if not ideals:
            h2 = False
        else:
            # Find zero independently to evaluate H2 even if H1 failed
            zero = None
            for z in R:
                is_z = True
                for a in R:
                    try:
                        if a + z != a or z + a != a:
                            is_z = False; break
                    except Exception:
                        is_z = False; break
                if is_z:
                    zero = z
                    break

            for I in ideals:
                if not I:
                    h2 = False; break
                
                is_sub = True
                for a in I:
                    if not contains(R, a):
                        is_sub = False; break
                if not is_sub:
                    h2 = False; break
                
                if zero is None or not contains(I, zero):
                    h2 = False; break
                
                closed_add_I = True
                for a in I:
                    for b in I:
                        if not contains(I, a + b):
                            closed_add_I = False; break
                    if not closed_add_I: break
                if not closed_add_I:
                    h2 = False; break
                
                has_inv_I = True
                for a in I:
                    inv_found = False
                    for b in I:
                        if a + b == zero:
                            inv_found = True; break
                    if not inv_found:
                        has_inv_I = False; break
                if not has_inv_I:
                    h2 = False; break
                
                is_left = True
                for r in R:
                    for a in I:
                        if not contains(I, r * a):
                            is_left = False; break
                    if not is_left: break
                
                is_right = True
                for r in R:
                    for a in I:
                        if not contains(I, a * r):
                            is_right = False; break
                    if not is_right: break
                
                # An ideal must be at least a left ideal or a right ideal
                if not (is_left or is_right):
                    h2 = False; break
    except Exception:
        h2 = False

    # H3: I_i + I_j = R for all i != j
    try:
        h3 = True
        n = len(ideals)
        for i in range(n):
            for j in range(i + 1, n):
                sum_ideal = []
                for a in ideals[i]:
                    for b in ideals[j]:
                        s = a + b
                        if not contains(sum_ideal, s):
                            sum_ideal.append(s)
                
                covers_R = True
                for r in R:
                    if not contains(sum_ideal, r):
                        covers_R = False; break
                if not covers_R:
                    h3 = False; break
            if not h3:
                break
    except Exception:
        h3 = False

    # Negated Conclusion: NO element x in R satisfies x = x_k mod I_k for all k
    try:
        neg_q = True
        if len(x_list) != len(ideals):
            neg_q = False
        else:
            all_in_R = True
            for xk in x_list:
                if not contains(R, xk):
                    all_in_R = False; break
            if not all_in_R:
                neg_q = False
            else:
                for x in R:
                    is_sol = True
                    for k in range(len(ideals)):
                        match_found = False
                        for i_k in ideals[k]:
                            if x_list[k] + i_k == x:
                                match_found = True
                                break
                        if not match_found:
                            is_sol = False
                            break
                    if is_sol:
                        neg_q = False
                        break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: I_1, ..., I_n are ideals of R",
    "H_3: I_i + I_j = R for all i != j",
    "¬Q: There is no element x in R such that x = x_k mod I_k for all k"
]

N_HYP = 3
NEG_Q_INDEX = 3