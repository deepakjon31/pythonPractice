from flask import Flask, render_template, request
from datetime import datetime, timedelta
from bokeh.plotting import figure

from bokeh.embed import components


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

        return render_template('tweeter.html', user_tweeter=user_tweeter, item=item, days=delta.days,
                               tweet_per_day=tweet_per_day)

def create_figure(current_feature_name, bins):
	p = Histogram(iris_df, current_feature_name, title=current_feature_name, color='Species',
	 	bins=bins, legend='top_right', width=600, height=400)

	# Set the x axis label
	p.xaxis.axis_label = current_feature_name

	# Set the y axis label
	p.yaxis.axis_label = 'Count'
	return p


@app.route('/chart')
def charts():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    colors = ["#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA", "#ABCDEF", "#DDDDDD", "#ABCABC"]
    return render_template('charts.html', set=zip(values, labels, colors), data=df)

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
