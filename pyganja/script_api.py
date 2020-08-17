from __future__ import print_function

import os
import json
import base64
from multiprocessing import Process
import hashlib
import webbrowser
import warnings

from .GanjaScene import GanjaScene

from .color import Color

CEFAVAILABLE = False
try:
    from .cefwindow import *
    CEFAVAILABLE = True
except:
    warnings.warn(
        'Failed to import cef_gui, cef functions will be unavailable',
        stacklevel=2)

JUPYTERAVAILABLE = False
try:
    from IPython.display import display, Javascript
    from IPython import get_ipython
    JUPYTERAVAILABLE = True
except:
    warnings.warn(
        'Failed to import ipython, notebook rendering will be unavailable',
        stacklevel=2)


def html_to_data_uri(html):
    html = html.encode("utf-8", "replace")
    b64 = base64.b64encode(html).decode("utf-8", "replace")
    ret = "data:text/html;base64,{data}".format(data=b64)
    return ret


def read_ganja():
    dir_name = os.path.dirname(os.path.abspath(__file__))
    ganja_filename = dir_name + '/static/ganja.js/ganja.js'
    with open(ganja_filename, 'r', encoding='utf8') as ganja_file:
        output = ganja_file.read()
    return output


def generate_notebook_js(scene, sig=None, *,
                         default_color=Color.DEFAULT, default_static=False, **kwargs):
    script_json = _to_scene_string(scene, default_color=default_color, default_static=default_static)
    if sig is not None:
        p = (sig > 0).sum().item()  # convert to json-compatible scalar
        q = (sig < 0).sum().item()  # convert to json-compatible scalar
        r = len(sig) - p - q
    else:
        p = 4
        q = 1
        r = 0
    mv_length = str(2 ** (p + q + r))

    # not the best way to test conformal, as it prevents non-euclidean  geometry
    if q != 0:
        conformal = True
    else:
        conformal = False

    if (p, q, r) in [(4, 1, 0), (3, 1, 0), (3, 0, 0), (3, 0, 1)]:
        opts = dict(
            p=p, q=q, r=r, mv_length=mv_length,
            graph=dict(
                conformal=conformal,
                gl=True,
                useUnnaturalLineDisplayForPointPairs=True,
            )
        )
        if p - q == 2:
            kwargs['gl'] = False  # 2d
        opts["graph"].update(kwargs)
        js = """
        // We load ganja.js with requireJS, since `module.exports` / require
        // only work if things are in separate files. In most situations
        // `module` is already undefined, but in VSCode is is not (gh-46).
        // Explicitly clearing it makes ganja.js fall back to RequireJS.
        let module = undefined;
        """
        js += read_ganja()
        js += """
        // take a closure on element before the next cell replaces it
        (function(element) {
            (requirejs||require)(['Algebra'], function(Algebra) {
                var opts = """ + json.dumps(opts) + """;  // injected from python
                var output = Algebra({p: opts.p, q: opts.q, r: opts.r, baseType: Float64Array}).inline((opts)=>{
                    var data = """ + script_json + """;  // injected from python

                    // When we get a file, we load and display.
                    var canvas;
                    var h=0, p=0;
                    // convert arrays of floats back to CGA elements.
                    data = data.map(x=>x.length==opts.mv_length?new Element(x):x);
                    // add the graph to the page.
                    canvas = this.graph(data, opts.graph);
                    canvas.options.h = h;
                    canvas.options.p = p;
                    // make it big.
                    canvas.style.width = '100%';
                    canvas.style.height = '50vh';
                    return canvas;
                })(opts);
                element.append(output);

                var a = document.createElement("button");
                var t = document.createTextNode("\N{FLOPPY DISK} Save");
                a.appendChild(t);
                function screenshot(){
                    //output.width = 1920;  output.height = 1080;
                    output.update(output.value);
                    output.toBlob(function(blob) {
                        var url = URL.createObjectURL(blob);
                        window.open(url, '_blank');
                    });
                }
                window.addEventListener('resize', function() {
                    output.update(output.value);
                });
                a.onclick = screenshot
                var butnelem = element.append(a);
            });
        })(element);
        """
    else:
        raise ValueError('Algebra not yet supported')
    return Javascript(js)


