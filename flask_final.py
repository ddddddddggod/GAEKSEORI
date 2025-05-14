import RPi.GPIO as GPIO
import time
from flask import Flask, render_template, url_for, redirect
app = Flask(__name__)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# variables
StepPins = [11, 13, 15, 16]
A1A = 23

GPIO.setup(StepPins, GPIO.OUT)
GPIO.setup(A1A, GPIO.OUT)


def setStep(degrees):
    steps_per_revolution = 200
    steps = degrees / 360.0 * steps_per_revolution
    delay = 0.01

    return (int(steps), delay)


def forward(degrees):
    (steps, delay) = setStep(degrees)
    for i in range(steps):
        for pin in range(4):
            if i % 4 == pin:
                GPIO.output(StepPins[pin], True)
            else:
                GPIO.output(StepPins[pin], False)
        time.sleep(delay)

    for pin in range(4):
        GPIO.output(StepPins[pin], False)


def backward(degrees):
    (steps, delay) = setStep(degrees)
    for i in range(steps, 0, -1):
        for pin in range(4):
            if i % 4 == pin:
                GPIO.output(StepPins[pin], True)
            else:
                GPIO.output(StepPins[pin], False)
        time.sleep(delay)
    for pin in range(4):
        GPIO.output(StepPins[pin], False)


@app.route('/')
def hello():
    return render_template('main.html')


@app.route('/forward')
def forward_handler():
    forward(90)
    return redirect(url_for('hello'))


@app.route('/backward')
def backward_handler():
    backward(90)
    return redirect(url_for('hello'))


@app.route('/on')
def on_handler():
    GPIO.output(A1A, GPIO.HIGH)
    return redirect(url_for('hello'))


@app.route('/off')
def off_handler():
    GPIO.output(A1A, GPIO.LOW)
    return redirect(url_for('hello'))


if __name__ == "__main__":
    app.run(debug="True", host="0.0.0.0")
