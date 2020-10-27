import collections.abc
import itertools

def update_dict(d, u, omit_new=False):
    """Recursively updates dict d with the values of dict u, 
    and returns d.

    Parameters
    ----------
    d : `dict`,
        The base dictionary that will be updated. 

    u : `dict`,
        The update dictionary that will update d.

    omit_new : `bool`, optional,
        If True, values that occur in u but not in d will be omitted and 
        thus not added to d. If False (default), new values will be
        added to d. 
    """
    
    for k, v in u.items():
        if k not in d and omit_new: 
            continue

        if isinstance(v, collections.abc.Mapping):
            d[k] = update_dict(d.get(k, {}), v, omit_new)
        elif isinstance(v, list):
            d[k] = [update_dict(i, j, omit_new) if not None in (i,j) else \
                    i if j is None else j \
                        for (i,j) in itertools.zip_longest(d.get(k, []), v)]
        else:
            d[k] = v
    return d