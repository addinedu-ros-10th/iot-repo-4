import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("test_HX711.csv", sep=" ")

print(data.iloc[:,0])

plt.figure(figsize=(12, 8))
plt.plot(data.index.values, data.iloc[:,0])
plt.grid(True)
plt.legend(["HX711_Output_Data"])
plt.show()
