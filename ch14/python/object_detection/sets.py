from collections import Counter
items = ['2', '2', '2', 'c', 'd', 'd', 'd', 'c', 'a', 'b']
counts = Counter(items)
for c in counts:
    print(c,counts[c])
print(counts)
print(counts['a'])