import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import primefactors, isprime

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

def conditions(witness):
    G = None
    p = None
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            a, b = witness
            if isinstance(a, (int, sympy.Integer)) and not isinstance(b, (int, sympy.Integer)):
                p, G = a, b
            else:
                G, p = a, b
        else:
            G = witness
    except Exception:
        return [False, False]

    if p is not None:
        try:
            if not isprime(p):
                h1 = False
            else:
                try:
                    order_G = G.order()
                except AttributeError:
                    order_G = len(G)
                h1 = (order_G % p == 0)
        except Exception:
            h1 = False

        try:
            has_element = False
            if hasattr(G, 'elements'):
                elements = G.elements
            else:
                elements = G
                
            for g in elements:
                try:
                    o = g.order()
                except AttributeError:
                    o = None
                if o == p:
                    has_element = True
                    break
            neg_q = not has_element
        except Exception:
            neg_q = False

        return [bool(h1), bool(neg_q)]
    else:
        try:
            try:
                order_G = G.order()
            except AttributeError:
                order_G = len(G)
                
            p_factors = primefactors(order_G)
            if not p_factors:
                return [False, False]
                
            h1 = True
            
            if hasattr(G, 'elements'):
                elements = G.elements
            else:
                elements = G
                
            neg_q = False
            for pf in p_factors:
                has_element = False
                for g in elements:
                    try:
                        o = g.order()
                    except AttributeError:
                        o = None
                    if o == pf:
                        has_element = True
                        break
                if not has_element:
                    neg_q = True
                    break
                    
            return [bool(h1), bool(neg_q)]
        except Exception:
            return [False, False]

CONDITION_LABELS = [
    "H_1: p is a prime number that divides the order of G",
    "¬Q: G does not contain at least one element of order p"
]

N_HYP = 1
NEG_Q_INDEX = 1