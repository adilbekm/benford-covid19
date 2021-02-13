def apply_benford(ns):
    '''Given a list of non-zero integers, ns, calculates frequency
    of numbers 1, 2, .., 9 in the first digit and returns a list
    of 9 floating point numbers, [f1, f2, .. f9], where
    f1 is the frequency of 1, f2 is the frequency of 2, etc.
    
    If the integer is negative, the negative sign will be ignored.
    If the integer is zero, it will be ingored.
    '''
    ns = [str(abs(n)) for n in ns if n != 0]
    cs = [0 for n in range(9)]
    t = len(ns)
    for n in ns:
        f = int(n[0])
        i = f - 1
        cs[i] += 1
    fs = [float(c) / float(t) for c in cs]
    return fs

