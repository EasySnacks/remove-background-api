#!/usr/bin/env python3
from flask import Flask, Response, request
from flask_cors import CORS
from PIL import Image
from rembg import new_session, remove
import io

app = Flask(__name__)
CORS(app)


@app.post('/api/rem-bg')
def remBg():
    auth = request.headers.get('Authorization', None)
    if not auth or not auth.startswith('Bearer '):
        return Response(status=401)
    auth = auth.removeprefix('Bearer ')
    with open('keys', 'r') as f:
        if not auth.strip() in [l.strip() for l in f.readlines()]:
            return Response(status=401)

    try:
        image = request.get_data(True, False, False)
        content_type = request.headers.get('Content-Type', '')
        image_kind = [content_type.split('/', 2)[1]] if '/' in content_type else None

        image = Image.open(io.BytesIO(image), formats=image_kind)
        image = remove(image, post_process_mask=True)
        body = io.BytesIO()
        image.save(body, format='PNG')
        return Response(body.getvalue(), status=200, content_type='image/png')
    except BaseException as e:
        return Response(repr(e), status=400, content_type='text/plain')


if __name__ == "__main__":
    app.run(debug=True)
