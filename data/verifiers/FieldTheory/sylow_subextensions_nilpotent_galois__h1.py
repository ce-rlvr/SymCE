import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Poly, abc, eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_normal(G, H):
    H_elements = set(H.elements)
    for g in G.elements:
        for h in H.elements:
            if (g * h * ~g) not in H_elements:
                return False
    return True

def normalizer(G, H):
    H_elements = set(H.elements)
    norm_elements = []
    for g in G.elements:
        is_norm = True
        for h in H.elements:
            if (g * h * ~g) not in H_elements:
                is_norm = False
                break
        if is_norm:
            norm_elements.append(g)
    return PermutationGroup(norm_elements)

def is_quotient_nilpotent(N, H):
    L = N.elements
    H_elements = set(H.elements)
    while True:
        next_L_gens = []
        for n in N.elements:
            for l in L:
                c = n * l * ~n * ~l
                if c not in H_elements:
                    next_L_gens.append(c)
        if not next_L_gens:
            return True
        next_L_group = PermutationGroup(next_L_gens + list(H.elements))
        if len(next_L_group.elements) == len(L):
            return False
        L = next_L_group.elements

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The dropped hypothesis is that L/K is a Galois extension.
    """
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, str):
            from sympy import sympify
            witness = sympify(witness.replace('^', '**'))
            
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
            if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
                H_elements = set(H.elements)
                if all(h in G.elements for h in H_elements):
                    N = normalizer(G, H)
                    # Gal(L/K) is interpreted as Aut(L/K) = N_G(H)/H for non-Galois extensions
                    # or the Galois group of the normal closure G is nilpotent.
                    if is_quotient_nilpotent(N, H) or (hasattr(G, 'is_nilpotent') and G.is_nilpotent):
                        h1 = True
                    
                    # L is the compositum of Galois extensions iff H is the intersection of normal subgroups.
                    # Since the compositum of Galois extensions is Galois, H must be normal in G.
                    if not is_normal(G, H):
                        neg_q = True
                    else:
                        if not is_quotient_nilpotent(G, H):
                            neg_q = True
                        else:
                            neg_q = False
                            
        elif isinstance(witness, PermutationGroup):
            G = witness
            if hasattr(G, 'is_nilpotent') and G.is_nilpotent:
                h1 = True
            else:
                id_perm = next(g for g in G.elements if g.is_Identity)
                H = PermutationGroup([id_perm])
                if is_quotient_nilpotent(G, H):
                    h1 = True
            # A single group represents a Galois extension. If it's nilpotent, it IS the compositum.
            neg_q = False
            
        elif isinstance(witness, (Poly, sympy.Expr)):
            f = Poly(witness, abc.x)
            try:
                is_irred = f.is_irreducible
            except Exception:
                is_irred = True
                
            if is_irred:
                if f.degree() == 2:
                    h1 = True
                    neg_q = False
                elif f.degree() == 3:
                    disc = f.discriminant()
                    from sympy import sqrt
                    if sqrt(disc).is_rational:
                        # Galois extension, Aut is Z3 (nilpotent)
                        h1 = True
                        neg_q = False
                    else:
                        # Non-Galois extension, Aut is trivial (nilpotent)
                        h1 = True
                        neg_q = True
                elif f == Poly(abc.x**4 - 2, abc.x):
                    # Non-Galois extension, Aut is Z2 (nilpotent)
                    h1 = True
                    neg_q = True
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The Galois group Gal(L/K) is a nilpotent group",
    "¬Q: L is not the compositum of Galois extensions of prime power degree for distinct primes"
]

N_HYP = 1
NEG_Q_INDEX = 1