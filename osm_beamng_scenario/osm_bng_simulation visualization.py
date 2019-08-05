import numpy as np
import matplotlib.pyplot as plt

fig=plt.figure()
ax=fig.add_subplot(1,1,1)
# Plot the points using matplotlib

plt.plot([1,3], [1,3], 'k--')
plt.plot([3,5], [3,2], 'k--')


centreCircle = plt.Circle((3,3),radius= 0.5,color="yellow",fill=False)

#Draw the circles to our plot
ax.add_patch(centreCircle)

plt.scatter(1.5, 1, c='blue', alpha=0.5)
plt.scatter(3.2, 3.2, c='red', alpha=0.5)
plt.scatter(4.5, 2.5, c='green', alpha=0.5)
plt.show()
#fig.savefig('plotcircles2.png')