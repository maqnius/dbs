<!doctype html>
<html>
	<head>
		<meta charset="utf-8"></meta>
		<title>Eine Website</title>
	</head>
	<body>
		<label for="eingabe">
			Ihr Name: <input id="feld" name="eingabe"></input>
		</label>
		<button id="knopf" type="button">
			Klick mich!
		</button>
		<div id="bereich"></div>

		<script type="text/javascript">
			document.getElementById("knopf").onclick = () => {
				let text = 'Hallo ';
				let eingabe = document.getElementById("feld").value;
				if(eingabe.trim()){
					text += eingabe + '!';
				} else {
					text += 'Unbekannter!'
				}

				document.getElementById('bereich').innerHTML = text;
			}
		</script>

	</body>
</html>