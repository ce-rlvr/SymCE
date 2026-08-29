import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import totient
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, x = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: x has finite order n
    try:
        if isinstance(x, Permutation):
            n = int(x.order())
            h2 = (n > 0)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # NegQ: The index [N_G(<x>) : C_G(x)] does NOT divide phi(n)
    try:
        if not (h1 and h2):
            return [h1, h2, False]
            
        degree = G.degree
        
        def pad(p):
            if getattr(p, 'size', 0) < degree:
                return Permutation([p(i) for i in range(degree)])
            return p

        x_elements = []
        curr = pad(x)
        for _ in range(n):
            x_elements.append(curr)
            curr = curr * pad(x)
            
        G_elements = list(G.generate())
        x_set = set(x_elements)
        
        N_G_count = 0
        for g in G_elements:
            g_inv = ~g
            if all((g * h * g_inv) in x_set for h in x_elements):
                N_G_count += 1
                
        C_G_count = 0
        for g in G_elements:
            if all(g * h == h * g for h in x_elements):
                C_G_count += 1
                
        if C_G_count == 0:
            neg_q = False
        else:
            index = N_G_count // C_G_count
            if index == 0:
                neg_q = False
            else:
                phi_n = totient(n)
                neg_q = (phi_n % index != 0)
                
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: G is a group", "H_2: x has finite order n", "not Q: The index does not divide phi(n)"]
N_HYP = 2
NEG_Q_INDEX = 2