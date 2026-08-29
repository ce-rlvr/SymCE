import math
from functools import reduce
from sympy import Rational, factorint
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard group theory objects for the evaluation namespace
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

def is_cyclic_subgroup_of_Q_star(gens):
    """
    Checks if a finitely generated subgroup of Q* (the multiplicative group of non-zero rationals)
    is cyclic. The input `gens` is a list of non-zero sympy.Rational objects.
    """
    if not gens:
        return True
        
    def get_exponents(r):
        num_factors = factorint(r.p)
        den_factors = factorint(r.q)
        exps = {}
        for p, e in num_factors.items():
            exps[p] = exps.get(p, 0) + e
        for p, e in den_factors.items():
            exps[p] = exps.get(p, 0) - e
        return exps

    all_exps = [get_exponents(abs(g)) for g in gens]
    
    primes = set()
    for exps in all_exps:
        primes.update(exps.keys())
    primes = sorted(list(primes))
    
    vectors = []
    for exps in all_exps:
        vectors.append([exps.get(p, 0) for p in primes])
        
    non_zero_vectors = [v for v in vectors if any(x != 0 for x in v)]
    if not non_zero_vectors:
        # All absolute values are 1. The group is a subgroup of {-1, 1}, which is cyclic.
        return True
        
    v0 = non_zero_vectors[0]
    # Check if all exponent vectors are collinear (rank <= 1)
    for v in non_zero_vectors[1:]:
        for i in range(len(primes)):
            for j in range(i + 1, len(primes)):
                if v0[i] * v[j] - v0[j] * v[i] != 0:
                    return False
                    
    # Find the first non-zero coordinate to compute relative multipliers
    j = next(idx for idx, val in enumerate(v0) if val != 0)
    c_values = [v[j] for v in vectors]
    
    # The generator of the absolute values corresponds to the gcd of the multipliers
    g = abs(reduce(math.gcd, c_values))
    k_values = [c // g for c in c_values]
    
    s_values = [1 if g_val > 0 else -1 for g_val in gens]
    
    # Check if there exists a sign s in {1, -1} such that s_x = s^(k_x) for all x
    s1_works = all(s == 1 for s in s_values)
    s_minus1_works = all(s_values[idx] == (1 if k_values[idx] % 2 == 0 else -1) for idx in range(len(gens)))
    
    return s1_works or s_minus1_works

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a list/tuple/set of numbers representing generators 
    of a subgroup of Q under multiplication.
    """
    # H_1: G is a subgroup of Q
    try:
        if not isinstance(witness, (list, tuple, set)):
            h1 = False
        else:
            gens = [Rational(g) for g in witness]
            # For the multiplicative group interpretation, 0 is not allowed.
            h1 = all(g != 0 for g in gens)
    except Exception:
        h1 = False

    # H_2: G is finitely generated
    try:
        # A finite collection of generators implies it is finitely generated
        h2 = isinstance(witness, (list, tuple, set))
    except Exception:
        h2 = False

    # ¬Q: G is NOT a cyclic group
    try:
        if not isinstance(witness, (list, tuple, set)):
            neg_q = False
        else:
            gens = [Rational(g) for g in witness]
            if not all(g != 0 for g in gens):
                neg_q = False
            else:
                neg_q = not is_cyclic_subgroup_of_Q_star(gens)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a subgroup of Q",
    "H_2: G is finitely generated",
    "¬Q: G is not a cyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2