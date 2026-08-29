import sympy
from sympy import Rational
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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

def conditions(witness) -> list[bool]:
    # H_1: G acts on a finite set \Omega
    try:
        if hasattr(witness, 'elements'):
            elements = list(witness.elements)
        else:
            elements = list(witness)
            
        if not elements:
            h1 = False
        else:
            h1 = all(isinstance(g, Permutation) for g in elements)
    except Exception:
        h1 = False

    # ¬Q: The number of orbits of G on \Omega is NOT equal to 1/|G| \sum_{g \in G} |Fix(g)|
    try:
        if not h1:
            neg_q = False
        else:
            n = max(g.size for g in elements)
            
            parent = list(range(n))
            def find(i):
                root = i
                while parent[root] != root:
                    root = parent[root]
                curr = i
                while curr != root:
                    nxt = parent[curr]
                    parent[curr] = root
                    curr = nxt
                return root
                
            def union(i, j):
                root_i = find(i)
                root_j = find(j)
                if root_i != root_j:
                    parent[root_i] = root_j
                    
            for g in elements:
                arr = g.array_form
                sz = len(arr)
                for i in range(sz):
                    union(i, arr[i])
                    
            if n == 0:
                num_orbits = 0
            else:
                num_orbits = len(set(find(i) for i in range(n)))
            
            sum_fix = 0
            for g in elements:
                # The number of fixed points in 0..n-1 is n minus the number of moved points
                sum_fix += n - len(g.support())
                
            lhs = num_orbits
            rhs = Rational(sum_fix, len(elements))
            
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G acts on a finite set \\Omega",
    "¬Q: The number of orbits of G on \\Omega is NOT equal to 1/|G| \\sum_{g \\in G} |Fix(g)|"
]

N_HYP = 1
NEG_Q_INDEX = 1