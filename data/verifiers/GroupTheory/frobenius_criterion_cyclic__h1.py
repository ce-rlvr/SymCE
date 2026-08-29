import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    "H_1: The order of G is n",
    "H_2: For every positive integer d dividing n, the equation x^d = e has at most d solutions in G",
    "¬Q: G is not a cyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # Extract G and n
    if isinstance(witness, tuple) and len(witness) == 2:
        G, n = witness
    else:
        G = witness
        try:
            n = G.order()
        except AttributeError:
            try:
                n = len(G)
            except TypeError:
                n = None

    # H1: The order of G is n
    try:
        if hasattr(G, 'order'):
            order_G = G.order()
        else:
            order_G = len(list(G))
        h1 = (order_G == n) and isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h1 = False

    # H2: For every positive integer d dividing n, x^d = e has at most d solutions
    h2 = False
    try:
        if h1:
            if hasattr(G, 'elements'):
                elements = list(G.elements)
            elif hasattr(G, 'generate'):
                elements = list(G.generate())
            else:
                elements = list(G)
                
            if hasattr(G, 'identity'):
                e = G.identity() if callable(G.identity) else G.identity
            else:
                e = None
                for x in elements:
                    if hasattr(x, 'is_identity'):
                        is_id = x.is_identity() if callable(x.is_identity) else x.is_identity
                        if is_id:
                            e = x
                            break
                if e is None:
                    idempotents = []
                    for x in elements:
                        try:
                            if x**2 == x:
                                idempotents.append(x)
                        except Exception:
                            pass
                    if idempotents:
                        e = idempotents[-1]
                    else:
                        e = elements[0]
            
            h2 = True
            for d in range(1, int(n) + 1):
                if n % d == 0:
                    solutions = 0
                    for x in elements:
                        if x**d == e:
                            solutions += 1
                    if solutions > d:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # neg_Q: G is not a cyclic group
    neg_q = False
    try:
        if hasattr(G, 'is_cyclic'):
            is_cyclic = G.is_cyclic() if callable(G.is_cyclic) else G.is_cyclic
            neg_q = not is_cyclic
        else:
            is_cyclic = False
            for x in elements:
                unique_gen = []
                unique_gen_set = set()
                hashable = True
                for k in range(1, int(n) + 1):
                    try:
                        g = x**k
                        if hashable:
                            try:
                                unique_gen_set.add(g)
                            except TypeError:
                                hashable = False
                                unique_gen.extend(list(unique_gen_set))
                                if g not in unique_gen:
                                    unique_gen.append(g)
                        else:
                            if g not in unique_gen:
                                unique_gen.append(g)
                    except Exception:
                        break
                
                if hashable:
                    if len(unique_gen_set) == n:
                        is_cyclic = True
                        break
                else:
                    if len(unique_gen) == n:
                        is_cyclic = True
                        break
            neg_q = not is_cyclic
    except Exception:
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]