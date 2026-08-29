import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
    "H_1: G is an infinite cyclic group",
    "H_2: a is a generator of G",
    "H_3: n is a positive integer",
    "¬Q: The index of H in G is not equal to n"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            a = witness.get('a')
            n = witness.get('n')
            H = witness.get('H')
        elif isinstance(witness, tuple) and len(witness) == 4:
            G, a, n, H = witness
        else:
            G = getattr(witness, 'G', None)
            a = getattr(witness, 'a', None)
            n = getattr(witness, 'n', None)
            H = getattr(witness, 'H', None)
    except Exception:
        return [False, False, False, False]

    # H1: G is an infinite cyclic group
    try:
        h1 = False
        if isinstance(G, str) and G.lower() in ['z', 'integers', 'infinite cyclic group', 'z_add']:
            h1 = True
        elif str(G) in ['Integers', 'S.Integers', 'Z']:
            h1 = True
        elif type(G).__name__ == 'FreeGroup' and len(G.generators) == 1:
            h1 = True
    except Exception:
        h1 = False

    # H2: a is a generator of G
    try:
        h2 = False
        if h1:
            if isinstance(G, str) or str(G) in ['Integers', 'S.Integers', 'Z']:
                if str(a) in ['1', '-1']:
                    h2 = True
            elif type(G).__name__ == 'FreeGroup':
                gens = G.generators
                if a == gens[0] or a == gens[0]**-1:
                    h2 = True
    except Exception:
        h2 = False

    # H3: n is a positive integer
    try:
        h3 = False
        if hasattr(n, 'is_integer') and n.is_integer:
            h3 = bool(n > 0)
        elif isinstance(n, int):
            h3 = bool(n > 0)
        else:
            h3 = bool(int(n) > 0 and float(n) == int(n))
    except Exception:
        h3 = False

    # neg_Q: The index of H in G is NOT equal to n
    try:
        neg_q = False
        index = None
        
        if isinstance(H, int) or (hasattr(H, 'is_integer') and H.is_integer):
            h_val = int(H)
            index = abs(h_val) if h_val != 0 else float('inf')
        elif str(H) in ['Integers', 'S.Integers', 'Z']:
            index = 1
        elif isinstance(H, str):
            s = H.strip()
            if s.lower() == 'z':
                index = 1
            elif s == '{0}':
                index = float('inf')
            else:
                num_str = ''
                if s.startswith('-'):
                    num_str = '-'
                    s = s[1:]
                for char in s:
                    if char.isdigit():
                        num_str += char
                    else:
                        break
                if num_str and num_str != '-':
                    h_val = int(num_str)
                    index = abs(h_val) if h_val != 0 else float('inf')
        elif type(H).__name__ == 'FreeGroupElement':
            exp = 0
            for gen, power in H.array_form:
                exp += power
            index = abs(exp) if exp != 0 else float('inf')
        elif type(H).__name__ == 'ImageSet':
            try:
                lam = H.lamda
                val1 = lam(1)
                val0 = lam(0)
                step = abs(val1 - val0)
                index = int(step) if step != 0 else float('inf')
            except Exception:
                pass
        elif hasattr(H, '__iter__') and not isinstance(H, str):
            elements = list(H)
            if len(elements) == 0:
                index = float('inf')
            elif type(elements[0]).__name__ == 'FreeGroupElement':
                g = 0
                for x in elements:
                    exp = 0
                    for gen, power in x.array_form:
                        exp += power
                    g = math.gcd(g, abs(exp))
                index = g if g != 0 else float('inf')
            else:
                all_zero = True
                for x in elements:
                    if int(x) != 0:
                        all_zero = False
                        break
                if all_zero:
                    index = float('inf')
                else:
                    g = 0
                    for x in elements:
                        g = math.gcd(g, abs(int(x)))
                    index = g if g != 0 else float('inf')
        
        if index is not None:
            neg_q = (float(index) != float(n))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]