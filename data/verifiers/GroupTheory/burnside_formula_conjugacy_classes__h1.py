import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: k(G) denotes the number of conjugacy classes of G",
    "¬Q: k(G) != (1/|G|) * sum_{g in G} |C_G(g)|"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1_ok = False
    neg_q = False
    
    try:
        elements = []
        if hasattr(witness, 'generate'):
            gen = witness.generate()
        elif hasattr(witness, 'elements'):
            gen = witness.elements
        else:
            gen = witness
            
        for i, e in enumerate(gen):
            if i >= 1000:
                raise ValueError("Too many elements")
            elements.append(e)
            
        order_G = len(elements)
        if order_G == 0:
            raise ValueError("Empty group")
            
        k_G = None
        if hasattr(witness, 'conjugacy_classes'):
            try:
                k_G = len(witness.conjugacy_classes())
            except Exception:
                pass
                
        if k_G is None:
            n = len(elements)
            parent = list(range(n))
            def find(i):
                if parent[i] == i: return i
                parent[i] = find(parent[i])
                return parent[i]
            def union(i, j):
                root_i = find(i)
                root_j = find(j)
                if root_i != root_j:
                    parent[root_i] = root_j

            for i in range(n):
                for j in range(i + 1, n):
                    if find(i) == find(j):
                        continue
                    a = elements[i]
                    b = elements[j]
                    if any((x * a == b * x) for x in elements):
                        union(i, j)
            k_G = len(set(find(i) for i in range(n)))
            
        h1_ok = True
        
        sum_C = 0
        for g in elements:
            c_g = sum(1 for x in elements if x * g == g * x)
            sum_C += c_g
            
        neg_q = bool(k_G * order_G != sum_C)
        
    except Exception:
        pass
        
    return [h1_ok, neg_q]