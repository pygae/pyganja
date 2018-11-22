
from flask import Flask, request, render_template
import os


app = Flask(__name__)


@app.route("/")
def render_main():
    return render_template('default.html', show_help=True, show_tools=True)


@app.route('/<page>')
def show(page):
    show_tools_string = request.args.get('show_tools')
    if show_tools_string == 'True':
        show_tools = True
    else:
        show_tools = False
    return render_template('%s.html' % page, show_help=False, show_tools=show_tools)


def end_graphics_server(server, fullname):
    server.terminate()
    server.join()
    if os.path.isfile(fullname):
            os.remove(fullname)


def run_app():
    app.run()


if __name__ == '__main__':
    app.run()
