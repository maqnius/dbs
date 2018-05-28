<%
"""
Header Template with navigation bar

"""

%>
<html>
<head>
    <title>{{title or 'No title'}}</title>
    <script src="/static/jquery-3.3.1.min.js"></script>
    <link rel="stylesheet" type="text/css" href="/static/main.css">
</head>
<body>
<header>
    <ul>
        % for url, name in menu.items():
            <li>
                <a class={{"active" if url==cur_url else ""}}  href="{{url}}">{{name}}</a>
            </li>
        % end
    </ul>
</header>
<section>