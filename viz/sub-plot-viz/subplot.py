import cx_Oracle as cx
import pandas as pd
import numpy as np
import json as js
import os
import getpass as gp

import plotly as py
import plotly.graph_objs as go
import plotly.offline as po

import plotly.figure_factory as ff
from plotly import tools


### Creds
passage = gp.getpass('Speak friend and enter:')

### cx_Oracle Connection String
conn = cx.connect()

### Donde esta mi data                               
os.chdir('')

######### Data source for enroll vs capacity #########

sql2 = open('dc-course-time-level-7.sql', 'r').read()

df2 = pd.read_sql(sql2, con=conn)



######### Data Transformation ############

wdrw = df2[df2['COURSE_LEVEL']=='100 Level']

wdrw['ENROLLMENT_CAPACITY']=wdrw['ENROLLMENT_CAPACITY'].astype(float)
wdrw['STARTHOUR24']=wdrw['STARTHOUR24'].astype(float)

agg_funcs = {'ENROLLMENT_COUNT':np.sum, 'WDRW_COUNT':np.sum, 'ENROLLMENT_CAPACITY':np.sum, 'GRADE_PTS_AWARDED':np.sum, 'GRADES_AWARDED_CNT':np.sum, 'GPA_OUTPERFORM_CNT':np.sum, 'GPA_GRADED_CNT':np.sum}

wdrw = wdrw.groupby(['STARTHOUR24'],as_index=False).agg(agg_funcs)


wdrw['WDRW_RATE']=wdrw['WDRW_COUNT']/wdrw['ENROLLMENT_COUNT']
wdrw['OCC_RATE']=wdrw['ENROLLMENT_COUNT']/wdrw['ENROLLMENT_CAPACITY']
wdrw['GPA_AWD']=wdrw['GRADE_PTS_AWARDED']/wdrw['GRADES_AWARDED_CNT']
wdrw['GPA_OUTPERFORM']=wdrw['GPA_OUTPERFORM_CNT']/wdrw['GPA_GRADED_CNT']
wdrw['UNUSED_CAP']=wdrw['ENROLLMENT_CAPACITY']-wdrw['ENROLLMENT_COUNT']


wdrw2 = df2[df2['COURSE_LEVEL']!= '100 Level']

wdrw2['ENROLLMENT_CAPACITY']=wdrw2['ENROLLMENT_CAPACITY'].astype(float)
wdrw2['STARTHOUR24']=wdrw2['STARTHOUR24'].astype(float)

wdrw2 = wdrw2.groupby(['STARTHOUR24'],as_index=False).agg(agg_funcs)

wdrw2['WDRW_RATE']=wdrw2['WDRW_COUNT']/wdrw2['ENROLLMENT_COUNT']
wdrw2['OCC_RATE']=wdrw2['ENROLLMENT_COUNT']/wdrw2['ENROLLMENT_CAPACITY']
wdrw2['GPA_AWD']=wdrw2['GRADE_PTS_AWARDED']/wdrw2['GRADES_AWARDED_CNT']
wdrw2['GPA_OUTPERFORM']=wdrw2['GPA_OUTPERFORM_CNT']/wdrw2['GPA_GRADED_CNT']
wdrw2['UNUSED_CAP']=wdrw2['ENROLLMENT_CAPACITY']-wdrw2['ENROLLMENT_COUNT']


###########    4-in-1 Graph  100 Level #############


