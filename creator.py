from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import fire

# focused imports
from big_sleep import Imagine
import torch

# default options, overridable from the command line
default_http_address = '127.0.0.1'
default_http_port = 5000


def initial_test():
    text = 'puppy with purple eyes'
    imagine = Imagine(
        text=text,
        lr=.07,
        save_every=10,
        open_folder=True,
        epochs=1,
        iterations=10,
        bilinear=False,
        image_size=256,
        save_progress=True,
        seed=False,
        torch_deterministic=False,
    )
    imagine()
    imagine.reset()
    del imagine.model
    del imagine.optimizer
    del imagine


# Main()
def run_app(http_host=default_http_address, http_port=default_http_port):
    # configure Flask for serving
    print(f'# Starting HTTP endpoint on {http_host}:{http_port}')
    app = Flask(__name__, template_folder='web')
    app.logger.setLevel(20)
    socket_io = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins='*')
    print()

    # test out app functionality at start
    # initial_test()

    @app.route('/')
    def index():
        return render_template('index.html')

    @socket_io.on('json')
    def handle_my_json_event(json):
        print('received json: ' + str(json))

    @socket_io.on('my_event')
    def handle_my_message_event(data):
        print('received message: ' + str(data))
        emit('my_response', {'data': f'{data}'})

    @socket_io.on('connect')
    def test_connect():
        print('Client connected')
        emit('my response', {'data': 'Connected'})

    @socket_io.on('disconnect')
    def test_disconnect():
        print('Client disconnected')

    # start sever
    socket_io.run(app, host=http_host, port=http_port)


if __name__ == '__main__':
    fire.Fire(run_app)
