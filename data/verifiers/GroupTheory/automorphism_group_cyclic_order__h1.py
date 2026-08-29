import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import totient
import itertools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1), Permutation(2, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def count_automorphisms(G):
    """
    Computes the size of the automorphism group of a finite PermutationGroup G.
    """
    elements = list(G.generate())
    n = len(elements)
    gens = list(set(G.generators))
    
    # Find the identity element
    identity = None
    for e in elements:
        if e * e == e:
            identity = e
            break
            
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    
    # Precompute Cayley table
    table = [[0] * n for _ in range(n)]
    for i, a in enumerate(elements):
        for j, b in enumerate(elements):
            table[i][j] = elem_to_idx[a * b]
            
    aut_count = 0
    
    # An automorphism is uniquely determined by the images of the generators.
    # We iterate over all possible assignments of generators to elements in G.
    for target_gens in itertools.product(elements, repeat=len(gens)):
        mapping = {elem_to_idx[identity]: elem_to_idx[identity]}
        queue = [elem_to_idx[identity]]
        
        valid = True
        gen_mapping = {elem_to_idx[g]: elem_to_idx[tg] for g, tg in zip(gens, target_gens)}
        
        head = 0
        # BFS to extend the mapping to all elements of G
        while head < len(queue) and valid:
            curr = queue[head]
            head += 1
            
            for g_idx, tg_idx in gen_mapping.items():
                next_elem = table[curr][g_idx]
                next_target = table[mapping[curr]][tg_idx]
                
                if next_elem in mapping:
                    if mapping[next_elem] != next_target:
                        valid = False
                        break
                else:
                    mapping[next_elem] = next_target
                    queue.append(next_elem)
                    
        # If the mapping is a well-defined homomorphism and is bijective, it's an automorphism
        if valid and len(mapping) == n:
            if len(set(mapping.values())) == n:
                aut_count += 1
                
    return aut_count

def conditions(witness) -> list[bool]:
    # H_1: The order of G is a finite integer n
    try:
        if not isinstance(witness, PermutationGroup):
            h1_ok = False
        else:
            elements = list(witness.generate())
            n = len(elements)
            h1_ok = (n > 0)
    except Exception:
        h1_ok = False

    # ¬Q: The order of the automorphism group of G is not equal to Euler's totient function phi(n)
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            aut_count = count_automorphisms(witness)
            expected = totient(n)
            neg_q_ok = (aut_count != expected)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The order of G is a finite integer n",
    "¬Q: The order of the automorphism group of G is not equal to Euler's totient function phi(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1