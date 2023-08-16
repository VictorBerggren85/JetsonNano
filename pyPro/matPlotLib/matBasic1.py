import matplotlib.pyplot as plt
import numpy as np

x=np.arange(-4,4,.1)
y=np.square(x)
z=np.square(x)-5
w=np.square(x+2)
np.
#z=np.range(-4,4,.1)

plt.grid(True)
plt.xlabel("X")
plt.ylabel("Y & Z & W & M")
plt.title("MyGraph")
#plt.axis([0,75, 0, 70])
plt.plot(x,y, 'm-o', linewidth=3, markersize=8, label="X-line")
plt.plot(x,z, 'g-o', linewidth=3, markersize=8, label="Z-line")
plt.plot(x,w, 'r-o', linewidth=3, markersize=8, label="W-line")
plt.legend(loc='upper center')
plt.show()