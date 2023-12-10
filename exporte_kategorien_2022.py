import matplotlib.pyplot as plt
import numpy

labels = ['Dienstleistungen', 'Handelswaren', 'Bergbau und Energie', 'Landwirtschaft']

merch_total = 453400
agri = numpy.rint(merch_total * 0.128)
manu = numpy.rint(merch_total * 0.679)
fuel = numpy.rint(merch_total * 0.191)
serv = 308676

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = numpy.rint((pct * total) / 100)
        return '{:.0f}'.format(val)
    return my_autopct
    
def plot(ax, sizes):
	ax.pie(sizes, labels=labels, autopct=make_autopct(sizes), explode=(0.1, 0, 0, 0), shadow=True, startangle=90,
	colors=[
        'cornflowerblue', 'gold', 'tomato', 'green', 
        "#77BFE2"])

fig, ax = plt.subplots()
plt.title(label="Exporte Indien 2022")
fig.set_size_inches(10, 10)
plot(ax, [serv, manu, fuel, agri])
plt.savefig('exporte_indien_2022.png')
#plt.show()
