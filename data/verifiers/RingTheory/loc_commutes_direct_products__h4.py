import math
from sympy.ntheory import factorint
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_d(m, elements):
    """
    Computes the size of the localization of Z/mZ at the given multiplicatively closed subset.
    The localization is isomorphic to Z/dZ, where d = m / gcd(m, g^\infty) and g is the product of elements.
    """
    if not elements:
        return m
    g = 1
    for e in elements:
        g = (g * e) % m
    
    curr_gcd = math.gcd(m, g)
    while True:
        next_gcd = math.gcd(m, curr_gcd * g)
        if next_gcd == curr_gcd:
            break
        curr_gcd = next_gcd
    return m // curr_gcd

def get_prime_powers(n):
    """Returns the multiset of prime powers in the prime factorization of n."""
    if n <= 1:
        return []
    factors = factorint(n)
    return [p**k for p, k in factors.items()]

def get_all_prime_powers(d_list):
    """Returns the sorted multiset of prime powers for a product of Z/d_i Z rings."""
    res = []
    for d in d_list:
        res.extend(get_prime_powers(d))
    return sorted(res)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    The witness is expected to represent finite commutative rings R_i = Z/m_i Z.
    witness.R_list: list of integers m_i > 0
    witness.S_list: list of lists of integers representing S_i
    witness.S: list of tuples of integers representing S
    """
    res = [False, False, False, False]
    
    # H_1: R_1, ..., R_n are commutative rings
    try:
        R_list = witness.R_list
        if isinstance(R_list, list) and len(R_list) > 0 and all(isinstance(m, int) and m > 0 for m in R_list):
            res[0] = True
    except Exception:
        pass

    # H_2: R is the direct product R_1 \times ... \times R_n
    # We verify this by checking that S is a valid multiplicatively closed subset of the product ring.
    try:
        S = witness.S
        if isinstance(S, list) and all(isinstance(s, tuple) and len(s) == len(witness.R_list) for s in S):
            valid = True
            for s in S:
                for i, m in enumerate(witness.R_list):
                    if not (isinstance(s[i], int) and 0 <= s[i] < m):
                        valid = False
            if valid:
                id_elem = tuple(1 % m for m in witness.R_list)
                if id_elem not in S:
                    valid = False
                if valid:
                    S_set = set(S)
                    for a in S:
                        for b in S:
                            prod = tuple((a[i] * b[i]) % witness.R_list[i] for i in range(len(a)))
                            if prod not in S_set:
                                valid = False
                                break
                        if not valid:
                            break
            if valid:
                res[1] = True
    except Exception:
        pass

    # H_3: S_i is a multiplicatively closed subset of R_i for each i
    try:
        S_list = witness.S_list
        if isinstance(S_list, list) and len(S_list) == len(witness.R_list):
            valid = True
            for i, m in enumerate(witness.R_list):
                Si = S_list[i]
                if not isinstance(Si, list):
                    valid = False
                    break
                if not all(isinstance(x, int) and 0 <= x < m for x in Si):
                    valid = False
                    break
                if 1 % m not in Si:
                    valid = False
                    break
                Si_set = set(Si)
                for a in Si:
                    for b in Si:
                        if (a * b) % m not in Si_set:
                            valid = False
                            break
                    if not valid:
                        break
                if not valid:
                    break
            if valid:
                res[2] = True
    except Exception:
        pass

    # ¬Q: The localized ring S^{-1}R is NOT isomorphic to the direct product S_1^{-1}R_1 \times ... \times S_n^{-1}R_n
    try:
        if res[0] and res[1] and res[2]:
            # Compute the isomorphism class of \prod S_i^{-1}R_i
            c_list = []
            for i, m in enumerate(witness.R_list):
                Si = witness.S_list[i]
                c_list.append(get_d(m, Si))
            
            # Compute the isomorphism class of S^{-1}R
            d_list = []
            for i, m in enumerate(witness.R_list):
                S_proj = [s[i] for s in witness.S]
                d_list.append(get_d(m, S_proj))
            
            # Two finite commutative rings of this form are isomorphic iff their multisets of prime powers match
            pp_c = get_all_prime_powers(c_list)
            pp_d = get_all_prime_powers(d_list)
            
            if pp_c != pp_d:
                res[3] = True
    except Exception:
        pass

    return res

CONDITION_LABELS = [
    "H_1: R_1, ..., R_n are commutative rings",
    "H_2: R is the direct product R_1 \\times ... \\times R_n",
    "H_3: S_i is a multiplicatively closed subset of R_i for each i",
    "¬Q: S^{-1}R is not isomorphic to S_1^{-1}R_1 \\times ... \\times S_n^{-1}R_n"
]

N_HYP = 3
NEG_Q_INDEX = 3