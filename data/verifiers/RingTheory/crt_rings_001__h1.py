import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup for potential witness references
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: I + J = R",
    "¬Q: R/(I \\cap J) is not isomorphic to R/I \\times R/J"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a counterexample to the false conjecture:
    Hypotheses:
      - I and J are ideals of R.
      - I + J = R.
    Conclusion:
      R/(I \cap J) \cong R/I \times R/J.
    """
    try:
        if isinstance(witness, dict):
            elements = witness['elements']
            add = witness['add']
            mul = witness['mul']
            zero = witness['zero']
            I = witness['I']
            J = witness['J']
        else:
            elements = witness.elements
            add = witness.add
            mul = witness.mul
            zero = witness.zero
            I = witness.I
            J = witness.J
    except Exception:
        return [False, False, False]

    def eq(a, b):
        return a == b

    def contains(lst, val):
        for x in lst:
            if eq(x, val): return True
        return False

    def get_neg(y):
        for z in elements:
            if eq(add(y, z), zero) and eq(add(z, y), zero):
                return z
        raise ValueError("No additive inverse found")

    def is_ideal(ideal):
        if not contains(ideal, zero): return False
        for x in ideal:
            for y in ideal:
                if not contains(ideal, add(x, y)): return False
            neg_x = get_neg(x)
            if not contains(ideal, neg_x): return False
            for r in elements:
                if not contains(ideal, mul(r, x)): return False
                if not contains(ideal, mul(x, r)): return False
        return True

    # H_1: I and J are ideals of R
    try:
        h1 = is_ideal(I) and is_ideal(J)
    except Exception:
        h1 = False

    # H_2: I + J = R
    try:
        I_plus_J = []
        for i in I:
            for j in J:
                s = add(i, j)
                if not contains(I_plus_J, s):
                    I_plus_J.append(s)
        h2 = True
        for r in elements:
            if not contains(I_plus_J, r):
                h2 = False
                break
    except Exception:
        h2 = False

    # neg_Q: R/(I \cap J) is NOT isomorphic to R/I \times R/J
    try:
        I_cap_J = [x for x in I if contains(J, x)]

        def are_in_same_coset(K, x, y):
            neg_y = get_neg(y)
            diff = add(x, neg_y)
            return contains(K, diff)

        def get_quotient(K):
            reps = []
            for x in elements:
                found = False
                for r in reps:
                    if are_in_same_coset(K, x, r):
                        found = True
                        break
                if not found:
                    reps.append(x)
            return reps

        reps_cap = get_quotient(I_cap_J)
        reps_I = get_quotient(I)
        reps_J = get_quotient(J)

        # Structure 1: R/(I \cap J)
        S1 = reps_cap
        def add1(x, y):
            s = add(x, y)
            for r in S1:
                if are_in_same_coset(I_cap_J, s, r): return r
            return s
        def mul1(x, y):
            p = mul(x, y)
            for r in S1:
                if are_in_same_coset(I_cap_J, p, r): return r
            return p

        # Structure 2: R/I \times R/J
        S2 = [(ri, rj) for ri in reps_I for rj in reps_J]
        def add2(x, y):
            s_I = add(x[0], y[0])
            s_J = add(x[1], y[1])
            r_I = s_I
            for r in reps_I:
                if are_in_same_coset(I, s_I, r): r_I = r; break
            r_J = s_J
            for r in reps_J:
                if are_in_same_coset(J, s_J, r): r_J = r; break
            return (r_I, r_J)

        def mul2(x, y):
            p_I = mul(x[0], y[0])
            p_J = mul(x[1], y[1])
            r_I = p_I
            for r in reps_I:
                if are_in_same_coset(I, p_I, r): r_I = r; break
            r_J = p_J
            for r in reps_J:
                if are_in_same_coset(J, p_J, r): r_J = r; break
            return (r_I, r_J)

        # Check isomorphism
        if len(S1) != len(S2):
            neg_q = True
        else:
            n = len(S1)
            S1_list = list(S1)
            S2_list = list(S2)

            add1_t = [[S1_list.index(add1(x, y)) for y in S1_list] for x in S1_list]
            mul1_t = [[S1_list.index(mul1(x, y)) for y in S1_list] for x in S1_list]
            add2_t = [[S2_list.index(add2(x, y)) for y in S2_list] for x in S2_list]
            mul2_t = [[S2_list.index(mul2(x, y)) for y in S2_list] for x in S2_list]

            def solve(mapping, used, i):
                if i == n: return True
                for j in range(n):
                    if not used[j]:
                        ok = True
                        for k in range(i):
                            if add2_t[mapping[k]][j] != mapping[add1_t[k][i]]: ok = False; break
                            if add2_t[j][mapping[k]] != mapping[add1_t[i][k]]: ok = False; break
                            if mul2_t[mapping[k]][j] != mapping[mul1_t[k][i]]: ok = False; break
                            if mul2_t[j][mapping[k]] != mapping[mul1_t[i][k]]: ok = False; break
                        if not ok: continue
                        if add2_t[j][j] != mapping[add1_t[i][i]]: continue
                        if mul2_t[j][j] != mapping[mul1_t[i][i]]: continue

                        mapping[i] = j
                        used[j] = True
                        if solve(mapping, used, i + 1): return True
                        used[j] = False
                return False

            is_iso = solve([0]*n, [False]*n, 0)
            neg_q = not is_iso

    except Exception:
        neg_q = False

    return [h1, h2, neg_q]