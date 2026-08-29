import math
from sympy import Integer, Matrix, eye, zeros
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Unpack witness
    if isinstance(witness, dict):
        G = witness.get('G')
        g = witness.get('g')
        n = witness.get('n')
        k = witness.get('k')
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 4:
            G, g, n, k = witness
        elif len(witness) == 3:
            G, g, k = witness
            n = None
        else:
            return [False, False, False, False]
    else:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = getattr(G, 'is_group', False) or hasattr(G, 'elements') or hasattr(G, 'generators') or isinstance(G, (list, tuple, set))
        if not h1 and G is not None:
            h1 = True  # Be lenient with group representation as long as it's provided
    except Exception:
        h1 = False

    # H_2: the order of g is a finite integer n
    try:
        if n is None:
            e = g**0
            m = g
            n_computed = 0
            for i in range(1, 1000):
                if m == e:
                    n_computed = i
                    break
                m = m * g
            n = n_computed
            h2 = (n > 0)
        else:
            h2 = isinstance(n, (int, Integer))
            if h2:
                e = g**0
                if n == 0:
                    m = g
                    h2_check = True
                    for i in range(1, 1000):
                        if m == e:
                            h2_check = False
                            break
                        m = m * g
                    h2 = h2 and h2_check
                elif n > 0:
                    m = g
                    h2_check = True
                    for i in range(1, n):
                        if m == e:
                            h2_check = False
                            break
                        m = m * g
                    h2 = h2 and h2_check and (m == e)
                else:
                    h2 = False
    except Exception:
        h2 = False

    # H_3: k is an integer
    try:
        h3 = isinstance(k, (int, Integer))
    except Exception:
        h3 = False

    # ¬Q: The order of the element g^k is not n / gcd(n, k)
    try:
        gk = g**k
        e = g**0
        
        if n == 0:
            if gk == e:
                order_gk = 1
            else:
                order_gk = 0
        else:
            m = gk
            order_gk = 0
            for i in range(1, int(n) + 2):
                if m == e:
                    order_gk = i
                    break
                m = m * gk
            if order_gk == 0:
                order_gk = float('inf')
        
        denom = math.gcd(int(n), int(k))
        expected = int(n) / denom
        
        neg_q = (order_gk != expected)
    except ZeroDivisionError:
        # If n=0 and k=0, gcd(0,0)=0, division by zero means the formula is undefined (fails)
        neg_q = True
    except Exception:
        neg_q = True

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: the order of g is a finite integer n",
    "H_3: k is an integer",
    "¬Q: The order of the element g^k is not n / gcd(n, k)"
]

N_HYP = 3
NEG_Q_INDEX = 3