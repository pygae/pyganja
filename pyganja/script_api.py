
from __future__ import print_function

import hashlib
import time
from multiprocessing import Process

from IPython.display import Javascript

from .flask_server import *
from .GanjaScene import GanjaScene

try:
    from .cefwindow import *
except:
    print('Failed to import cef_gui, cef functions will be unavailable')

import urllib


def generate_jinja_template(script_json, algebra='g3c'):
    if algebra == 'g3c':
        script_string = """
        Algebra(4,1,()=>{
          document.body.appendChild(this.graph(""" + script_json + """,{conformal:true,gl:true,grid:false}));
        });
        """
    else:
        raise ValueError('Algebra not yet supported')
    s_start = """{% extends 'base.html' %}
    {% block user_script %}
    `"""
    s_end = """
    `
    {% endblock %}
    """
    return s_start + script_string + s_end


def generate_notebook_js(script_json, algebra='g3c'):
    if algebra == 'g3c':
        js = """
        function add_graph_to_notebook(Algebra){
            var output = Algebra(4,1,()=>{
              // When we get a file, we load and display.
                var canvas;
                var h=0, p=0;
                  // convert arrays of 32 floats back to CGA elements.     
                     var data = """ + script_json + """;
                     data = data.map(x=>x.length==32?new Element(x):x);
                  // add the graph to the page.
                     canvas = this.graph(data,{gl:true,conformal:true,grid:true});
                     canvas.options.h = h; canvas.options.p = p;
                  // make it big.
                     canvas.style.width = '50vw';
                     canvas.style.height = '50vh';
                     return canvas;
                }
            );
            element.append(output);
        }
        require(['Algebra'],function(Algebra){add_graph_to_notebook(Algebra)});
        """
    else:
        raise ValueError('Algebra not yet supported')
    return js


def generate_and_save_template(script_json, algebra='g3c'):
    # Convert json to html string
    template_string = generate_jinja_template(script_json, algebra=algebra)

    # Save with unique name based on hash
    endpointname = hashlib.sha224(template_string.encode('utf-8')).hexdigest()
    filename = endpointname + ".html"
    dir_name = os.path.dirname(os.path.abspath(__file__))
    fullname = dir_name + '/templates/' + filename
    with open(fullname, 'w') as f_obj:
        print(template_string, file=f_obj)
    return fullname, filename, endpointname


def render_notebook_script(script_json, algebra='g3c'):
    """
    In a notebook we dont need to start a flask server or cefpython as we
    are already in the browser!
    """
    js = generate_notebook_js(script_json, algebra=algebra)
    Javascript(js)


def render_cef_script(script_json="", script_tools=False):
    # First save the script string as a template
    if script_json != "":
        fullname, filename, endpointname = generate_and_save_template(script_json)
    else:
        endpointname = ""

    def run_cef_process():
        if script_tools:
            params = urllib.parse.urlencode({'show_tools': True})
        else:
            params = urllib.parse.urlencode({'show_tools': False})
        final_url = "http://localhost:5000/" + endpointname + "?%s" % params
        run_cef_gui(final_url, "pyganja")

    try:
        # Now run the flask server
        server = Process(target=run_app)
        cef_gui = Process(target=run_cef_process)
        server.start()
        # Wait a little to warm up
        time.sleep(1)
        cef_gui.start()
        # Clean up our mess
        cef_gui.join()
        server.terminate()
        server.join()

        if script_json != "":
            if os.path.isfile(fullname):
                os.remove(fullname)
    except:
        if script_json != "":
            if os.path.isfile(fullname):
                os.remove(fullname)


def nb_draw_objects(objects, color=int('AA000000', 16)):
    if isinstance(objects, list):
        sc = GanjaScene()
        sc.add_objects(objects, color=color)
        render_notebook_script(str(sc))
    else:
        raise ValueError('The input is not a list of objects')


def draw_objects(objects, color=int('AA000000', 16)):
    if isinstance(objects, list):
        sc = GanjaScene()
        sc.add_objects(objects, color=color)
        render_cef_script(str(sc))
    else:
        raise ValueError('The input is not a list of objects')
