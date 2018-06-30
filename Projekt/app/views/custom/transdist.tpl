% include('header', **config, scripts = ["https://cdn.plot.ly/plotly-latest.min.js"])
<div id="out">
</div>
<script>
    let processData = function (data) {
        data.type = 'bar'

        let fig = {
          'data': [data],
          'layout': {
            xaxis: {title: 'Anzahl an eingehenden Transanktionen per Wallet'},
            yaxis: {title: 'Absolute Häufigkeit'}
          }
        }

        Plotly.newPlot('out', fig)
    }
</script>
% include('footer', **config)