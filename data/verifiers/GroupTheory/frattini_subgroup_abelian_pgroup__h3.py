import sympy
import sympy.ntheory
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, p = witness
    except Exception:
        return [False, False, False]
        
    # H1: p is a prime number
    try:
        h1 = bool(sympy.ntheory.isprime(p))
    except Exception:
        h1 = False
        
    # H2: G is a finite abelian p-group, written additively
    try:
        is_ab = getattr(G, 'is_abelian', False)
        if callable(is_ab):
            is_ab = is_ab()
            
        if not is_ab:
            h2 = False
        else:
            order_attr = getattr(G, 'order')
            order = order_attr() if callable(order_attr) else order_attr
            
            if order < 1 or order == float('inf'):
                h2 = False
            elif order == 1:
                h2 = True
            else:
                factors = sympy.ntheory.primefactors(order)
                if len(factors) == 1 and factors[0] == p:
                    h2 = True
                else:
                    h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: Phi(G) != pG
    try:
        elements = list(G.elements) if hasattr(G, 'elements') else list(G.generate())
        order_attr = getattr(G, 'order')
        order = order_attr() if callable(order_attr) else order_attr
        
        # Compute the Frattini subgroup Phi(G) for a finite abelian group
        # Phi(G) is the intersection of G^q for all prime factors q of |G|
        if order == 1:
            phi_G = set(elements)
        else:
            primes = sympy.ntheory.primefactors(order)
            phi_G = set(elements)
            for q in primes:
                G_q = set((x**q) for x in elements)
                phi_G = phi_G.intersection(G_q)
                
        # Compute pG (which is G^p in multiplicative notation)
        pG = set((x**p) for x in elements)
        
        neg_q = not (phi_G == pG)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a finite abelian p-group, written additively",
    "¬Q: Phi(G) != pG"
]

N_HYP = 2
NEG_Q_INDEX = 2