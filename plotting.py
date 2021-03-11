from motion_detection import df
from bokeh.plotting import show,figure,output_file
from bokeh.models import HoverTool, ColumnDataSource

df["Start_time"]=df["Start"].dt.strftime("%d/%m/%Y  %Hh:%Mm:%Ss")
df["End_time"]=df["End"].dt.strftime("%d/%m/%Y  %Hh:%Mm: %Ss")

cds=ColumnDataSource(df)

p=figure(x_axis_type='datetime',height=150,width=1000,title="Motion graph")
p.yaxis.ticker.desired_num_ticks=1
p.yaxis.minor_tick_line_color=None

hover=HoverTool(tooltips=[("Start","@Start_time"),("End","@End_time")])
p.add_tools(hover)

q=p.quad(left="Start",right="End",top=1,bottom=0,source=cds,color="green")

output_file("Graph.html")
show(p)