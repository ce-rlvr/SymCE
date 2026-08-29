import sympy
from sympy.combinatorics.free_groups import free_group

# Top-level setup
F2, x, y = free_group("x, y")

def conditions(witness) -> list[bool]:
    """
    Given a witness (u, v) as a tuple of elements in F2,
    returns a list of booleans:
      [H_1, H_2, neg_Q]
    """
    try:
        u, v = witness
    except Exception:
        return [False, False, False]

    # H_1: Let x, y be a free basis of F2
    try:
        h1_ok = (x in F2.generators) and (y in F2.generators) and len(F2.generators) == 2
    except Exception:
        h1_ok = False

    # H_2: Let u and v be elements of F2
    try:
        h2_ok = (u in F2) and (v in F2)
    except Exception:
        h2_ok = False

    # neg_Q: The conclusion FAILS.
    try:
        comm_uv = u * v * u**-1 * v**-1
        comm_xy = x * y * x**-1 * y**-1
        comm_xy_inv = y * x * y**-1 * x**-1
        
        def is_conjugate(w1, w2):
            l1 = list(w1.letter_form)
            while len(l1) >= 2 and l1[0] == l1[-1]**-1:
                l1 = l1[1:-1]
                
            l2 = list(w2.letter_form)
            while len(l2) >= 2 and l2[0] == l2[-1]**-1:
                l2 = l2[1:-1]
                
            if len(l1) != len(l2):
                return False
            if len(l1) == 0:
                return True
                
            for i in range(len(l1)):
                if l1 == l2[i:] + l2[:i]:
                    return True
            return False

        rhs_holds = is_conjugate(comm_uv, comm_xy) or is_conjugate(comm_uv, comm_xy_inv)
        
        def generates_F2(a, b):
            words = [a, b]
            for _ in range(1000):  # Bound iterations to prevent infinite loops
                words.sort(key=lambda w: len(w.letter_form))
                w1, w2 = words
                if len(w1.letter_form) == 0:
                    return False
                
                # Try to reduce w2 using w1
                reduced = False
                for op in [w1, w1**-1]:
                    for new_w in [w2 * op, op * w2]:
                        if len(new_w.letter_form) < len(w2.letter_form):
                            words[1] = new_w
                            reduced = True
                            break
                    if reduced:
                        break
                
                if not reduced:
                    # If no length reduction is possible, check if they are exactly the generators
                    # up to inverses and order.
                    gens = set([x, x**-1, y, y**-1])
                    return (words[0] in gens) and (words[1] in gens) and (words[0] != words[1]) and (words[0] != words[1]**-1)
            return False

        # A set {u, v} is a free basis iff it generates F2 and has size 2.
        is_free_basis = generates_F2(u, v) and (u != v)
        lhs_holds = is_free_basis
        
        # The conjecture states LHS iff RHS
        conjecture_holds = (lhs_holds == rhs_holds)
        neg_q_ok = not conjecture_holds

    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Let x, y be a free basis of F2",
    "H_2: Let u and v be elements of F2",
    "¬Q: The equivalence between u, v being a free basis and their commutator being conjugate to the commutator of x, y or its inverse fails"
]

N_HYP = 2
NEG_Q_INDEX = 2