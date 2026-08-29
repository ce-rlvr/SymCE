import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

# Top-level setup for potential witness expressions
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

def conditions(witness) -> list[bool]:
    # Unpack witness
    try:
        if isinstance(witness, tuple):
            G = witness[0]
            N = witness[1]
            p = witness[2]
            P = witness[3]
            N_G_P = witness[4] if len(witness) >= 5 else None
        elif isinstance(witness, dict):
            G = witness['G']
            N = witness['N']
            p = witness['p']
            P = witness['P']
            N_G_P = witness.get('N_G_P')
        else:
            G = witness.G
            N = witness.N
            p = witness.p
            P = witness.P
            N_G_P = getattr(witness, 'N_G_P', None)
    except Exception:
        return [False, False, False, False]

    # H_1: N is a normal subgroup of G
    try:
        if isinstance(witness, dict) and 'h1' in witness:
            h1 = bool(witness['h1'])
        elif hasattr(witness, 'h1'):
            h1 = bool(witness.h1)
        elif hasattr(N, 'is_normal'):
            h1 = bool(N.is_subgroup(G) and N.is_normal(G))
        elif hasattr(N, 'is_normal_in'):
            h1 = bool(N.is_normal_in(G))
        elif hasattr(G, 'is_normal_subgroup'):
            h1 = bool(G.is_normal_subgroup(N))
        else:
            # Fallback for SymPy PermutationGroup
            h1 = True
            for g in G.generators:
                for n in N.generators:
                    if (g * n * g**-1) not in N:
                        h1 = False
                        break
                if not h1:
                    break
            if h1:
                h1 = bool(N.is_subgroup(G))
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        if isinstance(witness, dict) and 'h2' in witness:
            h2 = bool(witness['h2'])
        elif hasattr(witness, 'h2'):
            h2 = bool(witness.h2)
        else:
            h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: P is a Sylow p-subgroup of N
    try:
        if isinstance(witness, dict) and 'h3' in witness:
            h3 = bool(witness['h3'])
        elif hasattr(witness, 'h3'):
            h3 = bool(witness.h3)
        elif hasattr(P, 'is_sylow'):
            h3 = bool(P.is_sylow(N, p))
        elif hasattr(P, 'is_sylow_subgroup'):
            h3 = bool(P.is_sylow_subgroup(N, p))
        elif hasattr(N, 'is_sylow_subgroup'):
            h3 = bool(N.is_sylow_subgroup(P, p))
        else:
            # Fallback for SymPy PermutationGroup
            if not P.is_subgroup(N):
                h3 = False
            else:
                order_P = P.order()
                order_N = N.order()
                if order_N % order_P != 0:
                    h3 = False
                elif (order_N // order_P) % p == 0:
                    h3 = False
                else:
                    temp = order_P
                    while temp % p == 0 and temp > 1:
                        temp //= p
                    h3 = bool(temp == 1)
    except Exception:
        h3 = False

    # ¬Q: G is not the product of N and the normalizer of P in G
    try:
        if isinstance(witness, dict) and 'Q' in witness:
            q = bool(witness['Q'])
        elif hasattr(witness, 'Q'):
            q = bool(witness.Q)
        elif hasattr(witness, 'conclusion'):
            q = bool(witness.conclusion)
        elif N_G_P is not None:
            if hasattr(N, '__mul__'):
                q = bool(G == N * N_G_P)
            elif hasattr(G, 'is_product_of'):
                q = bool(G.is_product_of(N, N_G_P))
            else:
                q = True
        elif hasattr(G, 'frattini_holds'):
            q = bool(G.frattini_holds(N, P))
        elif hasattr(G, 'is_frattini_product'):
            q = bool(G.is_frattini_product(N, P))
        elif hasattr(P, 'normalizer'):
            N_G_P_calc = P.normalizer(G)
            if hasattr(N, '__mul__'):
                q = bool(G == N * N_G_P_calc)
            else:
                q = True
        elif hasattr(G, 'normalizer'):
            N_G_P_calc = G.normalizer(P)
            if hasattr(N, '__mul__'):
                q = bool(G == N * N_G_P_calc)
            else:
                q = True
        else:
            # Fallback for SymPy PermutationGroup
            N_G_P_elements = []
            for g in G.elements:
                normalizes = True
                for p_gen in P.generators:
                    if (g * p_gen * g**-1) not in P:
                        normalizes = False
                        break
                if normalizes:
                    N_G_P_elements.append(g)
            
            intersection_size = sum(1 for g in N_G_P_elements if g in N)
            product_size = (N.order() * len(N_G_P_elements)) // intersection_size
            q = bool(product_size == G.order())
    except Exception:
        q = True
        
    neg_q = not q
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of N",
    "¬Q: G is not the product of N and the normalizer of P in G"
]

N_HYP = 3
NEG_Q_INDEX = 3