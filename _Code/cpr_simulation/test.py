def test():
    a = {
        "a" : 1,
        "b" : {
            "ba" : 1,
            "bb" : 1,
        },
        "c" : 1,
    }

    b = {
        "a" : 0,
        "b" : {
            "ba" : 0,
        },
        "d" : 0
    }

    a.update(b)
    return a

