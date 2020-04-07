import copy

b = {
    "B1": 2,
    "B2": (12, 23),
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

print(b)
c = copy.deepcopy(b)
print(c)
# c["B2"].append(231231)
print(id(b["B2"]))
print(id(c["B2"]))
print(c)
