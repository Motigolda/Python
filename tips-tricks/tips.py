# 1) Short if else:
# Regular if:
condition = True

if condition:
    x = 1
else:
    x = 0 

# Short if:
x = 1 if condition else 0

# 2) Write big numbers:
x = 1000000000
y = 100000000
# These numbers equals to the next way of writing, but now you can see the difference:
x = 1_000_000_000
y = 100_000_000

print(x) # will print 1000000000, without separation
print(y) # will print 100000000, without separation
# printing with separators:
print(f'{x:,}, {y:,}') # prints 1,000,000,000, 100,000,000

        