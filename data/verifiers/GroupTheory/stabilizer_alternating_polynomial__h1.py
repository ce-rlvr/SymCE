import sympy as sp
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: S_n acts on the polynomial ring R(x_1, ..., x_n) by permuting the variables",
    "H_2: Delta is the alternating polynomial",
    "¬Q: The stabilizer of Delta is not the alternating group A_n"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    if not isinstance(witness, (int, sp.Integer)):
        return [False, False, False]
        
    n = int(witness)
    if n < 1:
        return [False, False, False]
        
    h1 = True
    h2 = True
    
    try:
        if n > 5:
            neg_q = False
        else:
            xs = sp.symbols(f'x1:{n+1}')
            delta = sp.Integer(1)
            for i in range(n):
                for j in range(i+1, n):
                    delta *= (xs[i] - xs[j])
            delta = sp.expand(delta)
            
            Sn = SymmetricGroup(n)
            stabilizer = set()
            for p in Sn.generate_dimino():
                subs_dict = {xs[i]: xs[p(i)] for i in range(n)}
                p_delta = sp.expand(delta.subs(subs_dict))
                if p_delta == delta:
                    stabilizer.add(p)
                    
            try:
                An = AlternatingGroup(n)
                An_elements = set(An.generate_dimino())
                neg_q = (stabilizer != An_elements)
            except ValueError:
                # AlternatingGroup(1) raises ValueError in SymPy
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]