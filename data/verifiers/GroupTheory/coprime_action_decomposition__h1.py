import math
import sympy
import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard algebra objects
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false Coprime Action Decomposition Theorem.
    The dropped hypothesis is that G is a group (allowing G to be just a set of automorphisms).
    """
    try:
        # Format 1: witness = (n, G_list)
        # where A = Z/nZ, and G_list is a list of integers representing multiplication maps
        if isinstance(witness, tuple) and len(witness) == 2:
            n, G_list = witness
            if isinstance(n, int) and n > 0 and isinstance(G_list, (list, tuple)) and all(isinstance(g, int) for g in G_list):
                # H1: A is a finite abelian group
                h1 = True
                
                # H2: G acts on A by group automorphisms
                # Each g in G_list must be coprime to n
                h2 = all(math.gcd(g, n) == 1 for g in G_list)
                
                # H3: |G| and |A| are coprime
                h3 = (math.gcd(len(G_list), n) == 1)
                
                # Conclusion: A = C_A(G) \oplus [G, A]
                d = n
                for g in G_list:
                    d = math.gcd(d, g - 1)
                    
                neg_q = (math.gcd(d, n // d) > 1)
                
                return [h1, h2, h3, neg_q]
    except Exception:
        pass

    try:
        # Format 2: witness = (n, k, G_matrices)
        # where A = (Z/nZ)^k, and G_matrices is a list of lists of lists
        if isinstance(witness, tuple) and len(witness) == 3:
            n, k, G_matrices = witness
            if isinstance(n, int) and n > 1 and isinstance(k, int) and k > 0:
                if isinstance(G_matrices, (list, tuple)) and len(G_matrices) > 0:
                    h1 = True
                    
                    h2 = True
                    for M in G_matrices:
                        if not isinstance(M, (list, tuple)) or len(M) != k:
                            h2 = False
                            break
                        for row in M:
                            if not isinstance(row, (list, tuple)) or len(row) != k:
                                h2 = False
                                break
                        if not h2:
                            break
                        sym_M = sympy.Matrix(M)
                        det = int(sym_M.det())
                        if math.gcd(det, n) != 1:
                            h2 = False
                            break
                            
                    h3 = (math.gcd(len(G_matrices), n**k) == 1)
                    
                    A_elements = list(itertools.product(range(n), repeat=k))
                    zero = tuple([0]*k)
                    
                    def add(a, b):
                        return tuple((x + y) % n for x, y in zip(a, b))
                        
                    def apply_M(M, a):
                        res = []
                        for i in range(k):
                            val = sum(M[i][j] * a[j] for j in range(k)) % n
                            res.append(val)
                        return tuple(res)
                        
                    C_A = []
                    for a in A_elements:
                        if all(apply_M(M, a) == a for M in G_matrices):
                            C_A.append(a)
                            
                    generators = []
                    for M in G_matrices:
                        for a in A_elements:
                            Ma = apply_M(M, a)
                            neg_a = tuple((-x) % n for x in a)
                            generators.append(add(Ma, neg_a))
                            
                    G_A = {zero}
                    added = True
                    while added:
                        added = False
                        new_G_A = set(G_A)
                        for x in G_A:
                            for g in generators:
                                y = add(x, g)
                                if y not in new_G_A:
                                    new_G_A.add(y)
                                    added = True
                        G_A = new_G_A
                        
                    intersection = set(C_A).intersection(G_A)
                    is_direct_sum = (intersection == {zero}) and (len(C_A) * len(G_A) == n**k)
                    
                    neg_q = not is_direct_sum
                    
                    return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: A is a finite abelian group",
    "H_2: G acts on A by group automorphisms",
    "H_3: The orders |G| and |A| are coprime",
    "¬Q: A does not decompose as the direct sum of C_A(G) and the subgroup generated by g.a - a"
]

N_HYP = 3
NEG_Q_INDEX = 3