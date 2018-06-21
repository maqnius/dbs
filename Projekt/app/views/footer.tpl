</div>
<script>
    fetch('{{api_url}}')
        .then(function(response) {
            return response.json();
        })
        .then((data) => processData(data));
</script>
</body>
</html>