% include('header', **config)
<div id="out">
</div>
<script>
    let processData = function (data) {
        $('#out').html(JSON.stringify(data));
    }
</script>
% include('footer', **config)