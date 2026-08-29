import itertools
import math
import functools
from sympy import Matrix
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_Sn(k):
    elements = list(itertools.permutations(range(k)))
    def multiply(p1, p2):
        return tuple(p1[p2[i]] for i in range(k))
    def inverse(p):
        res = [0] * k
        for i, v in enumerate(p):
            res[v] = i
        return tuple(res)
    return elements, multiply, inverse

def get_A4():
    elements, multiply, inverse = get_Sn(4)
    def is_even(p):
        transpositions = 0
        visited = [False] * 4
        for i in range(4):
            if not visited[i]:
                length = 0
                curr = i
                while not visited[curr]:
                    visited[curr] = True
                    curr = p[curr]
                    length += 1
                transpositions += length - 1
        return transpositions % 2 == 0
    a4_elements = [p for p in elements if is_even(p)]
    return a4_elements, multiply, inverse

def count_homs(n, rels, elements, multiply, inverse):
    count = 0
    identity = elements[0]
    for mapping in itertools.product(elements, repeat=n):
        valid = True
        for rel in rels:
            val = identity
            for x in rel:
                if x > 0:
                    val = multiply(val, mapping[x-1])
                elif x < 0:
                    val = multiply(val, inverse(mapping[-x-1]))
            if val != identity:
                valid = False
                break
        if valid:
            count += 1
    return count

def parse_witness(witness):
    """
    Parses the witness into a tuple (n, rels) where n is the number of generators
    and rels is a list of relations (each relation is a list of non-zero integers).
    Supports both a raw tuple format and SymPy FpGroup objects.
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        n, rels = witness
        if isinstance(n, int) and isinstance(rels, list):
            if n > 10 or len(rels) > 20:
                return None
            valid = True
            for rel in rels:
                if not isinstance(rel, list):
                    valid = False
                    break
                for x in rel:
                    if not isinstance(x, int) or x == 0 or abs(x) > n:
                        valid = False
                        break
            if valid:
                return n, rels

    try:
        gens = list(witness.generators)
        relators = list(witness.relators)
        n = len(gens)
        if n > 10 or len(relators) > 20:
            return None
            
        rels = []
        for rel in relators:
            word = []
            for g, p in rel.array_form:
                base_idx = None
                for i, gen in enumerate(gens):
                    if g == gen:
                        base_idx = i + 1
                        break
                if base_idx is None:
                    return None
                if p > 0:
                    word.extend([base_idx] * p)
                else:
                    word.extend([-base_idx] * (-p))
            rels.append(word)
        return n, rels
    except Exception:
        pass
        
    return None

def is_abelianization_Z(n, rels):
    M = Matrix(max(len(rels), n), n, lambda i, j: 0)
    for i, rel in enumerate(rels):
        for x in rel:
            if x > 0:
                M[i, x-1] += 1
            elif x < 0:
                M[i, -x-1] -= 1
                
    if n == 1:
        return all(M[i, 0] == 0 for i in range(M.rows))
        
    for row_indices in itertools.combinations(range(M.rows), n):
        subM = M.extract(row_indices, range(n))
        if subM.det() != 0:
            return False
            
    minors_gcd = 0
    for row_indices in itertools.combinations(range(M.rows), n - 1):
        for col_indices in itertools.combinations(range(n), n - 1):
            subM = M.extract(row_indices, col_indices)
            det = abs(int(subM.det()))
            minors_gcd = math.gcd(minors_gcd, det)
            if minors_gcd == 1:
                return True
                
    return minors_gcd == 1

def is_not_trefoil(n, rels):
    s3_elements, s3_mul, s3_inv = get_Sn(3)
    if count_homs(n, rels, s3_elements, s3_mul, s3_inv) != 12:
        return True
        
    a4_elements, a4_mul, a4_inv = get_A4()
    if count_homs(n, rels, a4_elements, a4_mul, a4_inv) != 36:
        return True
        
    if n <= 4:
        s4_elements, s4_mul, s4_inv = get_Sn(4)
        if count_homs(n, rels, s4_elements, s4_mul, s4_inv) != 96:
            return True
            
    if n <= 3:
        s5_elements, s5_mul, s5_inv = get_Sn(5)
        if count_homs(n, rels, s5_elements, s5_mul, s5_inv) != 600:
            return True
            
    return False

def conditions(witness):
    parsed = parse_witness(witness)
    
    try:
        if parsed is None:
            h1_ok = False
        else:
            n, rels = parsed
            h1_ok = is_abelianization_Z(n, rels)
    except Exception:
        h1_ok = False

    try:
        if parsed is None:
            neg_q_ok = False
        else:
            n, rels = parsed
            neg_q_ok = is_not_trefoil(n, rels)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is the knot group of K (abelianization is Z)",
    "¬Q: G does not admit the presentation < x, y | x^2 = y^3 >"
]

N_HYP = 1
NEG_Q_INDEX = 1