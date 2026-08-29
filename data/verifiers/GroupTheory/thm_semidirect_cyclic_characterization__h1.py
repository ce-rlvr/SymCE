import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup
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

def are_isomorphic(m, n, k1, k2):
    N = m * n
    # Try sympy's is_isomorphic
    try:
        perm_a1 = []
        perm_b1 = []
        perm_a2 = []
        perm_b2 = []
        for x in range(m):
            for y in range(n):
                perm_a1.append(((x + 1) % m) * n + y)
                perm_b1.append(((k1 * x) % m) * n + (y + 1) % n)
                perm_a2.append(((x + 1) % m) * n + y)
                perm_b2.append(((k2 * x) % m) * n + (y + 1) % n)
        G1 = PermutationGroup(Permutation(perm_a1, size=N), Permutation(perm_b1, size=N))
        G2 = PermutationGroup(Permutation(perm_a2, size=N), Permutation(perm_b2, size=N))
        if hasattr(G1, 'is_isomorphic'):
            return G1.is_isomorphic(G2)
    except Exception:
        pass
    
    if N > 200:
        return False

    # Fallback: naive isomorphism check for small groups
    def get_table(k):
        table = []
        for x1 in range(m):
            for y1 in range(n):
                row = []
                for x2 in range(m):
                    for y2 in range(n):
                        x3 = (x1 + pow(k, y1, m) * x2) % m
                        y3 = (y1 + y2) % n
                        row.append(x3 * n + y3)
                table.append(row)
        return table
    
    T2 = get_table(k2)
    
    def power(T, x, p):
        res = 0
        for _ in range(p):
            res = T[res][x]
        return res
        
    def generate_size(T, A, B):
        seen = {0}
        q = [0]
        while q:
            curr = q.pop(0)
            for gen in (A, B):
                nxt = T[curr][gen]
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)
        return len(seen)
        
    for A in range(N):
        if power(T2, A, m) != 0:
            continue
        A_k1 = power(T2, A, k1)
        for B in range(N):
            if power(T2, B, n) != 0:
                continue
            if T2[B][A] == T2[A_k1][B]:
                if generate_size(T2, A, B) == N:
                    return True
    return False

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                m, n, k = witness
                h1 = (isinstance(m, int) and isinstance(n, int) and isinstance(k, int) and
                      m >= 2 and n >= 1 and math.gcd(k, m) == 1 and pow(k, n, m) == 1)
            elif len(witness) == 4:
                m, n, k1, k2 = witness
                h1 = (isinstance(m, int) and isinstance(n, int) and isinstance(k1, int) and isinstance(k2, int) and
                      m >= 2 and n >= 1 and math.gcd(k1, m) == 1 and pow(k1, n, m) == 1 and
                      math.gcd(k2, m) == 1 and pow(k2, n, m) == 1)
    except Exception:
        h1 = False

    try:
        if h1:
            if len(witness) == 3:
                m, n, k = witness
                for k2 in range(m):
                    if k2 == k % m:
                        continue
                    if math.gcd(k2, m) != 1:
                        continue
                    if pow(k2, n, m) != 1:
                        continue
                    if are_isomorphic(m, n, k, k2):
                        neg_q = True
                        break
            elif len(witness) == 4:
                m, n, k1, k2 = witness
                if k1 % m != k2 % m:
                    if are_isomorphic(m, n, k1, k2):
                        neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: phi is a valid action homomorphism from Z_n to Aut(Z_m)",
    "¬Q: The isomorphism class of G is not uniquely determined by phi (there exists another phi giving the same isomorphism class)"
]

N_HYP = 1
NEG_Q_INDEX = 1