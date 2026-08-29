import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime, factorint

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

CONDITION_LABELS = [
    "H_1: p and q are prime numbers",
    "H_2: p > q",
    "H_3: G is a group of order pq",
    "H_4: G is non-abelian",
    "¬Q: The commutator subgroup G' is not the unique Sylow p-subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            q = witness.get('q')
            G = witness.get('G')
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            p, q, G = witness
        else:
            G = witness
            order = G.order()
            factors = factorint(order)
            primes = sorted(list(factors.keys()), reverse=True)
            if len(primes) >= 2:
                p, q = primes[0], primes[1]
            elif len(primes) == 1:
                p = primes[0]
                q = primes[0]
            else:
                p, q = 0, 0
    except Exception:
        return [False] * 5

    try:
        h1 = bool(isprime(p) and isprime(q))
    except Exception:
        h1 = False

    try:
        h2 = bool(p > q)
    except Exception:
        h2 = False

    try:
        h3 = bool(hasattr(G, 'order') and G.order() == p * q)
    except Exception:
        h3 = False

    try:
        h4 = bool(hasattr(G, 'is_abelian') and not G.is_abelian)
    except Exception:
        h4 = False

    try:
        if not isprime(p):
            q_holds = False
        else:
            order = G.order()
            if order % p != 0:
                q_holds = False
            else:
                pk = 1
                temp = order
                while temp % p == 0:
                    pk *= p
                    temp //= p
                
                G_prime = G.derived_subgroup()
                q_holds = bool(G_prime.order() == pk)
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]