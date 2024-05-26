import random
import time

from flask import Flask

app = Flask(__name__)


@app.route('/success')
def success_endpoint():
    return {
        "message": "Chamada realizada com sucesso."
    }, 200


@app.route('/failure')
def faulty_endpoint():
    r = random.randint(0, 1)
    if r == 0:
        time.sleep(2)

    return {
        "message": "Falhou."
    }, 500


@app.route('/random')
def fail_randomly_endpoint():
    r = random.randint(0, 1)
    if r == 0:
        return {
            "message": "Chamada realizada com sucesso."
        }, 200

    return {
        "message": "Falhou (algumas vezes)."
    }, 500