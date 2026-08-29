import sympy
from sympy import ZZ, QQ
import math

# Standard finite rings represented by their modulus
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a tuple (R, P) where:
      - R is either sympy.ZZ or an integer n > 1 representing Z/nZ.
      - P is a list of generators (for ZZ) or a list of elements (for Z/nZ).
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
            
        R_obj, P_obj = witness
        
        # Case 1: R is the ring of integers ZZ
        if R_obj == ZZ or str(R_obj) == "ZZ":
            h1 = True
            h2 = True
            
            if isinstance(P_obj, int):
                k = abs(P_obj)
            elif isinstance(P_obj, (list, set, tuple)):
                if len(P_obj) == 0:
                    k = 0
                else:
                    if not all(isinstance(x, int) for x in P_obj):
                        return [False, False, False]
                    k = abs(P_obj[0])
                    for x in P_obj[1:]:
                        k = math.gcd(k, abs(x))
            else:
                return [False, False, False]
                
            if k == 0:
                # P = {0} is prime, S^{-1}ZZ = QQ is local with max ideal {0}
                neg_q = False
            elif k == 1:
                # P = ZZ, S is empty, S^{-1}ZZ = ZZ is not local
                neg_q = True
            else:
                is_prime = sympy.isprime(k)
                if is_prime:
                    # P is a prime ideal, S^{-1}ZZ is local
                    neg_q = False
                else:
                    # P is not prime, S is not multiplicatively closed.
                    # The multiplicative closure of S contains k, so k becomes a unit.
                    # Thus S^{-1}P is the whole ring, not a proper maximal ideal.
                    neg_q = True
                    
            return [h1, h2, neg_q]
            
        # Case 2: R is the finite ring Z/nZ
        elif isinstance(R_obj, int) and R_obj > 1:
            n = R_obj
            if isinstance(P_obj, int):
                P = {P_obj}
            else:
                try:
                    P = set(P_obj)
                except TypeError:
                    return [False, False, False]
                    
            if not all(isinstance(x, int) and 0 <= x < n for x in P):
                return [False, False, False]
                
            h1 = True
            h2 = True
            
            R = list(range(n))
            S = [x for x in R if x not in P]
            
            # Compute the multiplicative closure of S
            M = set(S)
            M.add(1)
            while True:
                new_M = set(M)
                for x in M:
                    for y in S:
                        new_M.add((x * y) % n)
                if len(new_M) == len(M):
                    break
                M = new_M
            M = list(M)
            
            # Precompute annihilators for fast equivalence checking
            annihilators = [False] * n
            for x in range(n):
                for u in M:
                    if (u * x) % n == 0:
                        annihilators[x] = True
                        break
                        
            def equiv(e1, e2):
                r1, s1 = e1
                r2, s2 = e2
                diff = (r1 * s2 - r2 * s1) % n
                return annihilators[diff]
                
            # Elements of S^{-1}R are equivalence classes of R x M
            elements = [(r, s) for r in R for s in M]
            classes = []
            for e in elements:
                found = False
                for c in classes:
                    if equiv(e, c[0]):
                        c.append(e)
                        found = True
                        break
                if not found:
                    classes.append([e])
                    
            def add(c1, c2):
                r1, s1 = classes[c1][0]
                r2, s2 = classes[c2][0]
                r3 = (r1 * s2 + r2 * s1) % n
                s3 = (s1 * s2) % n
                for i, c in enumerate(classes):
                    if equiv((r3, s3), c[0]):
                        return i
                return None

            def mul(c1, c2):
                r1, s1 = classes[c1][0]
                r2, s2 = classes[c2][0]
                r3 = (r1 * r2) % n
                s3 = (s1 * s2) % n
                for i, c in enumerate(classes):
                    if equiv((r3, s3), c[0]):
                        return i
                return None
                
            one_idx = None
            for i, c in enumerate(classes):
                if equiv((1, 1), c[0]):
                    one_idx = i
                    break
                    
            if len(classes) <= 1:
                # The zero ring is not a local ring
                is_local = False
                S_inv_P_is_max = False
            else:
                units = set()
                for i in range(len(classes)):
                    for j in range(len(classes)):
                        if mul(i, j) == one_idx:
                            units.add(i)
                            break
                non_units = set(range(len(classes))) - units
                
                # A finite commutative ring is local iff its non-units form an ideal
                is_ideal = True
                for x in non_units:
                    for y in non_units:
                        if add(x, y) not in non_units:
                            is_ideal = False
                            break
                    if not is_ideal:
                        break
                if is_ideal:
                    for x in non_units:
                        for r in range(len(classes)):
                            if mul(x, r) not in non_units:
                                is_ideal = False
                                break
                        if not is_ideal:
                            break
                            
                is_local = is_ideal
                
                # Check if S^{-1}P is exactly the unique maximal ideal
                S_inv_P = set()
                for i, c in enumerate(classes):
                    for r, s in c:
                        if r in P:
                            S_inv_P.add(i)
                            break
                            
                S_inv_P_is_max = is_local and (S_inv_P == non_units)
                
            neg_q = not S_inv_P_is_max
            
            return [h1, h2, neg_q]
            
        return [False, False, False]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S = R \\setminus P",
    "¬Q: S^{-1}R is not a local ring with unique maximal ideal S^{-1}P"
]

N_HYP = 2
NEG_Q_INDEX = 2