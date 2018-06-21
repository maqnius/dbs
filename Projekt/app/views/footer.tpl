</div>
<script>
    $('div.loading').show()
    fetch('{{api_url}}')
        .then(function(response) {
            $('div.loading').hide()
            return response.json()
        })
        .then((data) => processData(data))
</script>
</body>
</html>