hour_lbl = wdrw['STARTHOUR24']
color0 = wdrw['WDRW_RATE']
ycount0 = wdrw['ENROLLMENT_COUNT']
color1 = wdrw['OCC_RATE']
ycount1 = wdrw['ENROLLMENT_CAPACITY']
color2 = wdrw['GPA_AWD']
ycount2 = wdrw['GRADES_AWARDED_CNT']
color3 = wdrw['GPA_OUTPERFORM']
ycount3 = wdrw['GPA_GRADED_CNT']
text0 = ycount0.astype(str) + ' student enrollments <br><b>' + (color0*100).round(2).astype(str) + '% withdrawal rate </b><br>' + wdrw['WDRW_COUNT'].astype(str) + ' total withdrawals'
text1 = ycount1.astype(int).astype(str) + ' enrollment capacity <br><b>' + (color1*100).round(2).astype(str) + '% enrollment rate </b><br>' + wdrw['ENROLLMENT_COUNT'].astype(str) + ' total enrollments<br>' + wdrw['UNUSED_CAP'].astype(int).astype(str) + ' seats below capacity'
text2 = ycount2.astype(str) + ' grades awarded <br><b>' + color2.round(2).astype(str) + ' avg. GPA awarded</b>'
text3 = ycount3.astype(str) + ' grades awarded (with incoming GPA)<br><b>' + (color3*100).round(2).astype(str) + '% of students received a grade greater than their incoming GPA</b>'


hour_lbl2 = wdrw2['STARTHOUR24']
color4 = wdrw2['WDRW_RATE']
ycount4 = wdrw2['ENROLLMENT_COUNT']
color5 = wdrw2['OCC_RATE']
ycount5 = wdrw2['ENROLLMENT_CAPACITY']
color6 = wdrw2['GPA_AWD']
ycount6 = wdrw2['GRADES_AWARDED_CNT']
color7 = wdrw2['GPA_OUTPERFORM']
ycount7 = wdrw2['GPA_GRADED_CNT']
text4 = ycount4.astype(str) + ' student enrollments <br><b>' + (color4*100).round(2).astype(str) + '% withdrawal rate </b><br>' + wdrw2['WDRW_COUNT'].astype(str) + ' total withdrawals'
text5 = ycount5.astype(int).astype(str) + ' enrollment capacity <br><b>' + (color5*100).round(2).astype(str) + '% enrollment rate </b><br>' + wdrw2['ENROLLMENT_COUNT'].astype(str) + ' total enrollments<br>' + wdrw2['UNUSED_CAP'].astype(int).astype(str) + ' seats below capacity'
text6 = ycount6.astype(str) + ' grades awarded <br><b>' + color6.round(2).astype(str) + ' avg. GPA awarded</b>'
text7 = ycount7.astype(str) + ' grades awarded (with incoming GPA)<br><b>' + (color7*100).round(2).astype(str) + '% of students received a grade greater than their incoming GPA</b>'




trace0 = go.Bar(
    x=hour_lbl,
    y=ycount0,
    hoverinfo='text',
    text=text0,
    marker=dict(
        color=color0
        ,showscale=True
        ,colorscale='Viridis'
        ,cmax=.0125
        ,cmin=.006),
    showlegend=False,
    visible=True,
    opacity=0.9
)


trace1 = go.Bar(
    x=hour_lbl,
    y=ycount1,
    hoverinfo='text',
    text=text1,
    marker=dict(
        color=color1
        ,showscale=True
        ,colorscale='Portland'        
        ,cmax=1.0
        ,cmin=.835),
    showlegend=False,
    visible=False,
    opacity=0.9
)


trace2 = go.Bar(
    x=hour_lbl,
    y=ycount2,
    hoverinfo='text',
    text=text2,
    marker=dict(
        color=color2
        ,showscale=True
        ,colorscale='RdBu'        
        ,cmax=3.25
        ,cmin=2.75),
    showlegend=False,
    visible=False,
    opacity=0.9
)


trace3 = go.Bar(
    x=hour_lbl,
    y=ycount3,
    hoverinfo='text',
    text=text3,
    marker=dict(
        color=color3
        ,showscale=True
        ,colorscale='RdBu'        
        ,cmax=.63
        ,cmin=.42),
    showlegend=False,
    visible=False,
    opacity=0.9
)

