import matplotlib.pyplot as plt
import numpy as np

# Create the data
x = np.array(["Speed", "Cost", "Availability", "Power efficiency"])
y_GaAs = np.array([1.1, 1.2, 0.9, 0.8])
y_Silicon = np.array([1, 0.8, 1.1, 1])

# Create the bar graph
plt.bar(x, y_Silicon, label="GaAs", bottom=y_GaAs)
plt.bar(x, y_GaAs, label="Silicon", alpha = 0.8 )
plt.xlabel("Feature")
plt.ylabel("Relative difference")
plt.legend()

# Show the bar graph
plt.show()
