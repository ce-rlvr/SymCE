import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy import isprime
import math

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_semisimple(G):
    """
    A finite group is semisimple if it has no non-trivial normal solvable subgroups.
    Equivalently, it has no non-trivial normal abelian subgroups.
    We check this by verifying that the normal closure of every non-identity element is non-abelian.
    """
    if not isinstance(G, PermutationGroup):
        return False
    if G.order() > 10000:
        return False
    if G.order() == 1:
        return True
        
    elements = list(G.generate())
    checked = set()
    for g in elements:
        if g.is_Identity:
            continue
        if g in checked:
            continue
            
        # Find the conjugacy class of g (which generates its normal closure)
        cclass = set()
        frontier = [g]
        cclass.add(g)
        gens = G.generators
        while frontier:
            curr = frontier.pop()
            for gen in gens:
                nxt = gen * curr * ~gen
                if nxt not in cclass:
                    cclass.add(nxt)
                    frontier.append(nxt)
                nxt_inv = ~gen * curr * gen
                if nxt_inv not in cclass:
                    cclass.add(nxt_inv)
                    frontier.append(nxt_inv)
                    
        checked.update(cclass)
        
        # The normal closure is abelian iff the generators (the conjugacy class) commute pairwise
        cclass_list = list(cclass)
        is_abelian = True
        for i in range(len(cclass_list)):
            for j in range(i + 1, len(cclass_list)):
                if cclass_list[i] * cclass_list[j] != cclass_list[j] * cclass_list[i]:
                    is_abelian = False
                    break
            if not is_abelian:
                break
                
        if is_abelian:
            return False
            
    return True

def conditions(witness) -> list[bool]:
    try:
        G, p = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a semisimple finite group
    try:
        h1 = is_semisimple(G)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        if isinstance(p, (int, sympy.Integer)):
            h2 = bool(isprime(p))
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: O^p(G) is not equal to G
    # O^p(G) is the smallest normal subgroup such that the quotient is a p-group.
    # O^p(G) != G iff G has a non-trivial p-group quotient.
    # Since any non-trivial p-group has an abelian quotient of order p, 
    # G has a non-trivial p-group quotient iff its abelianization G/G' has order divisible by p.
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(p, (int, sympy.Integer)):
            neg_q = False
        else:
            ds = G.derived_subgroup
            if callable(ds):
                G_prime = ds()
            else:
                G_prime = ds
            index = G.order() // G_prime.order()
            neg_q = bool(index % p == 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "H_2: p is a prime number",
    "¬Q: O^p(G) is not equal to G"
]

N_HYP = 2
NEG_Q_INDEX = 2