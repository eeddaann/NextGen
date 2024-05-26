import time
from audio_helpers import save_spectrogram
from flask import (
    Flask, 
    jsonify,
    request,
    render_template
)
from flask_qrcode import QRcode
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from OpenSSL import SSL

# Function that create the app 
def create_app(test_config=None ):
    # create and configure the app
    app = Flask(__name__, static_url_path='/static')
    QRcode(app)

    # Simple route
    @app.route('/')
    def record():
        return render_template('index.html')
    
    @app.route('/qr')
    def qr():
        return render_template('qr.html')
    
    @app.route('/upload/audio/<perfix>', methods=['POST'])
    def uploadAudio(perfix):
        # Get params
        audio_file = request.files.get('audio_data')
        file_type = request.form.get("type", "mp3")

        # You may want to create a uuid for your filenames
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = "%s_%s.%s"%(perfix,timestr,file_type)

        # Save it on your local disk
        target_path = ("output/%s" % filename)
        audio_file.save(target_path)
        plot_data = save_spectrogram(target_path)

        return jsonify({"plot":plot_data})
        
    return app # do not foget to return the app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=3000, debug=False, ssl_context='adhoc')