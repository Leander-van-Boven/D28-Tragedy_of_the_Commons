import collections.abc
import itertools

def update_dict(d, u):
    """Recursively updates dict d with the values of dict u."""
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_dict(d.get(k, {}), v)
        elif isinstance(v, list):
            d[k] = [update_dict(i, j) if not None in (i,j) else \
                    i if j is None else j \
                        for (i,j) in itertools.zip_longest(d.get(k, []), v)]
        else:
            d[k] = v

    return d