def generate_full_html(scene, sig=None, grid=True, scale=1.0, gl=True,
                       default_color=Color.DEFAULT, default_static=False):
    script_json = _to_scene_string(scene, default_color=default_color, default_static=default_static)
    if sig is not None:
        p = (sig > 0).sum()
        q = (sig < 0).sum()
        r = len(sig) - p - q
    else:
        p = 4
        q = 1
        r = 0
    sig_short = '%i,%i,%i' % (p, q, r)
    print(sig_short)
    mv_length = str(2 ** (p + q + r))

    # not the best way to test conformal, as it prevents non-euclidean  geometry
    conformal = 'false'
    if q!=0:
        conformal = 'true'

    if sig_short in ['4,1,0', '3,0,0', '3,0,1']:
        if grid:
            gridstr = 'true'
        else:
            gridstr = 'false'
        scalestr = str(scale)

        script_string = """
                Algebra("""+sig_short+""",()=>{
                  var canvas = this.graph((""" + script_json + """).map(x=>x.length=="""+mv_length+"""?new Element(x):x),
                  {conformal:"""+conformal+""",gl:"""+str(gl).lower()+""",grid:"""+gridstr+""",scale:"""+scalestr+""",useUnnaturalLineDisplayForPointPairs:true});
                  canvas.style.width = '100vw';
                  canvas.style.height = '100vh';
                  document.body.appendChild(canvas);
                });
                """
        full_html = """<!DOCTYPE html>
        <html lang="en" style="height:100%;">
        <HEAD>
            <meta charset="UTF-8">
            <title>pyganja</title>
            <SCRIPT>""" + read_ganja() + """</SCRIPT>
        </HEAD>
        <BODY style="position:absolute; top:0; bottom:0; right:0; left:0; overflow:hidden;">
        <SCRIPT>
            """ + script_string + """
        </SCRIPT>
        </BODY>
        </html>
        """
        return full_html
    else:
        raise ValueError('Algebra not yet supported')


def render_browser_script(scene, sig=None, *, filename=None,
                          default_color=Color.DEFAULT, default_static=False, **kwargs):
    """
    If we have no jupyter and no cefpython we will be forced to generate html
    and render that in the users browser
    """
    html_code = generate_full_html(
        scene, sig=sig, default_color=default_color, default_static=default_static, **kwargs)
    if filename is None:
        hash_object = hashlib.md5(html_code.encode())
        filename = hash_object.hexdigest() + '.html'
    with open(filename, 'w', encoding='utf8') as fo:
        print(html_code,file=fo)
    webbrowser.open(filename)


def render_notebook_script(scene, sig=None, **kwargs):
    """
    In a notebook we dont need to start cefpython as we
    are already in the browser!
    """
    js = generate_notebook_js(scene, sig=sig, **kwargs)
    display(js)


def render_cef_script(scene="", sig=None, **kwargs):
    def render_script():
        final_url = html_to_data_uri(generate_full_html(scene, sig=sig, **kwargs))
        run_cef_gui(final_url, "pyganja")
    p = Process(target=render_script)
    p.start()
    p.join()


def isnotebook():
    # See:
    # https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


def draw(objects, color=Color.DEFAULT, sig=None, *,
         browser_window=False, new_window=False, static=False, **kwargs):
    kwargs = dict(sig=sig, default_color=color, default_static=static, **kwargs)
    if JUPYTERAVAILABLE and isnotebook() and not new_window:
        render_notebook_script(objects, **kwargs)
    elif CEFAVAILABLE and not browser_window:
        render_cef_script(objects, **kwargs)
    else:
        render_browser_script(objects, **kwargs)


def _to_scene_string(objects, default_color=Color.DEFAULT, default_static=False):
    if isinstance(objects, list):
        sc = GanjaScene()
        sc.add_objects(objects, color=default_color, static=default_static)
        return str(sc)
    elif isinstance(objects, str):
        return objects
    elif isinstance(objects, GanjaScene):
        return str(objects)
    else:
        sc = GanjaScene()
        try:
            print('Treating as iterable')
            sc.add_objects([i for i in objects], color=default_color, static=default_static)
            return str(sc)
        except Exception:
            raise ValueError('The input cannot be interpreted, it is not a list of objects or ganja scene')