trace4 = go.Bar(
    x=hour_lbl2,
    y=ycount4,
    hoverinfo='text',
    text=text4,
    marker=dict(
        color=color4
        ,showscale=True
        ,colorscale='Viridis'
        ,cmax=.0125
        ,cmin=.006),
    showlegend=False,
    visible=True,
    opacity=0.9
)


trace5 = go.Bar(
    x=hour_lbl2,
    y=ycount5,
    hoverinfo='text',
    text=text5,
    marker=dict(
        color=color5
        ,showscale=True
        ,colorscale='Portland'        
        ,cmax=1.0
        ,cmin=.835),
    showlegend=False,
    visible=False,
    opacity=0.9
)


trace6 = go.Bar(
    x=hour_lbl2,
    y=ycount6,
    hoverinfo='text',
    text=text6,
    marker=dict(
        color=color6
        ,showscale=True
        ,colorscale='RdBu'        
        ,cmax=3.25
        ,cmin=2.75),
    showlegend=False,
    visible=False,
    opacity=0.9
)


trace7 = go.Bar(
    x=hour_lbl,
    y=ycount7,
    hoverinfo='text',
    text=text7,
    marker=dict(
        color=color7
        ,showscale=True
        ,colorscale='RdBu'        
        ,cmax=.63
        ,cmin=.42),
    showlegend=False,
    visible=False,
    opacity=0.9
)

data = [trace0, trace1, trace2, trace3, trace4, trace5, trace6, trace7]

updatemenus = list([
    dict(type="buttons",
         active=-1,
         buttons=list([   
            dict(label = 'Withdrawals',
                 method = 'update',
                 args = [{'visible': [True, False, False, False, True, False, False, False]},
                         {'title': '<b>Count of Total Enrollments by Class Start Hour | Color by Withdraw Rate</b> <br> Winter 2014 to Spring 2017 (Summers Excluded)'}]),
            dict(label = 'Enroll v Capacity',
                 method = 'update',
                 args = [{'visible': [False, True, False, False, False, True, False, False]},
                         {'title': '<b>Sum of Total Capacity by Class Start Hour | Color by Enrollment Rate</b> <br> Winter 2014 to Spring 2017 (Summers Excluded)'}]),
            dict(label = 'Grades Awarded',
                 method = 'update',
                 args = [{'visible': [False, False, True, False, False, False, True, False]},
                         {'title': '<b>Count of Grades Awarded by Class Start Hour | Color by Avg. GPA Awarded</b> <br> Winter 2014 to Spring 2017 (Summers Excluded)'}]),
            dict(label = 'Grade vs Incoming GPA',
                 method = 'update',
                 args = [{'visible': [False, False, False, True, False, False, False, True]},
                         {'title': '<b>Count of Grades Awarded by Class Start Hour | Color by % Graded Above Incoming GPA</b> <br> Winter 2014 to Spring 2017 (Summers Excluded)'}]),
        ]),
    )
])


fig = tools.make_subplots(rows=2, cols=1, shared_xaxes=True)


fig.append_trace(trace0, 1, 1)
fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 1, 1)
fig.append_trace(trace3, 1, 1)
fig.append_trace(trace4, 2, 1)
fig.append_trace(trace5, 2, 1)
fig.append_trace(trace6, 2, 1)
fig.append_trace(trace7, 2, 1)



fig['layout']['yaxis2'].update(
                             )
fig['layout'].update(
    title='<b>Count of Total Enrollments by Class Start Hour | Color by Withdraw Rate</b> <br> Winter 2014 to Spring 2017 (Summers Excluded)',
    font=dict(family='Trebuchet MS', size=18),
    showlegend=False,
    updatemenus=updatemenus,
    xaxis1=dict(
            title='Class Start Hour (24hr Time)',
            titlefont=dict(
                family='Trebuchet MS',
                size=26,
                color='#7f7f7f'
            ),
            autotick=False,        
            dtick=1,
            ticklen=1,
            tickwidth=1
        ),
    yaxis1=dict(
        title='100 Level',
        titlefont=dict(
            family='Trebuchet MS',
            size=26,
            color='#7f7f7f'
            )
        ),
    yaxis2=dict(
        title='200+ Level',
        titlefont=dict(
            family='Trebuchet MS',
            size=26,
            color='#7f7f7f'
            )
         )
)



