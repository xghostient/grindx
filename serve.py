"""Serve grindx in the browser."""

from textual_serve.server import Server

server = Server("python3 app.py")
server.serve()
