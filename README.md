# Ghosts - TDA aplikace

## Dokumentace

### Důležité akce před začátkem vývoje

<p>WSL2 s disturucí Ubuntu -
<a href="https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-10#1-overview">https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-10#1-overview</a> <br>
Docker - <a href="https://tourdeapp.cz/vzdelavaci-materialy/2738-instalace-dockeru-na-windows">https://tourdeapp.cz/vzdelavaci-materialy/2738-instalace-dockeru-na-windows</a> (+ návod jak nainstalovat WSL2) <br>
Ve svém vývojovém prostředí najdi Source Control a pomocí akce pull si "stáhni" repositář z GitHubu <b>vojk/ghosts_tda</b> <br><br>
Momentálně máš nainstalovaný WSL2 s distrubucí Ubuntu, Docker a stáhlý repositář <b>vojk/ghosts_tda</b></p>

## Spuštění aplikace

### Lokálně

**Windows**
<h4>Prerekvizity</h4>
<ul>
<li>Python 3.11</li>
<li><p>pipenv ( pip install --user pipenv pro Windows,  <a href="https://pypi.org/project/pipenv/#installation">https://pypi.org/project/pipenv/#installation</a> pro Linux dle distribuce). (Pokud se při instalaci na Windows vyskytla <a href="https://github.com/Tour-de-App/flask-boilerplate/blob/main/PATH%20warning.md">chyba s proměnnou PATH.</a>)</p></li>
</ul>

<h4>Spuštění</h4>
<code>pipenv install</code> <br>
<code>pipenv shell</code>

<code>flask --app app\app.py run</code>

(<code>flask is not recognized as an internal or external command, operable program or batch file.</code> -> Nainstaluj Flask pomocí <code>pip install Flask</code>)

**Linux / macOS**

<code>flask --app app/app.py run</code>
<p>Aplikace bude dostupná na <code>http://127.0.0.1:5000</code></p>

### Pomocí Docker

<code>docker build . -t tda-flask</code> <br>
<code>docker run -p 8080:80 -v ${PWD}:/app tda-flask</code>

<p>Aplikace bude dostupná na <code>http://127.0.0.1:8080</code></p>


NOTE: TEAM_SECRET se vloží nějakou tu chvíli před tím než to budeme chtít odevzdávat