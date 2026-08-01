numbers = [20,11,40,20,44,20]
# for i in numbers:
#   if i == 20:
#     numbers.remove(i)

# num = set(numbers)

# print(numbers)


# while 20 in numbers:
#   numbers.remove(20)
# print(numbers)

result = [x for x in numbers if x != 20]
print(result)
