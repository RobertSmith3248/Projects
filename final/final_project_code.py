#Final project, Robert Smith, BCH5884
#repository: https://github.com/RobertSmith3248/Projects

import sys
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
#import the necessary libraries

a = input("This program will read in a list of chemical shifts in the NMR spectrum of 1-butene (obtained from NMR prediction software in ChemDraw) from a txt file and return a plot of the chemical shifts for the primary vinyl carbon and its attached hydrogens as 25 functional groups are interchanged. Press Enter/Return to continue.")
#introduction describing the program, where the data comes from, and the general output before generating the html file

data = pd.read_csv("chemical_shifts.txt", sep = ',')
#read in the txt file
#read_csv() works the same for both csv and txt files

x = 'Designation'
y = 'Hydrogen (ppm)'
z = 'Carbon (ppm)'
#define the variables for plotting later

h_parent = 5.13
c_parent = 113.3
#chemical shifts of the parent molecule

#calculate the means and standard deviations
hdata_mean = round(data['Hydrogen (ppm)'].mean(), 2)
#mean shift for hydrogen rounded to 2 decimal places
hsd = round(data['Hydrogen (ppm)'].std(), 2)
#standard deviation of hydrogen chemical shifts rounded to 2 decimal places
#print("The mean chemical shift for hydrogen is", hdata_mean, "ppm with a standard deviation of", hsd, "ppm.")

cdata_mean = round(data['Carbon (ppm)'].mean(), 2)
#mean shift for carbon rounded to 2 decimal places
csd = round(data['Carbon (ppm)'].std(), 2)
#standard deviation of carbon chemical shifts rounded to 2 decimal places
#print("The mean chemical shift for carbon is", cdata_mean, "ppm with a standard deviation of", csd, "ppm.")

#calculate the max and min values
hmax = data['Hydrogen (ppm)'].max()
#max shift for hydrogen
hmaxr = '{:04.2f}'.format(hmax)
#only display 6.9 if rounded using round() normally, so use hmaxr
#the :04 tells it to display 4 characters, .2 says to round to 2 decimal places, f says to return a float
hmin = data['Hydrogen (ppm)'].min()
#min shift for hydrogen

cmax = data['Carbon (ppm)'].max()
#max shift for carbon
cmin = data['Carbon (ppm)'].min()
#min shift for carbon

data['Deviation from Hydrogen Parent Shifts (ppm)'] = data['Hydrogen (ppm)'] - h_parent
data['Deviation from Carbon Parent Shifts (ppm)'] = data['Carbon (ppm)'] - c_parent
#subtract every value in the table from the chemical shifts of 1-butene and add them to the original dataframe with the assigned column title

sdata = {' ': ['Mean Shift', 'Standard Deviation', 'Largest Shift', 'Smallest Shift'],
        'Hydrogen (ppm)': [hdata_mean, hsd, hmaxr, hmin],
        'Carbon (ppm)': [cdata_mean, csd, cmax, cmin]
}
#compile all of the statistics into a table

df = pd.DataFrame(sdata, columns = [' ', 'Hydrogen (ppm)', 'Carbon (ppm)'])
#convert sdata into a pandas dataframe and define the columns

#function to apply to both sets of shifts
def shift_graph(data, ymin, ymax, ystep, shift, parent, title, fn):
    #define the function and note all of the values that will be changing
    ax = data.plot(x, shift, marker = 'o')
    #plot the data and mark the points with a circle
    #shift refers to either hydrogen (y) or carbon (z)
    ax.axhline(y = parent, color = 'k')
    #add a black horizontal line at the parent coordinate
    #parent refers to the parent molecule's chemical shift, defined above as h_parent and c_parent
    ax.get_legend().remove()
    #remove the legend that appears by default
    ax.grid(b = True, which = 'major', color = '#ABB2B9', linestyle = '-')
    #add major gridlines to the figure and format them with color and linestyle
    ax.set_xticks(np.arange(0, 26))
    #set the interval for the x-axis tick marks (doesn't change)
    ax.set_xticklabels(data[x])
    #each tick has a label as opposed to just every 6th tick having a label by default
    ax.set_xlabel("Substituent")
    #x-axis label (doesn't change)
    ax.set_yticks(np.arange(ymin, ymax, ystep))
    #y-axis ranges from ymin to ymax with intervals of ystep
    ax.set_ylabel("Chemical Shift (ppm)")
    #y-axis label (doesn't change)
    ax.set_title(title)
    #figure title
    fig = ax.get_figure()
    fig.savefig(fn)
    #save figure as filename, fn

shift_graph(data, 4, 7, 0.20, y, h_parent, "Hydrogen Chemical Shifts of 1-Butene", "hydrogen_shifts.png")
shift_graph(data, 80, 180, 10, z, c_parent, "Carbon Chemical Shifts of 1-Butene", "carbon_shifts.png")
#input the necessary values and call the function for both sets of shifts

#open and write to an html file
f = open("final_project_website.html", 'w')

#html code
f.write("<html>")
f.write("<title> NMR Analysis of 1-Butene </title>")
#title website
f.write("<h1> NMR Analysis of 1-Butene </h1>")
#header to title the page
f.write("<img src = '1_butene.png'><br>")
#insert the image 1_butene.png and start a new line
f.write("<body>")
#start body
f.write("<p style = 'font-size:20px'>")
#start paragraph with a font size of 20px
f.write("The purpose of this program is to examine the change in chemical shift as substituents of differing polarity and composition (denoted A-Z in the table below) are added to 1-butene (above). The chemical shifts that will be examined are of the primary vinyl carbon and its attached hydrogen (shown explicitly above). These chemical shifts are then graphed against the chemical shifts of the molecule with no substituents as a baseline, which is called the parent molecule in the table below. It is represented in each graph by a horizontal black line to make the comparisons easier to visualize, and the numerical deviations are also shown in the table along with the original shift values. The overall goal of the program is to provide a visual representation of shielding and deshielding effects and to show how changes in polarity, size, and degrees of unsaturation of substituents can affect the chemical shifts of the other atoms in the molecule.")
#elaborating on the purpose of the program and what information it provides
f.write("</p>")
#end paragraph
f.write("</body>")
#end body
f.write(data.to_html(index = False))
#use the to_html() function in pandas to convert the original dataframe to html code
f.write("<br>")
#<br> to start a new line
f.write(df.to_html(index = False))
#use the to_html() function in pandas to convert the table of statistics into html code
f.write("<img src = 'hydrogen_shifts.png'>")
#add the image generated by the function shift_graph using the hydrogen chemical shifts
f.write("<img src = 'carbon_shifts.png'>")
#add the image generated by the function shift_graph using the carbon chemical shifts
f.write("</html>")
#end the html code

print("Done!")