py.offline.plot(fig, show_link=False, filename='hourly-metrics.html')


################################################################


sqlFile = open('dc-course-time-prof-7.sql', 'r').read()
                               
df = pd.read_sql(sqlFile, con=conn)

### Transform dataframe
gpadiff = df
gpadiff['gpa-DELTA'] = gpadiff['NONSEVGPA']-gpadiff['SEVGPA']
gpadiff['pass-DELTA'] = gpadiff['NONSEVPASSRATE']-gpadiff['SEVPASSRATE']
gpadiff['gpa-outperform-DELTA'] = gpadiff['NONSEVGPA_OUTPERFORM']-gpadiff['SEVGPA_OUTPERFORM']
def gpaadvan(df):
    if df['gpa-DELTA'] < 0:
        return '7am Advantage'
    elif df['gpa-DELTA'] == 0:
        return 'Same GPA'
    else:
        return 'After 7am Advantage'
def passadvan(df):
    if df['pass-DELTA'] < 0:
        return '7am Advantage'
    elif df['pass-DELTA'] == 0:
        return 'Same Rate'
    else:
        return 'After 7am Advantage'
def gpaoutperform(df):
    if df['gpa-outperform-DELTA'] < 0:
        return '7am Advantage'
    elif df['gpa-outperform-DELTA'] == 0:
        return 'Same Rate'
    else:
        return 'After 7am Advantage'

gpadiff['gpa-advan'] = gpadiff.apply(gpaadvan, axis=1)
gpadiff['pass-advan'] = gpadiff.apply(passadvan, axis=1)
gpadiff['outperform-advan'] = gpadiff.apply(gpaoutperform, axis=1)

gpadist = gpadiff.groupby(['COURSE_LEVEL','gpa-advan'],as_index=False).size()
outperformdist = gpadiff.groupby(['COURSE_LEVEL','outperform-advan'],as_index=False).size()

course_level = gpadiff.groupby(['COURSE_LEVEL']).size()



########### GPA Diff Dist ##############

d1 = gpadiff[gpadiff['COURSE_LEVEL']=='100 Level']
d2 = gpadiff[gpadiff['COURSE_LEVEL']!='100 Level']
d1 = d1['gpa-DELTA']
d2 = d2['gpa-DELTA']



hist_data = [d1, d2]
group_labels = ['100 Level', '200+ Level']
colors = ['#cc6649', '#468499']
eldisto = ff.create_distplot(hist_data, group_labels, bin_size=.025, colors=colors)
distplot=eldisto['data']


########## GPA Advan Bar chart #############

gpadist=gpadist.div(course_level, level='COURSE_LEVEL').to_frame()
#passdist = passdist.div(course_level, level='COURSE_LEVEL').to_frame()
gpadist = gpadist.reset_index(level=['COURSE_LEVEL', 'gpa-advan'])

e1 = gpadist[gpadist['gpa-advan']=='7am Advantage']
e2 = gpadist[gpadist['gpa-advan']=='Same GPA']
e3 = gpadist[gpadist['gpa-advan']=='After 7am Advantage']
e1.columns = ['COURSE_LEVEL','gpa-advan','share']
e2.columns = ['COURSE_LEVEL','gpa-advan','share']
e3.columns = ['COURSE_LEVEL','gpa-advan','share']

