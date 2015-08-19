from subprocess import Popen, PIPE
import os
import SimpleHTTPServer
import SocketServer
import threading
import sys, getopt


def start_server(port, cwd, bind=""):
    #http.server.test(HandlerClass=http.server.SimpleHTTPRequestHandler,port=port,bind=bind)

    handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    try:
        httpd = SocketServer.TCPServer(("", port), handler)
        httpd_thread = threading.Thread(target=httpd.serve_forever)
        httpd_thread.setDaemon(True)
        httpd_thread.start()

        print('Server started at {}'.format(os.getcwd()))
        return httpd_thread
    except Exception as e:
        print('Server already running')
        return None


def main(argv):
    PORT = 8000
    cwd = os.getcwd()
    os.chdir("..")
    server = start_server(port = PORT, cwd=cwd)
    os.chdir(cwd)
    sleep(10000)


if __name__ == "__main__":
    main(sys.argv[1:])

