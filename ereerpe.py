def find_middle(lst):
  if len(lst) == 1: return None
  s = k = b = 0
  for p in lst: s += p
  s /= 2
  for p in range(len(lst)):
    k += lst[p]
    if k == s: return p
    elif k > s:
      j = len(lst) - 1
      while b < s:
        b += lst[j]
        j -= 1
      return p if abs(s - k) < abs(s - b) else j
  return

def shannon(iterable):
  print("***")
  rv = None
  if len(iterable) == 1: return rv
  half = round(sum(iterable) / 2)
  print("h:", half)
  print("I: ", iterable)
  group1=group2=0
  diff1=diff2=diff3=0
  for index in range(len(iterable)-2):
    group1 = iterable[:index+1]
    group2 = iterable[:index+2]
    sum1 = sum(group1)
    sum2 = sum(group2)
    diff1 = (sum1 - half)
    diff2 = (sum2 - half)
    print("g:", group1, group2)
    print(sum1, sum2)
    print("d:", diff1, diff2, diff3)
    print("-------------------")
    if sum1 >= half:
      break

    rv = (group1, group2)
  if rv:
    cero=shannon(group1)
    uno=shannon(group2)
    print()

  return rv
    



print('Hello, world!')

l = [1/2, 1/4, 1/8, 1/16, 1/32, 1/64, 1/64]
anita = [6/15, 2/15, 2/15, 2/15, 2/15, 1/15]
anita2 = [6, 2, 2, 2, 2, 1]

#print(sum(anita2))
print(shannon(anita2))
