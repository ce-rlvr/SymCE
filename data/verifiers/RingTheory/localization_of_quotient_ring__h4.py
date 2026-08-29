import math
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness objects
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
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: I is an ideal of R",
    "¬Q: The localized quotient ring (S^{-1}R)/(S^{-1}I) is NOT isomorphic to (S')^{-1}(R/I)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        # Extract witness components
        if isinstance(witness, dict):
            R_val = witness.get('R', witness.get('n', None))
            S = witness.get('S', [])
            I = witness.get('I', [])
            S_prime = witness.get('S_prime', witness.get('S_prime', []))
        elif isinstance(witness, tuple) and len(witness) == 4:
            R_val, S, I, S_prime = witness
        else:
            R_val = getattr(witness, 'R', getattr(witness, 'n', None))
            S = getattr(witness, 'S', [])
            I = getattr(witness, 'I', [])
            S_prime = getattr(witness, 'S_prime', [])

        # Determine n (modulus for Z/nZ, 0 means Z)
        if R_val in ('Z', 'ZZ') or str(R_val) in ('ZZ', 'Integers', 'Z'):
            n = 0
        elif isinstance(R_val, int):
            n = R_val
        else:
            n = 0

        if n < 0:
            n = abs(n)

        # Parse S
        if isinstance(S, int):
            S_list = [S]
        else:
            S_list = list(S)
        S_list = [int(x) for x in S_list]

        # Parse S_prime
        if isinstance(S_prime, int):
            S_prime_list = [S_prime]
        else:
            S_prime_list = list(S_prime)
        S_prime_list = [int(x) for x in S_prime_list]

        # H1: R is a commutative ring
        # We only support Z and Z/nZ, which are always commutative rings.
        h1 = True

        # H2: S is a multiplicatively closed subset of R
        h2 = False
        if S_list:
            if n > 0:
                S_mod = set(x % n for x in S_list)
                if 1 % n in S_mod:
                    closed = True
                    for a in S_mod:
                        for b in S_mod:
                            if (a * b) % n not in S_mod:
                                closed = False
                                break
                        if not closed: break
                    h2 = closed
            else:
                S_set = set(S_list)
                if 1 in S_set:
                    closed = True
                    for a in S_set:
                        for b in S_set:
                            if a * b not in S_set:
                                closed = False
                                break
                        if not closed: break
                    h2 = closed

        # H3: I is an ideal of R
        h3 = False
        if isinstance(I, int):
            h3 = True
        elif hasattr(I, 'gens'):
            h3 = True
        elif isinstance(I, (list, set, tuple)):
            I_list = [int(x) for x in list(I)]
            if I_list:
                if n > 0:
                    I_mod = set(x % n for x in I_list)
                    closed_add = True
                    for a in I_mod:
                        for b in I_mod:
                            if (a + b) % n not in I_mod:
                                closed_add = False
                                break
                        if not closed_add: break
                    # In Z/nZ, an additive subgroup is an ideal
                    h3 = closed_add
                else:
                    h3 = (set(I_list) == {0})

        # Compute m (generator of the ideal I)
        if isinstance(I, int):
            m = I
        elif hasattr(I, 'gens'):
            I_gens = [int(x) for x in I.gens]
            if not I_gens:
                m = 0
            else:
                m = I_gens[0]
                for x in I_gens[1:]:
                    m = math.gcd(m, x)
        else:
            I_list = [int(x) for x in list(I)]
            if not I_list:
                m = 0
            else:
                m = I_list[0]
                for x in I_list[1:]:
                    m = math.gcd(m, x)
        
        if n > 0:
            m = math.gcd(m, n)
        else:
            m = abs(m)

        # neg_Q: The localized quotient ring (S^{-1}R)/(S^{-1}I) is NOT isomorphic to (S')^{-1}(R/I)
        
        # Compute A, where Ring 1 is isomorphic to Z/AZ
        if n > 0:
            K_elements = []
            for x in range(n):
                if any((s * x) % n == 0 for s in S_list):
                    K_elements.append(x)
            k = n
            for x in K_elements:
                k = math.gcd(k, x)
        else:
            if 0 in S_list:
                k = 1
            else:
                k = 0
        A = math.gcd(m, k)

        # Compute B, where Ring 2 is isomorphic to Z/BZ
        if m > 0:
            closure = set(x % m for x in S_prime_list)
            closure.add(1 % m)
            queue = list(closure)
            while queue:
                a = queue.pop()
                new_elements = []
                for b in closure:
                    prod = (a * b) % m
                    if prod not in closure:
                        new_elements.append(prod)
                for x in new_elements:
                    closure.add(x)
                    queue.append(x)
            
            K_prime_elements = []
            for y in range(m):
                if any((sp * y) % m == 0 for sp in closure):
                    K_prime_elements.append(y)
            k_prime = m
            for y in K_prime_elements:
                k_prime = math.gcd(k_prime, y)
            B = k_prime
        else:
            if 0 in S_prime_list:
                B = 1
            else:
                B = 0

        # The rings Z/AZ and Z/BZ are isomorphic if and only if A == B
        neg_q = (A != B)

        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]