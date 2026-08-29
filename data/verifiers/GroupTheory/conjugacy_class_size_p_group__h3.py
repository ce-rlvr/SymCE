import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a finite p-group",
    "¬Q: The size of the conjugacy class of x in G is not a power of p"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        p, G, x = witness
    except Exception:
        return [False, False, False]
        
    # H_1: p is a prime number
    try:
        h1 = sympy.isprime(p)
        if h1 is None:
            h1 = False
    except Exception:
        h1 = False
        
    # H_2: G is a finite p-group
    try:
        if not isinstance(G, PermutationGroup):
            h2 = False
        elif not isinstance(p, (int, sympy.Integer)) or p < 2:
            h2 = False
        else:
            n = G.order()
            if n == 1:
                h2 = True
            else:
                temp = n
                while temp % p == 0:
                    temp //= p
                h2 = (temp == 1)
    except Exception:
        h2 = False
        
    # ¬Q: The size of the conjugacy class of x in G is not a power of p
    try:
        if not isinstance(G, PermutationGroup):
            neg_q = True
        elif not isinstance(x, Permutation):
            neg_q = True
        elif not G.contains(x):
            # If x is not in G, the conjugacy class of x in G is undefined.
            # Thus the statement "The size of the conjugacy class of x in G is a power of p" is false.
            neg_q = True
        else:
            orbit = set()
            for g in G.elements:
                orbit.add(g * x * g**-1)
            size = len(orbit)
            
            if size == 1:
                is_power = True
            elif not isinstance(p, (int, sympy.Integer)) or p < 2:
                is_power = False
            else:
                temp = size
                while temp % p == 0:
                    temp //= p
                is_power = (temp == 1)
            neg_q = not is_power
    except Exception:
        neg_q = True
        
    return [bool(h1), bool(h2), bool(neg_q)]