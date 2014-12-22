#!/usr/bin/env python

import pickle
from nvd3.lineWithFocusChart import lineWithFocusChart
import datetime
import os


def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    # Correct for Eastern timezone
    return delta.total_seconds()*1000+5*60*60*1000


history = pickle.load(open('history.p', 'rb'))

#Open file for test
output_file = open('index.html', 'w')
type = "lineWithFocusChart"
chart = lineWithFocusChart(name='lineWithFocusChart', color_category='category20', x_is_date=True, x_axis_format="%a %I%p") # "%a %d %b %I%p"
chart.set_containerheader("\n\n<h2>" + '&#x03C1;(t)' + "</h2>\n\n")

extra_serie = {"tooltip": {"y_start": "Occupancy: ", "y_end": "%"},
               "date_format": "%d %b %Y %H:%M:%S %p"}
#extra_serie = None
for place in history.keys():
    if place not in ['Roone Arledge Auditorium', 'Lehman Library 1', 'Lehman Library 2', 'Lehman Library 3', 'Lerner 1', 'Lerner 2', 'Lerner 3', 'Lerner 4', 'Lerner 5', 'Architectural and Fine Arts Library 1', 'Architectural and Fine Arts Library 2', 'Architectural and Fine Arts Library 3']:
        (times, percentages) = zip(*history[place])
        times = [unix_time_millis(dt) for dt in times]
        if 'Place' in place:
            place = "JJs Place"
        if 'Butler' in place:
            place = place.replace('Library', '')
        chart.add_serie(name=place, y=percentages, x=times, extra=extra_serie)

chart.buildhtml()

chart.htmlcontent = chart.htmlcontent.replace("nv.models.lineWithFocusChart()", "nv.models.lineWithFocusChart().interpolate(\"basis\").forceY([0,100])")
chart.htmlcontent = chart.htmlcontent.replace(".tickFormat(d3.format(',.2f'));", ".tickFormat(d3.format(',d'));")
chart.htmlcontent = chart.htmlcontent.replace("450px", "550px")
chart.htmlcontent = chart.htmlcontent.replace(".attr('height', 450)", ".attr('height', 550)")

chart.htmlcontent = chart.htmlcontent.replace("<head>",
     '''<head>
        <style>
            body {
                font-family: "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;
            }
            a {
                color: #3a9cff;
                text-decoration: none;
            }
            a:hover {
                color:#f04242;
            }
            h2, p {
                margin-left: 20px;
            }
        </style>''')

chart.htmlcontent = chart.htmlcontent.replace("<h2>&#x03C1;(t)</h2>",
        '''<h2>&#x03C1;(t)</h2>

<p>Watch people mill around Columbia during reading week and finals.</p>

<p>Drag across the mini chart to select a range. Click or double click on a location to toggle its visibility. Updates every 15 minutes with data from <a href="http://density.adicu.com">density.adicu.com</a>.</p>''')

output_file.write(chart.htmlcontent)

#close html file
output_file.close()
