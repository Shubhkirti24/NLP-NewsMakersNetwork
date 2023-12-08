from flask import Flask, render_template, request, redirect
import pandas as pd
from flask_debugtoolbar import DebugToolbarExtension
import os
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib.colors as mcolors
import plotly.offline as py
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/network')
def network():
    return render_template('network.html', content= "Newsmaker Network Builder")

@app.route('/about')
def about():
    return render_template('about.html', content= "about this site")

@app.route('/entityrec',methods = ['POST', 'GET'])
def entityrec():
    if request.method == 'POST':
        csv_path = os.path.join(app.root_path, 'static', 'co_sent.csv')
        csv_path3 = os.path.join(app.root_path, 'static', 'related_entites.csv')
        entity_df = pd.read_csv(csv_path)
        related_df = pd.read_csv(csv_path3)
        pr = request.form['pr']
        result = entity_df[entity_df['Name1'].str.contains(pr, case=False, na=False)]
        per_name = result.iloc[0]['Name1']
        result3 = related_df[related_df['Person'].str.contains(pr, case=False, na=False)]
        ent_10 = result3.iloc[0]['Top 10 Related Entities']
        sent_ave = result.iloc[0]['Average Sentiment']
        top_n = 30
        
        def make_edge(x, y, text, width):
            return go.Scatter(x=x, y=y, line=dict(width=width, color='cornflowerblue'),
                          hoverinfo='text', text=([text]), mode='lines')
        
        newsmakers = nx.DiGraph()
        result2 = entity_df[entity_df['Name1'].str.contains(per_name, case=False, na=False)]
        result2 = result2.nlargest(top_n, 'Co-mentions')
        
        min_value = result2['Co-mentions'].min() 
        max_value = result2['Co-mentions'].max()
        result2['Normalized Co-mentions'] = (result2['Co-mentions'] - min_value) / (max_value - min_value)
        
        for index, row in result2.iterrows():
            newsmakers.add_edge(row['Name1'], row['Name2'], weight=row['Normalized Co-mentions'],sentiment=row['Average Sentiment'])
            
        # Calculate average sentiment
        sentiment_sum = {node: 0 for node in newsmakers.nodes()}
        sentiment_count = {node: 0 for node in newsmakers.nodes()}
        for (n1, n2, data) in newsmakers.edges(data=True):
            sentiment_sum[n1] += data['sentiment']
            sentiment_sum[n2] += data['sentiment']
            sentiment_count[n1] += 1
            sentiment_count[n2] += 1
            
        node_sentiment = {node: (sentiment_sum[node] / sentiment_count[node] if sentiment_count[node] > 0 else 0) for node in newsmakers.nodes()}
        
        # Map sentiment to color
        min_sentiment = min(node_sentiment.values())
        max_sentiment = max(node_sentiment.values())
        
        if min_sentiment > 0:
            min_sentiment = -1 * max_sentiment
            
        norm = mcolors.TwoSlopeNorm(vmin=min_sentiment, vcenter = 0, vmax=max_sentiment)
        node_color = [mcolors.to_hex(plt.cm.RdYlGn(norm(node_sentiment[node]))) for node in newsmakers.nodes()]
        
        pos = nx.spring_layout(newsmakers)
        
        edge_trace = []
        for edge in newsmakers.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            text = f'{edge[0]} -- {edge[1]}: Co-mentions: {newsmakers.edges()[edge]["weight"]}'
            trace = make_edge([x0, x1, None], [y0, y1, None], text, 10 * newsmakers.edges()[edge]['weight']**1)
            edge_trace.append(trace)
            
        node_trace = go.Scatter(x=[], y=[], text=[], textposition="top center", textfont_size=10, mode='markers+text',
                        hoverinfo='none', marker=dict(color=node_color, size=50))
        
            # Add node positions and labels
        for node, (x, y) in pos.items():
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])
            node_trace['text'] += tuple(['<b>' + node + '</b>'])
        
        cmap = plt.cm.RdYlGn
        color_scale = [mcolors.to_hex(cmap(i)) for i in range(256)]
        color_scale = [color_scale[int(i * 255)] for i in norm([min_sentiment, 0, max_sentiment])]
        
        layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        
        # Create figure and add traces
        fig = go.Figure(layout=layout)
        for trace in edge_trace:
            fig.add_trace(trace)
        fig.add_trace(node_trace)

        # Update layout settings
        fig.update_layout(showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False, xaxis_zeroline=False, yaxis_zeroline=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        
        img_data = fig.show()
    return render_template('result.html', img_data=img_data, ent_10=ent_10, per_name=per_name, sent_ave=sent_ave)
    # return send_file(img, mimetype='image/png')

    
app.debug = False
toolbar = DebugToolbarExtension(app)
#app.debug = True
if __name__ == "__main__":
    app.run(debug=True)