import sympy
from sympy import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

def parse_witness(witness):
    """
    Parses the witness into a modulus n (where n=0 means Z, n>0 means Z_n)
    and a list of integer elements B.
    Accepts either a tuple (n, B) or just a list B.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R_obj, B_obj = witness
            n = 0
            if isinstance(R_obj, int):
                n = R_obj
            B = []
            for x in B_obj:
                if isinstance(x, (int, float)) and x == int(x):
                    B.append(int(x))
                elif hasattr(x, 'is_integer') and x.is_integer:
                    B.append(int(x))
                else:
                    return None, None
            B = list(set(B))
            if n > 0:
                B = list(set([x % n for x in B]))
            return n, B
        else:
            B = []
            for x in witness:
                if isinstance(x, (int, float)) and x == int(x):
                    B.append(int(x))
                elif hasattr(x, 'is_integer') and x.is_integer:
                    B.append(int(x))
                else:
                    return None, None
            B = list(set(B))
            return 0, B
    except Exception:
        return None, None

def conditions(witness) -> list[bool]:
    n, B = parse_witness(witness)
    
    # If parsing failed, or B is empty, or B is too large to test quickly
    if B is None or len(B) == 0 or len(B) > 100:
        return [False, False, False, False]
    
    # H1: R is a commutative ring with identity. 
    # (Z and Z_n are always commutative rings with identity)
    H1 = True
    
    # H2: Addition on B is defined as x (+) y = x + y - 2xy
    H2 = True
    
    # H3: Multiplication on B is the standard multiplication inherited from R
    H3 = True
    
    def add(x, y):
        res = x + y - 2 * x * y
        return res % n if n > 0 else res

    def mul(x, y):
        res = x * y
        return res % n if n > 0 else res

    is_boolean_ring = True
    
    try:
        # 1. Closure under (+)
        for x in B:
            for y in B:
                if add(x, y) not in B:
                    is_boolean_ring = False
                    break
            if not is_boolean_ring: break
            
        # 2. Closure under (*)
        if is_boolean_ring:
            for x in B:
                for y in B:
                    if mul(x, y) not in B:
                        is_boolean_ring = False
                        break
                if not is_boolean_ring: break
                
        # 3. Identity for (+)
        if is_boolean_ring:
            has_identity = False
            identity = None
            for e in B:
                is_id = True
                for x in B:
                    if add(x, e) != x or add(e, x) != x:
                        is_id = False
                        break
                if is_id:
                    has_identity = True
                    identity = e
                    break
            if not has_identity:
                is_boolean_ring = False
                
        # 4. Inverses for (+)
        if is_boolean_ring:
            for x in B:
                has_inv = False
                for y in B:
                    if add(x, y) == identity and add(y, x) == identity:
                        has_inv = True
                        break
                if not has_inv:
                    is_boolean_ring = False
                    break
                    
        # 5. Idempotence (x * x == x for all x in B)
        # This is the defining property of a Boolean ring
        if is_boolean_ring:
            for x in B:
                if mul(x, x) != x:
                    is_boolean_ring = False
                    break
                    
        # 6. Associativity and Distributivity
        if is_boolean_ring:
            for x in B:
                for y in B:
                    for z in B:
                        if add(add(x, y), z) != add(x, add(y, z)):
                            is_boolean_ring = False
                        if mul(mul(x, y), z) != mul(x, mul(y, z)):
                            is_boolean_ring = False
                        if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)):
                            is_boolean_ring = False
                        if mul(add(y, z), x) != add(mul(y, x), mul(z, x)):
                            is_boolean_ring = False
                        if not is_boolean_ring: break
                    if not is_boolean_ring: break
                if not is_boolean_ring: break
                
    except Exception:
        is_boolean_ring = False

    # The conclusion is that B forms a Boolean ring.
    # We want the conclusion to FAIL at the witness.
    neg_Q = not is_boolean_ring
    
    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: Addition on B is defined as x (+) y = x + y - 2xy",
    "H_3: Multiplication on B is the standard multiplication inherited from R",
    "¬Q: B does not form a Boolean ring under (+) and standard multiplication"
]

N_HYP = 3
NEG_Q_INDEX = 3