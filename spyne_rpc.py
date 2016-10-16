import logging
logging.basicConfig(level=logging.DEBUG)
from spyne import Application, rpc, ServiceBase, \
    Integer, Unicode, decorator,Float
from spyne.decorator import srpc
from spyne import Iterable
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication
import apihandler

class CrimeReportService(ServiceBase):
    @srpc(Float, Float, Float,_returns=Unicode)
    def checkcrime(lat, lon, radius):
      return apihandler.call(lat, lon, radius)
       

application = Application([CrimeReportService],
    tns='shafidayatar.crimereport.test',
    in_protocol=HttpRpc(validator='soft'),
    out_protocol=JsonDocument()
)
if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()
