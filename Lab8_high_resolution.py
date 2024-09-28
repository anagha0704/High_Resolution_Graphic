# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 15:29:50 2024

@author: anagh
"""

import pandas as pd
from bokeh.plotting import figure, show, output_file
from math import pi
from bokeh.layouts import gridplot
from bokeh.models import Label


# Categorize age into groups
def age_grouping(dtfrm, ag_lbls):
    ag_bns = [0, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    
    # Cut the age data into bins
    dtfrm['age_grp'] = pd.cut(dtfrm[0], bins=ag_bns, labels=ag_lbls, right=False)
    
    # Count for age groups
    ag_grp_cnt = (dtfrm['age_grp'].value_counts()).to_dict()
    ag_grp_cnt = dict(sorted(ag_grp_cnt.items()))
    
    return(ag_grp_cnt)


# Count for Marrital Status
def att_counting(dtfrm, ag_lbls, att_list, ul):
    print("for", ag_lbls, ":")
    at_cnt_1 = []
    for i in range(len(ul)):
        for j in range(len(ul[i])):
            at_cnt = (dtfrm[dtfrm['age_grp'] == ag_lbls][att_list].value_counts().get(ul[i][j]))
            if at_cnt == None:
                at_cnt = 0
            at_cnt_1.append(at_cnt)
        print(at_cnt_1)
    return(at_cnt_1)

# Plot the bar
def plotting(dtfrm, att_counts, ag_lbls, ul):
    arr = ul[0]

    ul = arr.tolist()

    q = figure(x_range=ul, width = 350, height=350, toolbar_location=None, tools="")
    q.vbar(x=ul, top=att_counts, width=0.05*len(att_counts))    # bar width for all bars
    
    # For maximum data-Ink Ratio
    q.xgrid.grid_line_color = None
    q.yaxis.visible = True
    q.yaxis.major_label_text_font_size = '10pt'
    q.yaxis.minor_tick_line_color = None
    q.xaxis.major_tick_line_color = None
    q.yaxis.axis_line_color = None
    q.xaxis.visible = False
    q.toolbar.logo = None

    return (q)

# Plot the x-axis
def plot_x(ul, att_counts, e):
    
    if e == 0: 
        q = figure(x_range=ul, width = 350, height=25, min_border_left=130, toolbar_location=None, tools="")
      
    else:    
        q = figure(x_range=ul, width = 350, height=25, min_border_left=45, toolbar_location=None, tools="")
        
    y = [0]*len(ul)
    q.vbar(x=ul, top=y, width=0.0005*len(ul))

    # For Grid
    q.y_range.start = 0
    q.xgrid.grid_line_color = None
    q.xaxis.major_label_text_font_size = '10pt'
    q.xaxis.major_label_orientation = (-pi/2)
    q.xaxis.axis_line_color = None
    q.yaxis.visible = False
    q.toolbar.logo = None
    q.outline_line_color = None

    return (q)

    
dtfrm = pd.read_csv('adult.data', header=None)
ag_lbls = ['0-20 years', '20-30 years', '30-40 years', '40-50 years', '50-60 years', '60-70 years', '70-80 years', '80-90 years', '90-100 years']

grp_wise_count = age_grouping(dtfrm, ag_lbls)

att_list = [5,14,3,1]


plots = [[] for _ in range(len(ag_lbls))]  # Create a list for each 'column' in the final grid


for att in att_list:
    ul = []
    ul.append(dtfrm[att].unique())
    for j, ag_lbl in enumerate(ag_lbls):
        att_counts = []
        att_counts = att_counting(dtfrm, ag_lbl, att, ul)
        plot = plotting(dtfrm, att_counts, ag_lbl, ul)
        plots[j].append(plot)  
    
    
       
ul = []

for att in att_list:
      ul.append(dtfrm[att].unique())
    
plotxaxis = []
  
i = 0
while i<4:
    plotx = plot_x(ul[i], att_counts, i)
    plotxaxis.append(plotx)
    i = i+1
        

for i, x_label in enumerate(ag_lbls):
    # Create a label for the age group
    age_label = Label(x=3, y=150, x_units='screen', y_units='screen',
                      text=ag_lbls[i],
                      text_baseline='middle', text_align='left',
                      border_line_color='black', border_line_alpha=1.0,
                      background_fill_color='white', background_fill_alpha=1.0)
    
    # Inserting the label to the left of first plot in every row
    plots[i][0].add_layout(age_label, 'left')
    
    

g = gridplot(plots)

t = gridplot([plotxaxis])

final = gridplot([[g], [t]], toolbar_location=None)

output_file("lab8.html")

show(final)