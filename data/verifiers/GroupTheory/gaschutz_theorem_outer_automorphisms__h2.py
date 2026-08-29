import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.ntheory import isprime
import itertools

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
        G, p = witness
    except Exception:
        return [False, False]
        
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # neg_Q: p does not divide the order of Out(G)
    try:
        elements = list(G.elements)
        n = len(elements)
        if n == 1:
            out_count = 1
        else:
            gens = list(G.generators)
            orders = [g.order() for g in elements]
            gen_orders = [g.order() for g in gens]
            
            candidates = []
            for go in gen_orders:
                cands = [e for e, o in zip(elements, orders) if o == go]
                candidates.append(cands)
                
            aut_count = 0
            
            # Find the identity element
            identity = None
            for g in elements:
                if g.order() == 1:
                    identity = g
                    break
            if identity is None:
                identity = elements[0]
                
            # Check all possible mappings of generators
            for combo in itertools.product(*candidates):
                mapping = {identity: identity}
                queue = [identity]
                valid = True
                
                # BFS to build the homomorphism and check for consistency
                while queue and valid:
                    u = queue.pop(0)
                    for h, fh in zip(gens, combo):
                        v = u * h
                        mapped_v = mapping[u] * fh
                        if v not in mapping:
                            mapping[v] = mapped_v
                            queue.append(v)
                        else:
                            if mapping[v] != mapped_v:
                                valid = False
                                break
                
                # If valid homomorphism and surjective, it's an automorphism
                if valid and len(mapping) == n:
                    aut_count += 1
                    
            # Calculate the size of the center Z(G)
            center_size = 0
            for g in elements:
                if all(g * h == h * g for h in gens):
                    center_size += 1
                    
            # |Inn(G)| = |G| / |Z(G)|
            inn_count = n // center_size
            
            # |Out(G)| = |Aut(G)| / |Inn(G)|
            out_count = aut_count // inn_count
            
        neg_q = (out_count % p != 0)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: p does not divide the order of Out(G)"
]

N_HYP = 1
NEG_Q_INDEX = 1