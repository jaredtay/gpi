# This is a simple script to highlight the features of this platform
#! <--- This flag will turn the color of a comment blue
# Use it to highlight special comments
import numpy as np
import matplotlib.pyplot as plt

#! Assignment Statements
a = 5
b = 12
c = (5**2 + 12**2)**0.5

#! Good input appears with green background
#! Bad input appears with red background
# Bad input here is defined as that which fails to be parsed by redbaron, a python package for manipulating
# abstract syntax trees. This means that a line of code such as this...
d = undefined_variable
# ... will be judged to be good input, but will obviously fail when run because 'undefined_variable' hasn't been
# defined yet.

# Plotting Sine and Cosine
begin = 0
end = 4*np.pi
N = 100

#! Function Calls
# Function calls have input and output spaces
# The title is the name of the function being called
# Hover over the title to see the code that generated it
T = np.linspace(begin, end, N)
S = np.sin(T)
C = np.cos(T)

fig = plt.figure(1)
ax = fig.add_subplot(111)

# Function calls with keyword arguments like ``label='Sine Wave'`` will be set apart
# To edit the raw code, right-click the line number on the left and select 'Raw'
ax.plot(T,S,'b',label='Sine Wave')
ax.plot(T,C,'r',label='Cosine Wave')

# Function calls without inputs or outputs
plt.show()

#! For loops:
sum = 0
ones = np.zeros(T.shape)
for i in range(len(T)):
   # Code within the for loop
   sum += T[i]
   ones[i] = S[i]**2 + C[i]**2

print(sum)
print(ones)
