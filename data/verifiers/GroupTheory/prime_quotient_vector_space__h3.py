import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import AbelianGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        A, p = witness
    except Exception:
        return [False, False, False]

    # H_1: A is an abelian group
    try:
        h1 = bool(getattr(A, 'is_abelian', False))
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # ¬Q: A/pA does not possess a natural structure as a vector space over F_p
    try:
        p_is_prime = bool(isprime(p))
    except Exception:
        p_is_prime = False

    try:
        if not p_is_prime:
            # If p is not prime, F_p is not a field, so it cannot be a vector space over F_p
            neg_q = True
        elif h1:
            # If A is abelian and p is prime, A/pA is always an elementary abelian p-group,
            # hence it always possesses a natural structure as a vector space over F_p.
            neg_q = False
        else:
            # If A is not abelian, we check if the set of p-th powers forms a normal subgroup
            # and if the quotient group is abelian.
            if not getattr(A, 'is_finite', True):
                neg_q = False
            else:
                elements = list(A.elements)
                P_set = set(x**p for x in elements)
                
                is_vector_space = True
                P_list = list(P_set)
                
                # Check if P_set is closed under multiplication (i.e., it is a subgroup)
                for x in P_list:
                    for y in P_list:
                        if x * y not in P_set:
                            is_vector_space = False
                            break
                    if not is_vector_space:
                        break
                        
                if is_vector_space:
                    # Check if P_set is a normal subgroup
                    for g in elements:
                        ginv = g**-1
                        for h in P_list:
                            if ginv * h * g not in P_set:
                                is_vector_space = False
                                break
                        if not is_vector_space:
                            break
                            
                if is_vector_space:
                    # Check if the quotient A/P_set is abelian (contains all commutators)
                    for x in A.generators:
                        xinv = x**-1
                        for y in A.generators:
                            yinv = y**-1
                            comm = xinv * yinv * x * y
                            if comm not in P_set:
                                is_vector_space = False
                                break
                        if not is_vector_space:
                            break
                            
                neg_q = not is_vector_space
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an abelian group",
    "H_2: p is a prime number",
    "¬Q: A/pA does not possess a natural structure as a vector space over F_p"
]

N_HYP = 2
NEG_Q_INDEX = 2