<%
scripts = [
    "/static/sigma.min.js"
]

include('header', **config, scripts=scripts)
%>
<div id="out"></div>
<script>
    let processData = function (data) {
        let s = new sigma('out')
        s.graph.read(data)
        s.refresh()
    }
</script>
% include('footer', **config)