import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    """
    Checks the hypotheses and negated conclusion for the false conjecture about the
    Universal Property of the Semidirect Product.
    
    The witness is expected to be a tuple: (N, H, phi, K, f, g)
    where:
      - N, H, K are lists of elements (representing groups)
      - phi is a function: H -> (function: N -> N)
      - f is a function: N -> K
      - g is a function: H -> K
    """
    try:
        N, H, phi, K, f, g = witness
    except Exception:
        return [False] * 5 + [False]

    def get_identity(G):
        for e in G:
            if all(e * x == x and x * e == x for x in G):
                return e
        return None

    def get_inverse(G, x, id_G):
        for y in G:
            if x * y == id_G and y * x == id_G:
                return y
        return None

    def is_group(G):
        if not G: return False
        id_G = get_identity(G)
        if id_G is None: return False
        for a in G:
            inv_a = get_inverse(G, a, id_G)
            if inv_a is None: return False
            for b in G:
                if a * b not in G: return False
        return True

    # H1: N and H are groups and phi: H -> Aut(N) is a homomorphism
    try:
        h1_ok = is_group(N) and is_group(H)
        if h1_ok:
            for h in H:
                img = [phi(h)(n) for n in N]
                has_duplicates = False
                for i in range(len(img)):
                    for j in range(i + 1, len(img)):
                        if img[i] == img[j]:
                            has_duplicates = True
                            break
                    if has_duplicates: break
                if has_duplicates or any(x not in N for x in img):
                    h1_ok = False
                
                for n1 in N:
                    for n2 in N:
                        if phi(h)(n1 * n2) != phi(h)(n1) * phi(h)(n2):
                            h1_ok = False
            
            for h1 in H:
                for h2 in H:
                    for n in N:
                        if phi(h1 * h2)(n) != phi(h1)(phi(h2)(n)):
                            h1_ok = False
    except Exception:
        h1_ok = False

    # H2: G = N \rtimes_\phi H is the external semidirect product
    # This is definitional, we just check if we can form it.
    try:
        h2_ok = True
    except Exception:
        h2_ok = False

    # H3: K is a group
    try:
        h3_ok = is_group(K)
    except Exception:
        h3_ok = False

    # H4: f: N -> K and g: H -> K are group homomorphisms
    try:
        h4_ok = True
        for n1 in N:
            for n2 in N:
                if f(n1 * n2) != f(n1) * f(n2):
                    h4_ok = False
        for h1 in H:
            for h2 in H:
                if g(h1 * h2) != g(h1) * g(h2):
                    h4_ok = False
    except Exception:
        h4_ok = False

    # H5: f(phi_h(n)) = g(h) f(n) g(h)^{-1} for all n in N and h in H
    try:
        h5_ok = True
        id_K = get_identity(K)
        for n in N:
            for h in H:
                inv_gh = get_inverse(K, g(h), id_K)
                if f(phi(h)(n)) != g(h) * f(n) * inv_gh:
                    h5_ok = False
    except Exception:
        h5_ok = False

    # neg_Q: The conclusion FAILS
    try:
        # Any homomorphism Phi satisfying the conditions must be given by Phi((n, h)) = f(n) * g(h)
        def Phi(n, h):
            return f(n) * g(h)

        is_hom = True
        for n1 in N:
            for h1 in H:
                for n2 in N:
                    for h2 in H:
                        n_res = n1 * phi(h1)(n2)
                        h_res = h1 * h2
                        if Phi(n_res, h_res) != Phi(n1, h1) * Phi(n2, h2):
                            is_hom = False
                            break
                    if not is_hom: break
                if not is_hom: break
            if not is_hom: break
        
        neg_q_ok = not is_hom
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, h5_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N and H are groups and phi: H -> Aut(N) is a homomorphism",
    "H_2: G = N \\rtimes_\\phi H is the external semidirect product",
    "H_3: K is a group",
    "H_4: f: N -> K and g: H -> K are group homomorphisms",
    "H_5: f(phi_h(n)) = g(h) f(n) g(h)^{-1} for all n in N and h in H",
    "¬Q: There does not exist a unique group homomorphism Phi: G -> K satisfying the conditions"
]

N_HYP = 5
NEG_Q_INDEX = 5