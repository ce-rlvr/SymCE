import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

# Top-level setup: named object bindings
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

def conditions(witness):
    try:
        p, q, G = witness
    except Exception:
        return [False, False, False, False, False]
    
    # H_1: p and q are prime numbers
    try:
        h1 = bool(isprime(p) and isprime(q))
    except Exception:
        h1 = False

    # H_2: q divides p - 1
    try:
        h2 = bool((p - 1) % q == 0)
    except Exception:
        h2 = False

    # H_3: G is a group of order pq
    try:
        h3 = bool(G.order() == p * q)
    except Exception:
        h3 = False

    # H_4: G is non-abelian
    try:
        h4 = bool(not G.is_abelian)
    except Exception:
        h4 = False

    # ¬Q: The commutator subgroup G' is not the unique Sylow p-subgroup of G
    try:
        G_prime = G.derived_subgroup()
        
        try:
            p_val = int(p)
        except Exception:
            p_val = -1
            
        if p_val > 1:
            hp = 1
            temp = int(G.order())
            while temp % p_val == 0:
                hp *= p_val
                temp //= p_val
        else:
            hp = -1
            
        is_sylow = (int(G_prime.order()) == hp)
        
        is_normal = True
        for g in G.generators:
            for h in G_prime.generators:
                if not G_prime.contains(g * h * g**-1):
                    is_normal = False
                    break
            if not is_normal:
                break
                
        q_holds = is_sylow and is_normal
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: p and q are prime numbers",
    "H_2: q divides p - 1",
    "H_3: G is a group of order pq",
    "H_4: G is non-abelian",
    "¬Q: The commutator subgroup G' is not the unique Sylow p-subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4