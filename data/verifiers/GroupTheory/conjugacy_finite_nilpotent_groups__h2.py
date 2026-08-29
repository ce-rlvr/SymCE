import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    elif hasattr(G, 'generate'):
        return list(G.generate())
    else:
        return list(G)

def are_conjugate(G, x, y, elements):
    for g in elements:
        try:
            if g * x * g**(-1) == y:
                return True
        except Exception:
            pass
        try:
            if g * x * ~g == y:
                return True
        except Exception:
            pass
    return False

def p_part(x, p, m):
    k = 0
    temp = m
    while temp % p == 0:
        k += 1
        temp //= p
    if k == 0:
        return x**m
    pk = p**k
    c = m // pk
    c_inv = pow(c, -1, pk)
    d = c * c_inv
    return x**d

def get_order(x):
    if callable(getattr(x, 'order', None)):
        return x.order()
    return x.order

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, x, y = witness
            elements_provided = True
        else:
            G = witness
            elements_provided = False
            
        # H_1: G is a finite nilpotent group
        try:
            if hasattr(G, 'is_nilpotent'):
                if callable(G.is_nilpotent):
                    h1 = bool(G.is_nilpotent())
                else:
                    h1 = bool(G.is_nilpotent)
            else:
                h1 = False
        except Exception:
            h1 = False

        # neg_Q: The elements x and y are conjugate in G if and only if for every prime p dividing the order of G, their p-parts x_p and y_p are conjugate in G
        try:
            elements = get_elements(G)
            order_G = len(elements)
            
            if order_G > 1:
                primes = list(factorint(order_G).keys())
            else:
                primes = []
                
            if elements_provided:
                order_x = get_order(x)
                order_y = get_order(y)
                
                x_conj_y = are_conjugate(G, x, y, elements)
                
                all_p_conj = True
                for p in primes:
                    x_p = p_part(x, p, order_x)
                    y_p = p_part(y, p, order_y)
                    if not are_conjugate(G, x_p, y_p, elements):
                        all_p_conj = False
                        break
                        
                q = (x_conj_y == all_p_conj)
                neg_q = not q
            else:
                neg_q = False
                for x_elem in elements:
                    for y_elem in elements:
                        order_x = get_order(x_elem)
                        order_y = get_order(y_elem)
                        
                        x_conj_y = are_conjugate(G, x_elem, y_elem, elements)
                        
                        all_p_conj = True
                        for p in primes:
                            x_p = p_part(x_elem, p, order_x)
                            y_p = p_part(y_elem, p, order_y)
                            if not are_conjugate(G, x_p, y_p, elements):
                                all_p_conj = False
                                break
                        
                        if x_conj_y != all_p_conj:
                            neg_q = True
                            break
                    if neg_q:
                        break
        except Exception:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: G is a finite nilpotent group",
    "¬Q: The conjugacy of x and y in G is not equivalent to the conjugacy of all their p-parts in G"
]

N_HYP = 1
NEG_Q_INDEX = 1