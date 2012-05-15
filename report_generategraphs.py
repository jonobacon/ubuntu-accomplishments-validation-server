import csv

days = []
todaynewusers = []
alltimetotalusers = []
alltimetotaltrophies = []
todaytotalusers = []
todaynewusers = []
todaytotaltrophies = []
todaynewtrophies = []

todaynewusers_html = ""
todaynewtrophies_html = ""
totalusers_html = ""
totaltrophies_html = ""

#html = "<h1>Accomplishments Stats</h1>"

lines = csv.reader(open('/home/jono/matrixstats_csv.txt', 'rb'), delimiter=',', quotechar='|')
lines.next()
# --------- New Users ----------------------------------------

#html = html + "<h2>New Users</h2>"

for row in lines:
    days.append(row[0])
    alltimetotalusers.append(int(row[1]))
    alltimetotaltrophies.append(int(row[2]))
    todaytotalusers.append(int(row[4]))
    todaynewusers.append(int(row[5]))
    todaytotaltrophies.append(int(row[6]))
    todaynewtrophies.append(int(row[7]))

    # total users HTML
    totalusers_html = totalusers_html + "['" + str(row[0]) + "'," +  str(row[1]) + "]," \

    # total users HTML
    totaltrophies_html = totaltrophies_html + "['" + str(row[0]) + "'," +  str(row[2]) + "]," \

    # today new users HTML
    todaynewusers_html = todaynewusers_html + "['" + str(row[0]) + "'," +  str(row[5]) + "]," \

    # today new trophies HTML
    todaynewtrophies_html = todaynewtrophies_html + "['" + str(row[0]) + "'," +  str(row[7]) + "]," \

html = "<html> \
  <head> \
    <script type='text/javascript' src='https://www.google.com/jsapi'></script> \
    <script type='text/javascript'> \
      google.load('visualization', '1.0', {'packages':['corechart']}); \
      google.setOnLoadCallback(drawChart); \
      google.setOnLoadCallback(drawTotalUsers); \
      google.setOnLoadCallback(drawTotalTrophies); \
      google.setOnLoadCallback(drawTodayTrophies);"

html = html + "function drawChart() { \
        var data = new google.visualization.DataTable(); \
        data.addColumn('string', 'Number Of Users'); \
        data.addColumn('number', 'Daily New Users');"

html = html + "data.addRows(["

html = html + todaynewusers_html

html = html + "]);  \
        var options = {'title':'Daily New Users', \
                       'width':1000, \
                       'height':600}; \
        var chart = new google.visualization.LineChart(document.getElementById('dailynewusers')); \
        chart.draw(data, options); \
      }"

# ----- total users -----

html = html + "function drawTotalUsers() { \
        var dataB = new google.visualization.DataTable(); \
        dataB.addColumn('string', 'Number Of Users'); \
        dataB.addColumn('number', 'Total Users');"

html = html + "dataB.addRows(["

html = html + totalusers_html

html = html + "]);  \
        var optionsB = {'title':'Total Users', \
                       'width':1000, \
                       'height':600}; \
        var chartB = new google.visualization.LineChart(document.getElementById('totalusers')); \
        chartB.draw(dataB, optionsB); \
      }"

# ----- total trophies -----

html = html + "function drawTotalTrophies() { \
        var dataB = new google.visualization.DataTable(); \
        dataB.addColumn('string', 'Number Of Trophies'); \
        dataB.addColumn('number', 'Total Trophies');"

html = html + "dataB.addRows(["

html = html + totaltrophies_html

html = html + "]);  \
        var optionsB = {'title':'Total Trophies', \
                       'width':1000, \
                       'height':600}; \
        var chartB = new google.visualization.LineChart(document.getElementById('totaltrophies')); \
        chartB.draw(dataB, optionsB); \
      }"

# ----- today new trophies -----

html = html + "function drawTodayTrophies() { \
        var data = new google.visualization.DataTable(); \
        data.addColumn('string', 'Number Of Trophies'); \
        data.addColumn('number', 'Daily New Trophies');"

html = html + "data.addRows(["

html = html + todaynewtrophies_html

html = html + "]);  \
        var options = {'title':'Daily Number of Signed Trophies Issued', \
                       'width':1000, \
                       'height':600}; \
        var chart = new google.visualization.LineChart(document.getElementById('dailynewtrophies')); \
        chart.draw(data, options); \
      }"
      
html = html + "</script> \
  </head> \
  <body> \
    <h2>Totals</h2> \
    <div id='totalusers'></div> \
    <div id='totaltrophies'></div> \
    <h2>Dailies</h2> \
    <div id='dailynewusers'></div> \
    <div id='dailynewtrophies'></div> \
  </body> \
</html>"

file = open("/var/www/admin/graphs/index.html","w")
file.write(html)
file.close()
