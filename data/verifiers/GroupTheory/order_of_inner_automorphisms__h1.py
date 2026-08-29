import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    "H_1: g is an element of G",
    "H_2: There exists a positive integer n such that g^n = e, and n is the smallest such integer",
    "H_3: \\phi_g: G \\to G is the inner automorphism defined by \\phi_g(x) = gxg^{-1}",
    "¬Q: The order of \\phi_g in the automorphism group Aut(G) does not divide n"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, g = witness
        else:
            G = witness.G
            g = witness.g
    except Exception:
        return [False, False, False, False]

    def mul(a, b):
        if hasattr(G, 'op'): return G.op(a, b)
        if hasattr(G, 'mul'): return G.mul(a, b)
        return a * b

    def inv(a):
        if hasattr(G, 'inv'): return G.inv(a)
        if hasattr(a, 'inv'): return a.inv()
        return a**-1

    try:
        if hasattr(G, 'elements'):
            if callable(G.elements):
                elems = list(G.elements())
            else:
                elems = list(G.elements)
        else:
            elems = list(G)
    except Exception:
        elems = []

    def get_id():
        if hasattr(G, 'identity'):
            return G.identity() if callable(G.identity) else G.identity
        if hasattr(G, 'e'):
            return G.e() if callable(G.e) else G.e
        if hasattr(G, 'id'):
            return G.id() if callable(G.id) else G.id
        if elems:
            for x in elems:
                try:
                    if all(mul(x, y) == y and mul(y, x) == y for y in elems):
                        return x
                except Exception:
                    continue
        return None

    e = get_id()

    # H1: g is an element of G
    try:
        if elems:
            h1 = g in elems
        elif hasattr(G, '__contains__'):
            h1 = g in G
        else:
            h1 = True
    except Exception:
        h1 = False

    # H2: There exists a positive integer n such that g^n = e, and n is the smallest such integer
    n = None
    try:
        current = g
        for i in range(1, 2000):
            is_id = False
            if e is not None and current == e:
                is_id = True
            elif hasattr(current, 'is_Identity') and current.is_Identity:
                is_id = True
            elif current == 1:
                is_id = True
            
            if is_id:
                n = i
                break
            current = mul(current, g)
        h2 = (n is not None)
    except Exception:
        h2 = False

    # H3: \phi_g: G \to G is the inner automorphism defined by \phi_g(x) = gxg^{-1}
    try:
        if not elems:
            h3 = False
        else:
            if hasattr(G, 'phi'):
                try:
                    _ = G.phi(g, elems[0])
                    phi = lambda x: G.phi(g, x)
                except Exception:
                    phi = lambda x: G.phi(x)
            else:
                g_inv = inv(g)
                phi = lambda x: mul(mul(g, x), g_inv)

            is_hom = True
            for x in elems:
                for y in elems:
                    if phi(mul(x, y)) != mul(phi(x), phi(y)):
                        is_hom = False
                        break
                if not is_hom:
                    break
            
            mapped = []
            for x in elems:
                mx = phi(x)
                if mx not in mapped:
                    mapped.append(mx)
            is_bij = len(mapped) == len(elems)
            
            g_inv = inv(g)
            is_gxg_inv = True
            for x in elems:
                px = phi(x)
                left_assoc = mul(mul(g, x), g_inv)
                right_assoc = mul(g, mul(x, g_inv))
                if px != left_assoc and px != right_assoc:
                    is_gxg_inv = False
                    break
            
            h3 = is_hom and is_bij and is_gxg_inv
    except Exception:
        h3 = False

    # neg_Q: The order of \phi_g in the automorphism group Aut(G) does not divide n
    try:
        if not h2 or not h3:
            neg_q = False
        else:
            order_phi = None
            for k in range(1, 2000):
                is_id_map = True
                for x in elems:
                    val = x
                    for _ in range(k):
                        val = phi(val)
                    if val != x:
                        is_id_map = False
                        break
                if is_id_map:
                    order_phi = k
                    break
            
            if order_phi is None:
                neg_q = False
            else:
                neg_q = (n % order_phi != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]