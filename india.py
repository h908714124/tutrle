import matplotlib.pyplot as plt
import numpy

labels = ['Waren', 'Dienstleistungen']

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = numpy.rint((pct * total) / 100)
        return '{:.0f}'.format(val)
    return my_autopct
    
def plot(ax, sizes):
	ax.pie(sizes, labels=labels, autopct=make_autopct(sizes))

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.set_size_inches(10, 6)
ax1.legend(title="Indien 2022")
ax2.legend(title="Deutschland 2022")
plot(ax1, [453400, 308676])
plot(ax2, [1657577, 406202])
#plt.savefig('exporte_indien_deutschland_2022.png')
plt.show()
