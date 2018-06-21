<%
"""
Header Template with navigation bar

"""

%>
<html>
<head>
    <title>{{title or 'No title'}}</title>

    <script src="/static/jquery-3.3.1.min.js"></script>
    % for link in get('scripts', []):
        <script src="{{link}}"></script>
    % end

    <link rel="stylesheet" type="text/css" href="/static/main.css">
    <link rel="stylesheet" type="text/css" href="/static/spectre.min.css">
    <link rel="stylesheet" type="text/css" href="/static/spectre-exp.min.css">
    <link rel="stylesheet" type="text/css" href="/static/spectre-icons.min.css">

    % for link in get('css', []):
        <link rel="stylesheet" type="text/css" href="{{link}}">
    % end
</head>
<body>
<header class="navbar bg-gray">
    <section class="navbar-section">
        % for url, name in menu.items():
            <a class="btn {{"btn-primary" if url==cur_url else "btn-link"}}"  href="{{url}}">{{name}}</a>
        % end
    </section>
</header>
<div id="main" class="container">
<div class="loading loading-lg"></div>