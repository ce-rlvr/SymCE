import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import isprime

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

def extract_witness(witness):
    if isinstance(witness, dict):
        return witness.get('G'), witness.get('p'), witness.get('P')
    elif isinstance(witness, (list, tuple)) and len(witness) == 3:
        return witness[0], witness[1], witness[2]
    elif hasattr(witness, 'G') and hasattr(witness, 'p') and hasattr(witness, 'P'):
        return witness.G, witness.p, witness.P
    else:
        return None, None, None

def is_semisimple(G):
    """
    A finite group is semisimple iff it has no non-trivial abelian normal subgroups.
    This is equivalent to saying that no non-identity element has an abelian normal closure.
    """
    try:
        if G.order() <= 1:
            return False
        # For very large groups, fallback to checking if it's a non-abelian simple group
        if G.order() > 10000:
            if getattr(G, 'is_simple', False) and not getattr(G, 'is_abelian', True):
                return True
            return False
            
        for g in G.generate():
            if getattr(g, 'is_Identity', False):
                continue
                
            is_id = True
            if hasattr(g, 'size'):
                for i in range(g.size):
                    if g(i) != i:
                        is_id = False
                        break
            if is_id:
                continue
            
            nc = G.normal_closure([g])
            if nc.is_abelian:
                return False
        return True
    except Exception:
        return False

def is_normal_subgroup(H, G):
    try:
        try:
            if not H.is_subgroup(G):
                return False
            return H.is_normal(G)
        except Exception:
            # Fallback manual check
            for h in H.generators:
                if not G.contains(h):
                    return False
            for h in H.generators:
                for g in G.generators:
                    conj = (~g) * h * g
                    if not H.contains(conj):
                        return False
            return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    G, p, P = extract_witness(witness)
    
    # H_1: Let G be a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    # H_2: Let G be a non-trivial semisimple group
    try:
        h2 = is_semisimple(G)
    except Exception:
        h2 = False

    # H_3: Let p be a prime number dividing the order of G
    try:
        h3 = isprime(p) and G.order() % p == 0
    except Exception:
        h3 = False

    # ¬Q: P IS a normal subgroup of G (Conclusion fails)
    try:
        if P is None:
            neg_q = False
        else:
            neg_q = isinstance(P, PermutationGroup) and is_normal_subgroup(P, G)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a non-trivial semisimple group",
    "H_3: p is a prime number dividing the order of G",
    "¬Q: P is a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3