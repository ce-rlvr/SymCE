import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup for potential witness objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein 4-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def evaluate(f, x):
    if callable(f):
        return f(x)
    elif isinstance(f, dict):
        return f[x]
    else:
        return f(x)

def get_array(p, size):
    arr = p.array_form
    if len(arr) < size:
        arr = arr + list(range(len(arr), size))
    return arr

def direct_product(G1, G2):
    n1 = G1.degree
    n2 = G2.degree
    gens = []
    for g in G1.generators:
        arr = get_array(g, n1) + list(range(n1, n1 + n2))
        gens.append(Permutation(arr))
    for g in G2.generators:
        arr = list(range(n1)) + [x + n1 for x in get_array(g, n2)]
        gens.append(Permutation(arr))
    if not gens:
        gens.append(Permutation(list(range(n1 + n2))))
    return PermutationGroup(gens)

def pi1_func(p, n1, n2):
    arr = get_array(p, n1 + n2)
    return Permutation(arr[:n1])

def pi2_func(p, n1, n2):
    arr = get_array(p, n1 + n2)
    return Permutation([x - n1 for x in arr[n1:n1+n2]])

def is_homomorphism(G, H, f):
    try:
        elements = list(G.elements)
        for g in elements:
            val = evaluate(f, g)
            if not H.contains(val):
                return False
        for g1 in elements:
            for g2 in elements:
                if evaluate(f, g1 * g2) != evaluate(f, g1) * evaluate(f, g2):
                    return False
        return True
    except Exception:
        return False

def is_homomorphism_dict(G, H, f_dict):
    elements = list(G.elements)
    for g1 in elements:
        for g2 in elements:
            if f_dict[g1 * g2] != f_dict[g1] * f_dict[g2]:
                return False
    return True

def conditions(witness):
    try:
        K = witness['K']
        G1 = witness['G1']
        G2 = witness['G2']
        f1 = witness['f1']
        f2 = witness['f2']
    except Exception:
        return [False, False, False, False]
        
    is_standard = False
    if 'G1xG2' in witness:
        G1xG2 = witness['G1xG2']
        pi1 = witness['pi1']
        pi2 = witness['pi2']
    else:
        try:
            G1xG2 = direct_product(G1, G2)
            n1 = G1.degree
            n2 = G2.degree
            pi1 = lambda p: pi1_func(p, n1, n2)
            pi2 = lambda p: pi2_func(p, n1, n2)
            is_standard = True
        except Exception:
            return [False, False, False, False]

    # H1: f1 is a group homomorphism from K to G1
    h1_ok = is_homomorphism(K, G1, f1)
    
    # H2: f2 is a group homomorphism from K to G2
    h2_ok = is_homomorphism(K, G2, f2)
    
    # H3: pi1 and pi2 are the canonical projection homomorphisms
    if is_standard:
        h3_ok = True
    else:
        h3_ok = is_homomorphism(G1xG2, G1, pi1) and is_homomorphism(G1xG2, G2, pi2)
        
    # neg_Q: It is NOT the case that there exists a unique group homomorphism f: K -> G1xG2 
    # such that pi1(f(k)) == f1(k) and pi2(f(k)) == f2(k)
    neg_q_ok = False
    try:
        elements_K = list(K.elements)
        if is_standard:
            n1 = G1.degree
            n2 = G2.degree
            f_dict = {}
            for k in elements_K:
                v1 = evaluate(f1, k)
                v2 = evaluate(f2, k)
                arr1 = get_array(v1, n1)
                arr2 = get_array(v2, n2)
                arr = arr1 + [x + n1 for x in arr2]
                y = Permutation(arr)
                f_dict[k] = y
            if is_homomorphism_dict(K, G1xG2, f_dict):
                neg_q_ok = False
            else:
                neg_q_ok = True
        else:
            valid_y = {}
            possible = True
            for k in elements_K:
                v1 = evaluate(f1, k)
                v2 = evaluate(f2, k)
                valid = []
                for y in G1xG2.elements:
                    if evaluate(pi1, y) == v1 and evaluate(pi2, y) == v2:
                        valid.append(y)
                if not valid:
                    possible = False
                    break
                valid_y[k] = valid
                
            if not possible:
                neg_q_ok = True
            else:
                keys = elements_K
                lists = [valid_y[k] for k in keys]
                hom_count = 0
                for combo in itertools.product(*lists):
                    f_dict = dict(zip(keys, combo))
                    if is_homomorphism_dict(K, G1xG2, f_dict):
                        hom_count += 1
                        if hom_count > 1:
                            break
                neg_q_ok = (hom_count != 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f_1: K -> G_1 is a group homomorphism",
    "H_2: f_2: K -> G_2 is a group homomorphism",
    "H_3: pi_1 and pi_2 are the canonical projection homomorphisms",
    "¬Q: There does not exist a unique group homomorphism f: K -> G_1 x G_2 such that pi_1 o f = f_1 and pi_2 o f = f_2"
]

N_HYP = 3
NEG_Q_INDEX = 3