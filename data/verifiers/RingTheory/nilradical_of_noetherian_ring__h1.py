import itertools
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# A standard counterexample: the ring of 2x2 matrices over GF(2)
M2_Z2_elements = [Matrix(2, 2, entries) for entries in itertools.product([0, 1], repeat=4)]
M2_Z2 = (M2_Z2_elements, 2)

# The nilradical (set of all nilpotent elements) of M2(Z2)
N_M2_Z2 = []
for A in M2_Z2_elements:
    if ((A * A) % 2).is_zero_matrix:
        N_M2_Z2.append(A)

def eq(A, B, mod):
    if mod > 0:
        return ((A - B) % mod).is_zero_matrix
    else:
        return (A - B).is_zero_matrix

def mat_to_tuple(M, mod):
    if mod > 0:
        return tuple(x % mod for x in M)
    return tuple(M)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    Hypotheses:
      - R is a Noetherian ring
      - N is the nilradical of R
    Conclusion:
      - There exists a positive integer k such that N^k = {0}
    """
    # Parse witness
    try:
        if witness == "M2_Z2":
            witness = (M2_Z2, N_M2_Z2)
        elif isinstance(witness, tuple) and len(witness) == 2:
            if witness[0] == "M2_Z2":
                witness = (M2_Z2, N_M2_Z2)
                
        if isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[1], list):
                # witness is (R, N)
                R, N_elements = witness
                if isinstance(R, tuple) and len(R) == 2:
                    R_elements, mod = R
                else:
                    R_elements = R
                    mod = 0
            elif isinstance(witness[1], int):
                # witness is just R = (R_elements, mod)
                R_elements, mod = witness
                N_elements = None
            else:
                return [False, False, False]
        elif isinstance(witness, list):
            # witness is just R = R_elements
            R_elements = witness
            mod = 0
            N_elements = None
        else:
            return [False, False, False]
            
        if not isinstance(R_elements, list):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a Noetherian ring
    # We verify this by checking if R is a finite ring (which implies Noetherian)
    h1_ok = False
    try:
        n = len(R_elements)
        if n > 0:
            zero = None
            for A in R_elements:
                if all(eq(A + B, B, mod) for B in R_elements):
                    zero = A
                    break
            if zero is not None:
                elements_set = set(mat_to_tuple(M, mod) for M in R_elements)
                if len(elements_set) == n:
                    is_ring = True
                    for A in R_elements:
                        has_inv = False
                        for B in R_elements:
                            if mat_to_tuple(A + B, mod) == mat_to_tuple(zero, mod):
                                has_inv = True
                                break
                        if not has_inv:
                            is_ring = False
                            break
                        for B in R_elements:
                            if mat_to_tuple(A + B, mod) not in elements_set:
                                is_ring = False
                                break
                            prod = A * B
                            if mod > 0:
                                prod = prod % mod
                            if mat_to_tuple(prod, mod) not in elements_set:
                                is_ring = False
                                break
                        if not is_ring:
                            break
                    
                    # Check for multiplicative identity
                    if is_ring:
                        has_id = False
                        for E in R_elements:
                            is_id = True
                            for A in R_elements:
                                prod1 = E * A
                                prod2 = A * E
                                if mod > 0:
                                    prod1 = prod1 % mod
                                    prod2 = prod2 % mod
                                if mat_to_tuple(prod1, mod) != mat_to_tuple(A, mod) or \
                                   mat_to_tuple(prod2, mod) != mat_to_tuple(A, mod):
                                    is_id = False
                                    break
                            if is_id:
                                has_id = True
                                break
                        if not has_id:
                            is_ring = False
                            
                    h1_ok = is_ring
    except Exception:
        h1_ok = False

    # H_2: N is the nilradical of R
    # In this context, nilradical means the set of all nilpotent elements
    h2_ok = False
    try:
        if h1_ok:
            expected_N = []
            for A in R_elements:
                curr = A
                is_nil = False
                for _ in range(n):
                    if mat_to_tuple(curr, mod) == mat_to_tuple(zero, mod):
                        is_nil = True
                        break
                    curr = curr * A
                    if mod > 0:
                        curr = curr % mod
                if is_nil:
                    expected_N.append(A)
            
            if N_elements is None:
                N_elements = expected_N
                h2_ok = True
            else:
                set_N = set(mat_to_tuple(M, mod) for M in N_elements)
                set_expected = set(mat_to_tuple(M, mod) for M in expected_N)
                h2_ok = (set_N == set_expected)
    except Exception:
        h2_ok = False

    # neg_Q: N^k is never {0} for any positive integer k
    neg_q_ok = False
    try:
        if h1_ok and h2_ok:
            zero_tuple = mat_to_tuple(zero, mod)
            current_set = set(mat_to_tuple(M, mod) for M in N_elements)
            seen = []
            
            N_tuples = list(current_set)
            tuple_to_mat = {mat_to_tuple(M, mod): M for M in R_elements}
            
            mul_table = {}
            def get_mul(a_tup, b_tup):
                if (a_tup, b_tup) not in mul_table:
                    a_mat = tuple_to_mat[a_tup]
                    b_mat = tuple_to_mat[b_tup]
                    prod = a_mat * b_mat
                    if mod > 0:
                        prod = prod % mod
                    mul_table[(a_tup, b_tup)] = mat_to_tuple(prod, mod)
                return mul_table[(a_tup, b_tup)]
            
            step = 0
            while step < 1000:
                if not current_set:
                    break
                if current_set == {zero_tuple}:
                    neg_q_ok = False
                    break
                if current_set in seen:
                    neg_q_ok = True
                    break
                seen.append(current_set)
                
                next_set = set()
                for a_tup in current_set:
                    for b_tup in N_tuples:
                        next_set.add(get_mul(a_tup, b_tup))
                current_set = next_set
                step += 1
            else:
                # If it didn't stabilize to {0} in 1000 steps, it never will
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "H_2: N is the nilradical of R",
    "¬Q: N^k is never {0} for any positive integer k"
]

N_HYP = 2
NEG_Q_INDEX = 2