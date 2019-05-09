import http.server
import json
import socketserver
import sys
import urllib

socketserver.TCPServer.allow_reuse_address
PORT = 8000

class Genius(http.server.BaseHTTPRequestHandler):

    def app_principal(self):
        html = """
        		<html>
        				<head>
        						<title>genius_lydia</title>
        						<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        				</head>
        				<body align=center style='background-color: #ECF6CE'>
        						<h1>Bienvenido a la App de búsqueda de artistas y sus respectivas canciones</h1>
        						<h2>A continuación tiene un formulario en el que podrá realizar la búsqueda que necesite</h2>
        						<br>
        						<form method="get" action="searchSongs">
        								<input type = "submit" value="Introduce el nombre del artista">
        								<input type = "text" name="artist"></input>
        								</input>
        						</form>
        						<br>
        						<br>

        <p> Ingeniería Biomédica  </p>
        <p> Universidad Rey Juan Carlos  </p>
        						<p>  Grado en Ingeniería Biomédica  </p>
        						<p> Curso 2018-2019 - URJC </p>
        <p> Lydia Marugán Romero  </p>
        				</body>
        		</html>
        				"""
        return html

    def app_secundaria(self, lista):
        html = """
                                        <html>
                                            <head>
                                                <title>Openfda Lydia </title>
                                                <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
                                            </head>
                                            <body style='background-color: #ECF6CE'>
                                            <ul style='list-style: none;' >
                                                <h1> Resultado de su búsqueda: </h1>
                                                <br>
                                                <ul>
                                    """

        for song in lista:
            html += "<li style='height:50px'>"
            print('default_cover')
            print(song['header_image_thumbnail_url'])
            html += "<img align='left' height='70' width='70' src='" + song['header_image_thumbnail_url'] + "'>"
            html += "<a href='" + song['url'] + "'>"
            html += "<h4>" + song['title'] + "</h4>"
            #html += "</a>"
            #html += "</li>"
        html += """
                                                </ul>
                                            </body>
                                        </html>
                                    """
        html += ('</ul>\n'
                    '\n'
                    '<a href="/">Volver a la página inicial </a>'
                    '</body>\n'
                    '</html>')
        return html

    def resultado_incorrecto(self):
        html = """
                                        <html>
                                            <head>
                                                <title>Openfda Lydia </title>
                                                <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
                                            </head>
                                            <body style='background-color: #ECF6CE'>
                                                <h1> Respuesta no encontrada: </h1>
                                                <p> Introduzca una nueva respuesta en la página inicial <p>
                                                <br>
                                                <ul>
                                    """

        html += ('</ul>\n'
                    '\n'
                    '<a href="/">Volver a la página inicial </a>'
                    '</body>\n'
                    '</html>')
        return html

    def resultado_vacio(self):
        html = """
                                        <html>
                                            <head>
                                                <title>Openfda Lydia </title>
                                                <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
                                            </head>
                                            <body style='background-color: #ECF6CE'>
                                                <h1> Respuesta vacía: </h1>
                                                <p> Introduzca una respuesta en la página inicial <p>
                                                <br>
                                                <ul>
                                    """

        html += ('</ul>\n'
                    '\n'
                    '<a href="/">Volver a la página inicial </a>'
                    '</body>\n'
                    '</html>')
        return html

    def peticion(self, query):
        URL = "api.genius.com"
        try:
            token = sys.argv[1]
        except IndexError:
            token = "Adi0jx3rNY6vqnEZ9LrWDgemaM-bh_qdpizovx5g1YbZSqepFgp6bPPaABvJ0pRM"

        headers = {'User-Agent': 'http-client'}
        conexion = http.client.HTTPSConnection(URL)
        headers = {"Authorization": "Bearer " + token}

        conexion.request("GET", query, None, headers)
        resp = conexion.getresponse()
        resp1 = resp.read().decode("utf-8")
        conexion.close()
        respuesta = json.loads(resp1)
        return respuesta

    def buscar_artista(self, nombre):
        try:
            url = "/search?q=" + nombre
            repo = self.peticion(url)

            for item in repo['response']['hits']:
                artistas = item['result']['primary_artist']['name']
                artista = nombre.replace("+", " ")
                if artista in artistas:
                    id = item['result']['primary_artist']['id']
                    break

          # 20 indica el número de páginas y 1 el número de páginas
            url = "/artists/%s/songs?per_page=%i&page=%i" % (id, 20, 1)
            canciones = self.peticion(url)
            titulos = canciones['response']['songs']
            return titulos

        except UnboundLocalError:
            if nombre == "":
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                resultado_final = self.resultado_vacio()
                self.wfile.write(bytes(resultado_final, "utf8"))
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                resultado_final = self.resultado_incorrecto()
                self.wfile.write(bytes(resultado_final, "utf8"))



    def do_GET(self):

        if self.path == "/":
            resultado_final = self.app_principal()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(resultado_final, "utf8"))
        elif 'searchSongs' in self.path:
            corte= self.path.split("?")[1]
            artista = corte.split("=")[1]
            titulos = self.buscar_artista(artista)
            if titulos:
                resultado_final = self.app_secundaria(titulos)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(resultado_final, "utf8"))
        elif 'redirect' in self.path:
            self.send_response(301)
            self.send_header('Location', 'http://localhost:' + str(PORT))
            self.end_headers()
        elif 'secret' in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Recurso no encontrado '{}'.".format(self.path).encode())
        return

socketserver.TCPServer.allow_reuse_address = True
Handler = Genius
httpd = socketserver.TCPServer(("", PORT), Genius)
print("Sirviendo en el puerto:", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("El usuario ha interrumpido la conexión en el puerto", PORT)

print("Servidor parado")
