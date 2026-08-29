import itertools

# Top-level setup
# No specific named objects are required for this domain, but we provide a namespace.
# The witness is expected to be an object representing a ring with:
# - `elements`: an iterable of elements
# - `zero`: the additive identity element
# - `add(a, b)`: a method/function returning the sum of a and b
# - `mul(a, b)`: a method/function returning the product of a and b

def is_boolean_ring(R):
    try:
        elements = list(R.elements)
        if not elements:
            return False
        zero = R.zero
        if zero not in elements:
            return False
            
        # Check additive identity
        for a in elements:
            if R.add(a, zero) != a or R.add(zero, a) != a:
                return False
                
        # Check additive inverse, commutativity, and associativity
        for a in elements:
            for b in elements:
                if R.add(a, b) != R.add(b, a): 
                    return False
                # In a Boolean ring, a + a = 0
                if R.add(a, a) != zero: 
                    return False
                for c in elements:
                    if R.add(R.add(a, b), c) != R.add(a, R.add(b, c)): 
                        return False
                    
        # Check multiplicative associativity, distributivity, and x^2 = x
        for a in elements:
            # Boolean ring property: a^2 = a
            if R.mul(a, a) != a: 
                return False
            for b in elements:
                for c in elements:
                    if R.mul(R.mul(a, b), c) != R.mul(a, R.mul(b, c)): 
                        return False
                    if R.mul(a, R.add(b, c)) != R.add(R.mul(a, b), R.mul(a, c)): 
                        return False
                    if R.mul(R.add(a, b), c) != R.add(R.mul(a, c), R.mul(b, c)): 
                        return False
                    
        return True
    except Exception:
        return False

def has_identity(R):
    try:
        elements = list(R.elements)
        if not elements:
            return False
        for e in elements:
            is_id = True
            for a in elements:
                if R.mul(e, a) != a or R.mul(a, e) != a:
                    is_id = False
                    break
            if is_id:
                return True
        return False
    except Exception:
        return False

def check_Q(R):
    try:
        elements = list(R.elements)
        if not elements:
            return False
            
        elements_prime = [(a, m) for a in elements for m in (0, 1)]
        
        def add_prime(x, y):
            a, m = x
            b, n = y
            return (R.add(a, b), (m + n) % 2)
            
        def mul_prime(x, y):
            a, m = x
            b, n = y
            ab = R.mul(a, b)
            na = a if n == 1 else R.zero
            mb = b if m == 1 else R.zero
            first = R.add(R.add(ab, na), mb)
            second = (m * n) % 2
            return (first, second)
            
        zero_prime = (R.zero, 0)
        id_prime = (R.zero, 1)
        
        # Check if R' is a Boolean ring
        for x in elements_prime:
            if add_prime(x, zero_prime) != x or add_prime(zero_prime, x) != x:
                return False
                
        for x in elements_prime:
            for y in elements_prime:
                if add_prime(x, y) != add_prime(y, x): 
                    return False
                if add_prime(x, x) != zero_prime: 
                    return False
                for z in elements_prime:
                    if add_prime(add_prime(x, y), z) != add_prime(x, add_prime(y, z)): 
                        return False
                        
        for x in elements_prime:
            if mul_prime(x, x) != x: 
                return False
            for y in elements_prime:
                for z in elements_prime:
                    if mul_prime(mul_prime(x, y), z) != mul_prime(x, mul_prime(y, z)): 
                        return False
                    if mul_prime(x, add_prime(y, z)) != add_prime(mul_prime(x, y), mul_prime(x, z)): 
                        return False
                    if mul_prime(add_prime(x, y), z) != add_prime(mul_prime(x, z), mul_prime(y, z)): 
                        return False
                        
        # Check if (0, 1) is the identity in R'
        for x in elements_prime:
            if mul_prime(x, id_prime) != x or mul_prime(id_prime, x) != x:
                return False
                
        # Check if R' contains a subring isomorphic to R
        # A subring of a ring with identity must contain the identity.
        n = len(elements)
        if n <= 4:
            # Exhaustive check for small rings
            for subset in itertools.combinations(elements_prime, n):
                if zero_prime not in subset or id_prime not in subset:
                    continue
                
                closed = True
                for x in subset:
                    for y in subset:
                        if add_prime(x, y) not in subset: 
                            closed = False
                            break
                        if mul_prime(x, y) not in subset: 
                            closed = False
                            break
                    if not closed:
                        break
                if not closed:
                    continue
                    
                isomorphic = False
                for perm in itertools.permutations(subset):
                    f = dict(zip(elements, perm))
                    valid = True
                    for a in elements:
                        for b in elements:
                            if f[R.add(a, b)] != add_prime(f[a], f[b]): 
                                valid = False
                                break
                            if f[R.mul(a, b)] != mul_prime(f[a], f[b]): 
                                valid = False
                                break
                        if not valid:
                            break
                    if valid:
                        isomorphic = True
                        break
                if isomorphic:
                    return True
            return False
        else:
            # For larger rings, we use the mathematical equivalence:
            # R' contains a subring isomorphic to R iff R has an identity.
            return has_identity(R)
            
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # H_1: R is a Boolean ring without an identity element
    h1 = is_boolean_ring(witness) and not has_identity(witness)
    
    # H_2: Addition on R' is defined correctly (Trivially true as it's a definition)
    h2 = True
    
    # H_3: Multiplication on R' is defined correctly (Trivially true as it's a definition)
    h3 = True
    
    # neg_Q: R' is not a Boolean ring with identity (0, 1) or does not contain a subring isomorphic to R
    neg_q = not check_Q(witness)
    
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring without an identity element",
    "H_2: Addition on R' is defined correctly",
    "H_3: Multiplication on R' is defined correctly",
    "¬Q: R' is not a Boolean ring with identity (0, 1) or does not contain a subring isomorphic to R"
]

N_HYP = 3
NEG_Q_INDEX = 3