erace1 = go.Bar(
    x=e1['COURSE_LEVEL'],
    y=e1['share'],
    name='7am Advantage',
    marker = dict(color = '#445a2f')
)
erace2 = go.Bar(
    x=e2['COURSE_LEVEL'],
    y=e2['share'],
    name='Same GPA'
)
erace3 = go.Bar(
    x=e3['COURSE_LEVEL'],
    y=e3['share'],
    name='After 7am Advantage',
    marker = dict(color = '#b69a6e')
)

fog = tools.make_subplots( subplot_titles=('<b>Distribution of Non-7am GPA minus 7am GPA</b> | (greater than 1 = higher GPA for non-7am sections)', '<B>Summary - % Awarding Higher Grades to 7am vs non-7am</b>'),
  #specs=[[{}, {'rowspan': 2}], #rowspan=2 means that we  concatenate  (1,2) with (2,2) into one cell encoded (1,2) 
         #[{},  None]],                       
    rows=1,
    cols=2
    )
fog.append_trace(distplot[0], 1, 1)
fog.append_trace(distplot[1], 1, 1)
fog.append_trace(distplot[2], 1, 1)
fog.append_trace(distplot[3], 1, 1)
#fog.append_trace(distplot[4], 2, 1)
#fog.append_trace(distplot[5], 2, 1)
fog.append_trace(erace1, 1, 2)
fog.append_trace(erace2, 1, 2)
fog.append_trace(erace3, 1, 2)
fog['layout'].update(title='<b>Do Professors Award Higher or Lower Grades for 7am Sections?</b> | Winter 2014 to Spring 2017 (Summers Excluded)')

py.offline.plot(fog, show_link=False, filename='gpa-diff-7am.html')


#########  Enrollment vs Capacity Dist  ##########


popocc = df2
popocc = popocc[popocc['OCCUPANCY']<=2]

dd1 = popocc[popocc['SEVWINDOW']=='7am']
dd2 = popocc[popocc['SEVWINDOW']!='7am']
dd1 = dd1['OCCUPANCY']
dd2 = dd2['OCCUPANCY']


hist_data = [dd1, dd2]
group_labels = ['7am Classes', 'After 7am Classes']
colors = ['#333F44','#94F3E4']
fig3 = ff.create_distplot(hist_data, group_labels, bin_size=.05, show_hist=False,colors=colors)
fistplot = fig3['data']

###########    At/over Capacity Bar  #############
classfull = popocc.groupby(['SEVWINDOW'],as_index=False).agg({'CLASS_FULL':'mean'})
classfull = classfull.reset_index(level=['SEVWINDOW'])
classfull.columns = ['SEVWINDOW','full']
print classfull
colorz = ['#37AA9C','#94F3E4' ]
trace0 = go.Bar(
    x=classfull['SEVWINDOW'],
    y=classfull['full'],
    marker=dict(
        color=colorz),
)

#ddata = [trace0]
#ddayout = go.Layout(
#    title='% at or Over Capacity by Popular Window - Winter 2014 to Spring 2017',
#)
#fig4 = go.Figure(data=ddata,layout=ddayout)
#print po.plot(fig4,show_link=False, filename='full-class.html')

feg = tools.make_subplots( subplot_titles=('<b>Distribution of Enrollment to Capacity </b> | (% enroll to capacity, including withdrawals)', '<b>Summary - % Sections at Capacity</b> | 7am vs non-7am'),
  #specs=[[{}, {'rowspan': 2}], #rowspan=2 means that we  concatenate  (1,2) with (2,2) into one cell encoded (1,2) 
         #[{},  None]],                       
    rows=1,
    cols=2
    )
feg.append_trace(fistplot[0], 1, 1)
feg.append_trace(fistplot[1], 1, 1)
feg.append_trace(trace0, 1, 2)

feg['layout'].update(title='<b>How is Enrollment to Capacity Different for 7am Classes?</b> | Winter 2014 to Spring 2017 (Summers Excluded)')

py.offline.plot(feg, show_link=False, filename='enroll-diff-7am.html')