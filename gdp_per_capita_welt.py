import matplotlib.pyplot as plt
import numpy as np

# creating the dataset
data = {
  'Irland': 96.260,
  'Singapur': 73.850,
  'USA': 70.043 ,
  'NL': 55.575,
  'DE': 48.869 ,
  'UAE': 44.272,
  'UK': 44.028,
  'FR': 42.662,
  'Japan': 37.946,
  'Italien': 33.906,
  'Südkorea': 32.992,
  'China': 11.97, 
  'Indien': 2.177,
}

laender = list(data.keys())
werte = list(data.values())
  
fig = plt.figure(figsize = (12, 5))
 
# creating the bar plot
plt.bar(laender, werte, color =['maroon', 'maroon', 'maroon', 'maroon', 'blue','maroon','maroon','maroon','maroon','maroon','maroon','maroon', 'blue'], 
        width = 0.4)
 
#plt.xlabel("Land")
plt.ylabel("BIP pro Kopf (Tausend USD)")
plt.title("BIP pro Kopf, 2022")
#plt.show()
plt.savefig('gdp_welt_2022.png')
