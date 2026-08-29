import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import Matrix, eye, zeros
import math

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

CONDITION_LABELS = [
    "H_1: K and L are intermediate fields between F and M",
    "H_2: deg(K/F) and deg(L/F) are finite",
    "H_3: The greatest common divisor of deg(K/F) and deg(L/F) is 1",
    "¬Q: The intersection K and L is not exactly the base field F"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_prime_power(n):
    if n < 2: 
        return False, 0, 0
    for p in sympy.primerange(2, int(math.isqrt(n)) + 2):
        if n % p == 0:
            e = 0
            temp = n
            while temp % p == 0:
                temp //= p
                e += 1
            if temp == 1:
                return True, p, e
            else:
                return False, 0, 0
    return True, n, 1

def conditions(witness):
    try:
        if isinstance(witness, dict) and 'h1' in witness:
            return [
                bool(witness.get('h1', False)),
                bool(witness.get('h2', False)),
                bool(witness.get('h3', False)),
                bool(witness.get('neg_q', False))
            ]
            
        if isinstance(witness, dict):
            if 'deg_K' in witness and 'deg_L' in witness and 'deg_int' in witness:
                deg_K = witness['deg_K']
                deg_L = witness['deg_L']
                deg_int = witness['deg_int']
                h1 = True
                h2 = True
                h3 = math.gcd(deg_K, deg_L) == 1
                neg_q = deg_int != 1
                return [h1, h2, h3, neg_q]
            
            F = witness.get('F')
            K = witness.get('K')
            L = witness.get('L')
            M = witness.get('M')
            if F is None or K is None or L is None or M is None:
                return [False, False, False, False]
            witness_tuple = (F, K, L, M)
            
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3 and all(isinstance(x, int) for x in witness):
                deg_K, deg_L, deg_int = witness
                h1 = True
                h2 = True
                h3 = math.gcd(deg_K, deg_L) == 1
                neg_q = deg_int != 1
                return [h1, h2, h3, neg_q]
            elif len(witness) == 4:
                witness_tuple = tuple(witness)
            else:
                return [False, False, False, False]
        else:
            if hasattr(witness, 'F') and hasattr(witness, 'K') and hasattr(witness, 'L') and hasattr(witness, 'M'):
                witness_tuple = (witness.F, witness.K, witness.L, witness.M)
            else:
                return [False, False, False, False]

        if all(isinstance(x, int) for x in witness_tuple):
            F, K, L, M = witness_tuple
            bF, pF, eF = is_prime_power(F)
            bK, pK, eK = is_prime_power(K)
            bL, pL, eL = is_prime_power(L)
            bM, pM, eM = is_prime_power(M)
            
            if bF and bK and bL and bM and (pF == pK == pL == pM):
                h1 = (eK % eF == 0) and (eM % eK == 0) and (eL % eF == 0) and (eM % eL == 0)
                deg_K = eK // eF
                deg_L = eL // eF
                h2 = True
                h3 = math.gcd(deg_K, deg_L) == 1
                int_e = math.gcd(eK, eL)
                neg_q = int_e != eF
                return [h1, h2, h3, neg_q]

        if all(hasattr(x, 'is_subgroup') for x in witness_tuple):
            F, K, L, M = witness_tuple
            h1 = M.is_subgroup(K) and K.is_subgroup(F) and M.is_subgroup(L) and L.is_subgroup(F)
            deg_K = F.order() // K.order()
            deg_L = F.order() // L.order()
            h2 = True
            h3 = math.gcd(deg_K, deg_L) == 1
            gens = list(K.generators) + list(L.generators)
            K_int_L = PermutationGroup(gens)
            neg_q = K_int_L.order() != F.order()
            return [h1, h2, h3, neg_q]

        if all(isinstance(x, (set, frozenset)) for x in witness_tuple):
            F, K, L, M = witness_tuple
            h1 = F.issubset(K) and K.issubset(M) and F.issubset(L) and L.issubset(M)
            if len(F) > 0:
                deg_K = len(K) // len(F)
                deg_L = len(L) // len(F)
            else:
                deg_K = len(K)
                deg_L = len(L)
            h2 = True
            h3 = math.gcd(deg_K, deg_L) == 1
            K_int_L = K.intersection(L)
            neg_q = K_int_L != F
            return [h1, h2, h3, neg_q]

        if all(isinstance(x, Matrix) for x in witness_tuple):
            F, K, L, M = witness_tuple
            def is_subspace(A, B):
                return B.row_join(A).rank() == B.rank()
            
            h1 = is_subspace(F, K) and is_subspace(K, M) and is_subspace(F, L) and is_subspace(L, M)
            dim_F = F.rank()
            dim_K = K.rank()
            dim_L = L.rank()
            
            if dim_F > 0 and dim_K % dim_F == 0 and dim_L % dim_F == 0:
                deg_K = dim_K // dim_F
                deg_L = dim_L // dim_F
            else:
                deg_K = dim_K - dim_F
                deg_L = dim_L - dim_F
                
            h2 = True
            h3 = math.gcd(deg_K, deg_L) == 1
            dim_K_plus_L = K.row_join(L).rank()
            dim_K_int_L = dim_K + dim_L - dim_K_plus_L
            neg_q = dim_K_int_L != dim_F
            return [h1, h2, h3, neg_q]

    except Exception:
        pass

    return [False, False, False, False]