from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid, Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

from companies_csv import df
from tweeter_api import TweeterAPI


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html', data=df)


@app.route('/company/<company>', methods=['GET', 'POST'])
def compnaytweeter(company):
    if company in df['Company Name'].tolist():
        user_tweeter = df[df['Company Name'] == company]['Tweeter Link'].values.tolist()[0].split('/')[-1].replace('@', '')
        print(user_tweeter)
        try:
            tweeter = TweeterAPI()
            item = tweeter.get_user(user_tweeter)
            delta = datetime.utcnow() - item.created_at
            tweet_per_day = float(item.statuses_count) / float(delta.days)
        except:
            pass
        else:
            return render_template('tweeter.html', user_tweeter=user_tweeter, item=item, days=delta.days,
                                   tweet_per_day=tweet_per_day)
        return redirect(url_for('home.html', data=df))

def create_figure():
    plot = figure(plot_height=200, plot_width=200, toolbar_location=None)
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [2 ** v for v in x]

    plot.line(x, y, line_width=4)
    plot.toolbar.logo = None

    return plot


@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)


# cur.execute("create table pickled(id integer primary key, data blob)")
# cur.execute("insert into pickled(data) values (?)", (sqlite3.Binary(pickle.dumps(pass here object, protocol=2)),))
# Fetch the BLOBs back from SQLite
# cur.execute("select data from pickled")
# for row in cur:
# serialized_point = row[0]

# Deserialize the BLOB to a Python object - # pickle.loads() needs a
# bytestring.
# point = pickle.loads(str(serialized_point))
# print "got point back from database", point
