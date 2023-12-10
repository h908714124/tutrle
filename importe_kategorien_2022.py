import matplotlib.pyplot as plt
import numpy

labels = ['Dienstleistungen', 'Handelswaren', 'Bergbau und Energie', 'Landwirtschaft','Andere']

merch_total = 720441
agri = numpy.rint(merch_total * 0.67)
manu = numpy.rint(merch_total * 0.477)
fuel = numpy.rint(merch_total * 0.352)
other = numpy.rint(merch_total * 0.104)
serv = 248543

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = numpy.rint((pct * total) / 100)
        return '{:.0f}'.format(val)
    return my_autopct
    
def plot(ax, sizes):
	ax.pie(sizes, labels=labels, autopct=make_autopct(sizes), explode=(0, 0, 0, 0, 0), startangle=90,
	colors=['cornflowerblue', 'gold', 'tomato', 'green', 'gray'])

fig, ax = plt.subplots()
plt.title(label="Importe Indien 2022")
fig.set_size_inches(10, 10)
plot(ax, [serv, manu, fuel, agri, other])
plt.savefig('importe_indien_2022.png')
#plt.show()
