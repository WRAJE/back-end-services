from http import *
class MyHttp(Http):
  def getRoot(self, path):
    body = f"<h1>Hello</h1><p>Path={path}</p>"
    self.response(body)

  def get404(self, path):
    body = f"<h1>404 Not Found</h1><p>Path={path}</p>"
    self.response(body)

MyHttp(HOST,PORT).start_server()