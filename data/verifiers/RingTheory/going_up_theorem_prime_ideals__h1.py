import sympy
import sympy.combinatorics
import sympy.matrices
import itertools

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

CONDITION_LABELS = [
    "H_1: R is a subring of S",
    "H_2: S is an integral extension of R",
    "H_3: P1 and P2 are prime ideals of R such that P1 is a subset of P2",
    "H_4: Q1 is a prime ideal of S such that the intersection of Q1 and R is equal to P1",
    "¬Q: There does not exist a prime ideal Q2 of S such that Q1 is a subset of Q2 and the intersection of Q2 and R is equal to P2"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness) -> list[bool]:
    # 1. Try mock object methods (for infinite rings or custom symbolic representations)
    try:
        if hasattr(witness, 'R_is_subring_of_S'):
            h1 = bool(witness.R_is_subring_of_S())
            h2 = bool(witness.S_is_integral_extension_of_R())
            h3 = bool(witness.P1_and_P2_are_prime_ideals_and_P1_subset_P2())
            h4 = bool(witness.Q1_is_prime_ideal_and_intersection_eq_P1())
            neg_q = not bool(witness.exists_Q2())
            return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    # 2. Try dictionary representation
    if isinstance(witness, dict) and 'H1' in witness:
        try:
            return [
                bool(witness.get('H1', False)),
                bool(witness.get('H2', False)),
                bool(witness.get('H3', False)),
                bool(witness.get('H4', False)),
                bool(witness.get('neg_Q', False))
            ]
        except Exception:
            pass

    # 3. Try finite ring evaluation (mathematical verification for finite models)
    try:
        w = witness
        S = list(w.S)
        R = list(w.R)
        P1 = list(w.P1)
        P2 = list(w.P2)
        Q1 = list(w.Q1)
        
        zero = None
        for z in S:
            if all(w.add(x, z) == x for x in S):
                zero = z
                break
                
        def neg(y):
            for z in S:
                if w.add(y, z) == zero:
                    return z
            return None

        def is_subring(subset):
            if not subset: return False
            if zero not in subset: return False
            for x in subset:
                for y in subset:
                    ny = neg(y)
                    if ny is None or w.add(x, ny) not in subset: return False
                    if w.mul(x, y) not in subset: return False
            return True

        def is_ideal(ring_set, ideal_set):
            if not set(ideal_set).issubset(set(ring_set)): return False
            for x in ideal_set:
                for y in ideal_set:
                    ny = neg(y)
                    if ny is None or w.add(x, ny) not in ideal_set: return False
            for r in ring_set:
                for x in ideal_set:
                    if w.mul(r, x) not in ideal_set: return False
                    if w.mul(x, r) not in ideal_set: return False
            return True

        def is_prime_ideal(ring_set, ideal_set):
            if not is_ideal(ring_set, ideal_set): return False
            if set(ideal_set) == set(ring_set): return False
            for a in ring_set:
                for b in ring_set:
                    aRb_in_P = True
                    for r in ring_set:
                        if w.mul(a, w.mul(r, b)) not in ideal_set:
                            aRb_in_P = False
                            break
                    if aRb_in_P:
                        if a not in ideal_set and b not in ideal_set:
                            return False
            return True

        h1 = set(R).issubset(set(S)) and is_subring(R)
        
        id_S = None
        for e in S:
            if all(w.mul(x, e) == x and w.mul(e, x) == x for x in S):
                id_S = e
                break
        
        # For finite rings, elements are integral. We just check shared identity if it exists.
        h2 = True
        if id_S is not None and id_S not in R:
            h2 = False
            
        h3 = is_prime_ideal(R, P1) and is_prime_ideal(R, P2) and set(P1).issubset(set(P2))
        h4 = is_prime_ideal(S, Q1) and set(Q1).intersection(set(R)) == set(P1)
        
        prime_ideals = []
        if hasattr(w, 'all_prime_ideals_of_S'):
            prime_ideals = w.all_prime_ideals_of_S
        else:
            for i in range(1, len(S)):
                for subset in itertools.combinations(S, i):
                    if is_prime_ideal(S, subset):
                        prime_ideals.append(subset)
                        
        exists_Q2 = False
        for Q2 in prime_ideals:
            if set(Q1).issubset(set(Q2)) and set(Q2).intersection(set(R)) == set(P2):
                exists_Q2 = True
                break
        neg_q = not exists_Q2
        
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    return [False, False, False, False, False]