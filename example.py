def func(a, b):
    print(a, b)

d = [{'a': 1}, {'b': 2}]
for i in d:
    func(**d)