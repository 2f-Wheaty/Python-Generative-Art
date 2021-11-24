import os
from io import BytesIO
from flask import Flask, Response, request, abort, render_template_string, send_from_directory
from PIL import Image

app = Flask(__name__)

WIDTH = 128
HEIGHT = 128
TEMPLATE_CARD = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Generative Art Showcase</title>
        <meta charset="utf-8"/>
        <style>
        body {
            margin: 0;
            background-color: #333;
        }
        .image {
            display: block;
            margin: 2em auto;
            background-color: #444;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
        }
        img {
            display: block;
        }
        h1 {
            text-align:center;
        }
        </style>
        <script src="https://code.jquery.com/jquery-1.10.2.min.js" charset="utf-8"></script>
        <script src="jquery.unveil.js" charset="utf-8"></script>
        <script>
            $(document).ready(function() {
                $('img').unveil();
            });
        </script>
    </head>
    <body>
        {% for image in images %}
            <a class="image" href="{{ image.src }}" style="width: {{ image.width }}px; height: {{ image.height }}px">
                <img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-src="{{ image.src }}?w={{ image.width }}&amp;h={{ image.height }}" width="{{ image.width }}" height="{{ image.height }}" />
            </a>
        {% endfor %}
    </body>
'''

TEMPLATE_MAIN = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Generative Art Showcase</title>
        <meta charset="utf-8"/>
        <style>
        body {
            margin: 0;
            background-color: #333;
        }
        .image {
            display: block;
            margin: 2em auto;
            background-color: #444;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
        }
        img {
            display: block;
        }
        h1 {
            text-align:center;
        }
        </style>
        <script src="https://code.jquery.com/jquery-1.10.2.min.js" charset="utf-8"></script>
        <script src="jquery.unveil.js" charset="utf-8"></script>
        <script>
            $(document).ready(function() {
                $('img').unveil();
            });
        </script>
    </head>
    <body>
        {% for image in images %}
            <a class="image" href="{{ image.src }}" style="width: {{ image.width }}px; height: {{ image.height }}px">
                <img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-src="{{ image.src }}?w={{ image.width }}&amp;h={{ image.height }}" width="{{ image.width }}" height="{{ image.height }}" />
            </a>
        {% endfor %}
    </body>
'''

@app.route('/<path:filename>')
def image(filename):
    try:
        w = int(request.args['w'])
        h = int(request.args['h'])
    except (KeyError, ValueError):
        return send_from_directory('.', filename)

    try:
        im = Image.open(filename)
        im.thumbnail((w, h), Image.ANTIALIAS)
        io = BytesIO()
        im.save(io, format='PNG')
        return Response(io.getvalue(), mimetype='image/jpeg')

    except IOError:
        abort(404)

    return send_from_directory('.', filename)

@app.route('/')
def index():
    images = []
    for root, dirs, files in os.walk('.'):
        for filename in [os.path.join(root, name) for name in files]:
            if not filename.endswith('.png'):
                continue
            if 'preview' in filename.replace('/', ' '):
              continue
            else:
              WIDTH = 128
              HEIGHT = 128
            im = Image.open(filename)
            w, h = im.size
            aspect = 1.0*w/h
            if aspect > 1.0*WIDTH/HEIGHT:
                width = min(w, WIDTH)
                height = width/aspect
            else:
                height = min(h, HEIGHT)
                width = height*aspect
            filename1 = filename.replace('_', ' ').replace('.', ' ')
            num = [int(i) for i in filename1.split() if i.isdigit()]
            num = num[0]
            collection = 'MainCollection'
            if int(num) >= 10:
              if int(num) < 100:
                f = open(f'collection_output/{collection}/meta/0{num}.json', 'r')
              else:
                if int(num) == 274:
                  pass
                else:
                  f = open(f'collection_output/{collection}/meta/{num}.json', 'r')
            else:
              f = open(f'collection_output/{collection}/meta/00{num}.json', 'r')
            # r = f.read()
            name = f.readline()
            name = f.readline()
            name = print(str(f.readline().split('"')[3]).lower())
            name = 'test'
            images.append({
                'width': int(width),
                'height': int(height),
                'src': filename,
            })

    return render_template_string(TEMPLATE_MAIN, **{
        'images': images,
        'name': name,
    })

@app.route('/help')
def cards():
  data = []
  return render_template_string(TEMPLATE_MAIN, **{
        'data': data,
    })



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="443")
