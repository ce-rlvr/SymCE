import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group theory and linear algebra objects
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
    "H_1: R and S are commutative rings with identity",
    "H_2: R is a subring of S",
    "H_3: S is an integral extension of R",
    "H_4: Q_1 and Q_2 are prime ideals of S",
    "H_5: Q_1 ∩ R = Q_2 ∩ R",
    "¬Q: Q_1 != Q_2"
]

N_HYP = 5
NEG_Q_INDEX = 5

# Expected witness format for this algebraic counterexample:
# witness = (n, add, mul, R_elements, Q1_elements, Q2_elements)
# where:
#   n: int, the number of elements in the finite ring S. Elements are represented as integers 0, 1, ..., n-1.
#   add: list of lists of size n x n, the addition table of S.
#   mul: list of lists of size n x n, the multiplication table of S.
#   R_elements: list of ints, the elements of the subring R.
#   Q1_elements: list of ints, the elements of the prime ideal Q1.
#   Q2_elements: list of ints, the elements of the prime ideal Q2.

def conditions(witness):
    try:
        if len(witness) != 6:
            return [False] * 6
        n, add, mul, R_elements, Q1_elements, Q2_elements = witness
        
        # H1: R and S are commutative rings with identity
        h1 = True
        zero = None
        identity = None
        
        if not isinstance(n, int) or n <= 0:
            h1 = False
        else:
            # Find additive identity (zero)
            for i in range(n):
                if all(add[i][j] == j and add[j][i] == j for j in range(n)):
                    zero = i
                    break
            if zero is None:
                h1 = False
            
            # Check addition is an abelian group
            if h1:
                for i in range(n):
                    if not h1: break
                    for j in range(n):
                        if add[i][j] != add[j][i]: h1 = False; break
                        for k in range(n):
                            if add[add[i][j]][k] != add[i][add[j][k]]: h1 = False; break
            
            # Check existence of additive inverses
            if h1:
                for i in range(n):
                    if not any(add[i][j] == zero for j in range(n)): h1 = False; break
            
            # Check multiplication is commutative and associative
            if h1:
                for i in range(n):
                    if not h1: break
                    for j in range(n):
                        if mul[i][j] != mul[j][i]: h1 = False; break
                        for k in range(n):
                            if mul[mul[i][j]][k] != mul[i][mul[j][k]]: h1 = False; break
            
            # Check distributivity
            if h1:
                for i in range(n):
                    if not h1: break
                    for j in range(n):
                        if not h1: break
                        for k in range(n):
                            if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: h1 = False; break
            
            # Find multiplicative identity
            if h1:
                for i in range(n):
                    if all(mul[i][j] == j and mul[j][i] == j for j in range(n)):
                        identity = i
                        break
                if identity is None: h1 = False
                
        # H2: R is a subring of S
        h2 = False
        if h1:
            h2 = True
            try:
                R_set = set(R_elements)
            except Exception:
                h2 = False
                
            if h2 and (not R_set or zero not in R_set or identity not in R_set):
                h2 = False
                
            if h2:
                for i in R_set:
                    if not h2: break
                    for j in R_set:
                        if add[i][j] not in R_set: h2 = False; break
                        if mul[i][j] not in R_set: h2 = False; break
            if h2:
                for i in R_set:
                    if not any(add[i][j] == zero and j in R_set for j in range(n)):
                        h2 = False; break
                        
        # H3: S is an integral extension of R
        h3 = False
        if h2:
            h3 = True
            neg_id = None
            for i in range(n):
                if add[identity][i] == zero:
                    neg_id = i
                    break
            if neg_id not in R_set:
                h3 = False
            else:
                # For finite rings, every element is integral over any subring.
                # We verify this by finding a repeating power s^k = s^m, 
                # which gives the monic polynomial x^k - x^m = 0 with coefficients in R.
                for s in range(n):
                    powers = [identity, s]
                    curr = s
                    found = False
                    for _ in range(n + 1):
                        curr = mul[curr][s]
                        if curr in powers:
                            found = True
                            break
                        powers.append(curr)
                    if not found:
                        h3 = False
                        break
                        
        # H4: Q1 and Q2 are prime ideals of S
        h4 = False
        if h1:
            def is_prime_ideal(Q_list):
                try:
                    Q = set(Q_list)
                except Exception:
                    return False
                if not Q or len(Q) == n or zero not in Q: return False
                for i in Q:
                    if not any(add[i][j] == zero and j in Q for j in range(n)):
                        return False
                for i in Q:
                    for j in Q:
                        if add[i][j] not in Q: return False
                for q in Q:
                    for s in range(n):
                        if mul[q][s] not in Q: return False
                for a in range(n):
                    for b in range(n):
                        if mul[a][b] in Q and a not in Q and b not in Q:
                            return False
                return True
            
            h4 = is_prime_ideal(Q1_elements) and is_prime_ideal(Q2_elements)
            
        # H5: Q1 ∩ R = Q2 ∩ R
        h5 = False
        if h1 and h2:
            try:
                int1 = set(Q1_elements).intersection(set(R_elements))
                int2 = set(Q2_elements).intersection(set(R_elements))
                h5 = (int1 == int2)
            except Exception:
                h5 = False
                
        # neg_Q: Q1 != Q2
        neg_q = False
        try:
            neg_q = set(Q1_elements) != set(Q2_elements)
        except Exception:
            pass
            
        return [h1, h2, h3, h4, h5, neg_q]
    except Exception:
        return [False, False, False, False, False, False]