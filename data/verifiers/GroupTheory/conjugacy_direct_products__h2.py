import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "¬Q: Conjugacy in G x H is not equivalent to component-wise conjugacy"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple):
            return [False, False]
            
        if len(witness) == 2:
            G, H = witness
            h1_ok = hasattr(G, 'elements') and hasattr(H, 'elements')
            if not h1_ok:
                return [False, False]
            # The conclusion is a logical tautology for any valid groups G and H.
            # \exists x \exists y (P(x) \land Q(y)) <-> (\exists x P(x)) \land (\exists y Q(y))
            return [True, False]
            
        elif len(witness) == 4:
            G, H, pair1, pair2 = witness
            g1, h1 = pair1
            g2, h2 = pair2
        elif len(witness) == 6:
            G, H, g1, h1, g2, h2 = witness
        else:
            return [False, False]
            
        h1_ok = hasattr(G, 'elements') and hasattr(H, 'elements')
        if not h1_ok:
            return [False, False]
            
        conj_G = any(x * g1 * x**-1 == g2 for x in G.elements)
        conj_H = any(y * h1 * y**-1 == h2 for y in H.elements)
        
        conj_GxH = False
        for x in G.elements:
            for y in H.elements:
                if x * g1 * x**-1 == g2 and y * h1 * y**-1 == h2:
                    conj_GxH = True
                    break
            if conj_GxH:
                break
                
        neg_q = (conj_GxH != (conj_G and conj_H))
        return [True, neg_q]
        
    except Exception:
        return [False, False]