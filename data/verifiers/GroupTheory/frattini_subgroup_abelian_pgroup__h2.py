import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory

# Top-level setup: named object bindings
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
    try:
        G, p = witness
    except Exception:
        return [False, False, False]
    
    # H_1: p is a prime number
    try:
        h1 = bool(sympy.ntheory.isprime(p))
    except Exception:
        h1 = False
        
    # H_2: G is a group (and Phi(G) is its Frattini subgroup by definition)
    try:
        h2 = isinstance(G, PermutationGroup)
    except Exception:
        h2 = False
        
    # ¬Q: Phi(G) != pG
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            elements = list(G.elements)
            id_elem = elements[0]**0 if elements else None
            G_set = frozenset(elements)
            
            # Find all subgroups of G using BFS closure
            subgroups = set()
            subgroups.add(frozenset([id_elem]))
            
            queue = [set([id_elem])]
            for sg in queue:
                for g in elements:
                    if g not in sg:
                        new_sg_list = list(sg)
                        new_sg_list.append(g)
                        new_sg_set = set(new_sg_list)
                        
                        head = 0
                        while head < len(new_sg_list):
                            a = new_sg_list[head]
                            current_len = len(new_sg_list)
                            for j in range(current_len):
                                b = new_sg_list[j]
                                
                                c1 = a * b
                                if c1 not in new_sg_set:
                                    new_sg_set.add(c1)
                                    new_sg_list.append(c1)
                                    
                                c2 = b * a
                                if c2 not in new_sg_set:
                                    new_sg_set.add(c2)
                                    new_sg_list.append(c2)
                            head += 1
                            
                        fs = frozenset(new_sg_set)
                        if fs not in subgroups:
                            subgroups.add(fs)
                            queue.append(new_sg_set)
            
            # Identify maximal subgroups
            proper_subgroups = [sg for sg in subgroups if sg != G_set]
            maximal = []
            for sg in proper_subgroups:
                is_maximal = True
                for other in proper_subgroups:
                    if sg != other and sg.issubset(other):
                        is_maximal = False
                        break
                if is_maximal:
                    maximal.append(sg)
            
            # Compute Frattini subgroup Phi(G)
            if not maximal:
                phi_G = G_set
            else:
                phi_G = frozenset.intersection(*maximal)
                
            # Compute pG = {x^p | x \in G}
            pG = frozenset(x**p for x in elements)
            
            neg_q = bool(phi_G != pG)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: Phi(G) is the Frattini subgroup of G, defined as the intersection of all maximal subgroups of G",
    "¬Q: Phi(G) != pG"
]

N_HYP = 2
NEG_Q_INDEX = 2