import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    Hypotheses:
      1. G is a finite group
      2. N is a normal subgroup of G
      3. The order of N is a power of p
      4. P is a Sylow p-subgroup of G
    Conclusion:
      N is a subgroup of P
    """
    if isinstance(witness, dict):
        G = witness.get('G')
        N = witness.get('N')
        P = witness.get('P')
        p = witness.get('p')
    else:
        try:
            G, N, P, p = witness
        except Exception:
            return [False] * 4 + [False]
            
    try:
        p = int(p)
    except Exception:
        pass

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        is_sub = all(g in G for g in N.generators)
        if not is_sub:
            h2 = False
        else:
            h2 = True
            for g in G.generators:
                for n in N.generators:
                    if (g * n * ~g) not in N:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H_3: The order of N is a power of p
    try:
        order_N = N.order()
        if order_N == 1:
            h3 = True
        elif p <= 1:
            h3 = False
        else:
            temp = order_N
            while temp % p == 0:
                temp //= p
            h3 = (temp == 1)
    except Exception:
        h3 = False

    # H_4: P is a Sylow p-subgroup of G
    try:
        is_sub = all(g in G for g in P.generators)
        if not is_sub:
            h4 = False
        else:
            order_P = P.order()
            order_G = G.order()
            if p <= 1:
                h4 = False
            else:
                temp = order_P
                while temp % p == 0:
                    temp //= p
                is_power = (temp == 1)
                
                if not is_power:
                    h4 = False
                else:
                    # P is a Sylow p-subgroup if its order is the highest power of p dividing |G|
                    h4 = (order_G % (order_P * p) != 0)
    except Exception:
        h4 = False

    # ¬Q: N is not a subgroup of P
    try:
        neg_q = not all(g in P for g in N.generators)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: The order of N is a power of p",
    "H_4: P is a Sylow p-subgroup of G",
    "¬Q: N is not a subgroup of P"
]

N_HYP = 4
NEG_Q_INDEX = 4