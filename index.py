import requests as r 
from io import StringIO
 
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
 
mydf= r.get("https://www.gunviolencearchive.org/export-finished/download?uuid=99d3ff0d-76d2-4042-bf55-15417482432b&filename=public%3A//export-01aa4618-47e5-44b1-8a8e-b97475b5bd28.csv",headers=headers).text
 
newdf = pd.read_csv(StringIO(mydf))
 
 
newdf['State'] = newdf['State'].map(us_state_abbrev).fillna(newdf['State'])
newdfkill = newdf[["State","# Killed"]].reset_index()
newkill = newdfkill.groupby("State")['# Killed'].sum().reset_index()
newkill.columns = ["State","Killings"]
 
finalkill= statekill.set_index('State').add(newkill.set_index('State'),fill_value=0).reset_index()
 
 
fig = px.choropleth(finalkill,
                    locations="State",
                    color="Killings", 
                    locationmode = 'USA-states',
                    color_continuous_scale="OrRd",
) 
fig.update_layout(
    title = {
        'text':"Live:Gun Violence Deaths Across America <br><sup> Confirmed deaths due to gun violence from 2013-2021 </sup>",
        'x':0.5,
        'xanchor':'center'
    },
    geo= dict(  
        scope = "usa",
        projection=go.layout.geo.Projection(type="albers usa"),
        showlakes=True,
        lakecolor='white'
    ),
    margin=dict(l=0, r=0, t=50,b=0),
    font=dict(size=12),     
    coloraxis_colorbar=dict(
        title="Amount of Deaths",
    )
)
fig.data[0].marker.line.color = "white"
fig.show()
newdfinjured = newdf[["State","# Injured"]].reset_index()
newdfinjured['State'] = newdfinjured['State'].map(us_state_abbrev).fillna(newdf['State'])
newinjury = newdfinjured.groupby("State")['# Injured'].sum().reset_index()
newinjury.columns = ["State","Injured"]
finalinjury= stateinjury.set_index('State').add(newinjury.set_index('State'),fill_value=0).reset_index()
fig = px.choropleth(finalinjury,
                    locations="State",
                    color="Injured", 
                    locationmode = "USA-states",
                    color_continuous_scale="RedOr",
) 
fig.update_layout(
    title = {
        'text':"Live: Gun Violence Injuries Across America <br><sup> Confirmed injuries due to gun violence from 2013-2021 </sup>",
        'x':0.5,
        'xanchor':'center'
    },
    geo= dict(  
        scope = "usa",
        projection=go.layout.geo.Projection(type="albers usa"),
        showlakes=True,
        lakecolor='white'
    ),
    margin=dict(l=0, r=0, t=50,b=0),
    font=dict(size=12),     
    coloraxis_colorbar=dict(
        title="Amount of Injuries",
    )
)
 
fig.data[0].marker.line.color = "white"
fig.show()
