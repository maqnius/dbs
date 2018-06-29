<%
scripts = [
    "/static/sigma.min.js",
    "/static/sigma.plugins.animate.js",
    "/static/sigma.layout.noverlap.js"
]

include('header', **config, scripts=scripts)
%>
<div id="out"></div>
<script>
    let processData = function (data) {
        let s = new sigma('out')
        s.graph.read(data)
        let listener = s.configNoverlap({})

        // Bind all events:
        listener.bind('start stop interpolate', function(event) {
            console.log(event.type)
        })

        // Start the algorithm:
        s.startNoverlap()
        s.refresh()
    }
</script>
% include('footer', **config)