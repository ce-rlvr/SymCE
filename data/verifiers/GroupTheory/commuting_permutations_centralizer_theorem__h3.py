import sympy
from sympy.combinatorics import Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        n, sigma = witness
    except Exception:
        return [False, False, False]
        
    # H1: n is an integer with n >= 1
    try:
        h1 = type(n) is int and n >= 1
    except Exception:
        h1 = False
        
    # H2: sigma is an element of S_n
    try:
        if isinstance(sigma, Permutation):
            supp = sigma.support()
            if not supp:
                h2 = True
            else:
                h2 = max(supp) < n
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: The centralizer of sigma in S_n is NOT exactly the cyclic subgroup <sigma>
    try:
        if not (h1 and h2):
            neg_q = False
        elif n > 7:
            # Prevent timeout for large n
            neg_q = False
        else:
            # Helper to normalize permutation size to exactly n
            def to_size_n(p, size):
                arr = p.array_form
                if len(arr) < size:
                    arr = arr + list(range(len(arr), size))
                elif len(arr) > size:
                    arr = arr[:size]
                return Permutation(arr)
                
            sigma_n = to_size_n(sigma, n)
            
            # Compute the cyclic subgroup <sigma>
            order = sigma_n.order()
            cyclic_subgroup = set()
            curr = to_size_n(Permutation(), n)
            for _ in range(order):
                cyclic_subgroup.add(curr)
                curr = to_size_n(curr * sigma_n, n)
                
            # Compute the centralizer of sigma in S_n
            Sn = SymmetricGroup(n)
            centralizer = set()
            for tau in Sn.generate():
                tau_n = to_size_n(tau, n)
                # Check if tau commutes with sigma
                if to_size_n(tau_n * sigma_n, n) == to_size_n(sigma_n * tau_n, n):
                    centralizer.add(tau_n)
                    
            # The conclusion fails if the centralizer is not exactly the cyclic subgroup
            neg_q = (centralizer != cyclic_subgroup)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer with n >= 1",
    "H_2: sigma is an element of S_n",
    "¬Q: The centralizer of sigma in S_n is not exactly the cyclic subgroup <sigma>"
]

N_HYP = 2
NEG_Q_INDEX = 2