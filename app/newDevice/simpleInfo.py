b = {
    "B1": 2,
    "B2": 3,
}
old = {
    "A": 1,
    "B": b,
    "C": 4
}

new = {
    "A": 2,
    "B": {
        "B1": 3,
        "B2": 4,
    },
    "C": 5
}

old.update(new)
print(old)
print(b)
