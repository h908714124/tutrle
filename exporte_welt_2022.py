import matplotlib.pyplot as plt
import numpy as np

# creating the dataset
data = {
  'China': 3.715827, 
  'USA': 3.011859,
  'DE': 2.060409,
  'FR': 1.005319,
  'UK': 1.001418,
  'Japan': 0.921211,
  'NL': 0.916169,
  'Singapur': 0.870806,
  'Südkorea': 0.820642,
  'Indien': 0.767716,
  'UAE': 0.767716,
  'Italien': 0.767716,
  'Irland': 0.767716,
}

laender = list(data.keys())
werte = list(data.values())
  
fig = plt.figure(figsize = (12, 5))
 
# creating the bar plot
plt.bar(laender, werte, color =['maroon', 'maroon', 'blue', 'maroon','maroon','maroon','maroon','maroon','maroon', 'blue','maroon','maroon','maroon'], 
        width = 0.4)
 
#plt.xlabel("Land")
plt.ylabel("Exorte Gesamt (Billionen USD)")
plt.title("Exporte Gesamt, Waren und Dienstleistungen, 2022")
#plt.show()
plt.savefig('exporte_welt_2022.png')
