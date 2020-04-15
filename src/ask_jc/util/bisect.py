def bisect_right_with_key(array, key, key_getter, lo=0, hi=None):
    """Return the index where to insert item x with key_getter(x)=key in list 'array', assuming 'array' is sorted in
     direct order.

    The return value i is such that all e in array[:i] have e <= key, and all e in
    array[i:] have e > key.  So if key already appears in the list, a.insert(x) will
    insert just after the rightmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(array)
    while lo < hi:
        mid = (lo + hi) // 2
        if key < key_getter(array[mid]):
            hi = mid
        else:
            lo = mid + 1
    return lo


def bisect_left_with_key(array, key, key_getter, lo=0, hi=None):
    """Return the index where to insert item x in list a, assuming a is sorted in direct order.

    The return value i is such that all e in a[:i] have e < x, and all e in
    a[i:] have e >= x.  So if x already appears in the list, a.insert(x) will
    insert just before the leftmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(array)
    while lo < hi:
        mid = (lo + hi) // 2
        if key_getter(array[mid]) < key:
            lo = mid + 1
        else:
            hi = mid
    return lo


def reverse_bisect_right_with_key(a, x, key, lo=0, hi=None):
    """Return the index where to insert item x in list a, assuming a is sorted in reverse order.

    The return value i is such that all e in a[:i] have e >= x, and all e in
    a[i:] have e < x.  So if x already appears in the list, a.insert(x) will
    insert just after the rightmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if x > key(a[mid]):
            hi = mid
        else:
            lo = mid + 1
    return lo


def reverse_bisect_left_with_key(a, x, key, lo=0, hi=None):
    """Return the index where to insert item x in list a, assuming a is sorted in reverse order.

    The return value i is such that all e in a[:i] have e > x, and all e in
    a[i:] have e <= x.  So if x already appears in the list, a.insert(x) will
    insert just before the leftmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if key(a[mid]) > x:
            lo = mid + 1
        else:
            hi = mid
    return lo
