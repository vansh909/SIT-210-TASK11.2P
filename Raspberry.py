import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# MQTT broker details
broker_address = "broker.hivemq.com"
port = 1883
topic = "PhValuezzz"

# GPIO pins for servo motors
SERVO_PIN_1 = 17  # GPIO pin for servo 1
SERVO_PIN_2 = 18  # GPIO pin for servo 2
FEEDER_PIN = 27  # GPIO pin for the feeder servo

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN_1, GPIO.OUT)
GPIO.setup(SERVO_PIN_2, GPIO.OUT)
GPIO.setup(FEEDER_PIN, GPIO.OUT)

# Servo PWM initialization
pwm = GPIO.PWM(SERVO_PIN_1, 50)  # 50 Hz frequency
pwm_2 = GPIO.PWM(SERVO_PIN_2, 50)  # 50 Hz frequency
pwm_3 = GPIO.PWM(FEEDER_PIN, 50)  # 50 Hz frequency

# Start PWM with 0 duty ycle (off)

#servo_pwm_2.start(0)
#feeder_pwm.start(0)

# Function to control servo 1
def control_servo_1():
    action_label.config(text="Dispensing Sodium Bicarbonate for maintaining the pH")
    # Simulate servo control for dispensing reagent for pH below 7
    # Adjust duty cycle as needed for your servo and setup
   # servo_pwm_1.ChangeDutyCycle(7)
    # Change duty cycle for appropriate movement
    # Move from 0 to 180 degrees
    pwm.start(0)
    for dc in range(0, 181, 5):
        pwm.ChangeDutyCycle(dc / 18 + 2)

        # Pause at 180 degrees for 2 seconds
    time.sleep(1)

        # Move from 180 to 0 degrees
    for dc in range(180, -1, -5):
        pwm.ChangeDutyCycle(dc / 18 + 2)
            

        # Pause at 0 degrees for 2 seconds
    time.sleep(1)
    

# Function to control servo 2
def control_servo_2():
    action_label.config(text="Dispensing Citric Acid for maintaining the ph")
    # Simulate servo control for dispensing reagent for pH above 8
    # Adjust duty cycle as needed for your servo and setup
    #servo_pwm_2.ChangeDutyCycle(7)  # Change duty cycle for appropriate movement
    pwm_2.start(0)
    for dc in range(0, 181, 5):
        pwm_2.ChangeDutyCycle(dc / 18 + 2)

        # Pause at 180 degrees for 2 seconds
    time.sleep(1)

        # Move from 180 to 0 degrees
    for dc in range(180, -1, -5):
        pwm_2.ChangeDutyCycle(dc / 18 + 2)
            

        # Pause at 0 degrees for 2 seconds
    time.sleep(1)

# Function to control the feeder
def control_feeder():
    action_label.config(text="Feed fishes")
    # Simulate servo control for the feeder
    # Adjust duty cycle as needed for your servo and setup
    #feeder_pwm.ChangeDutyCycle(7)  # Change duty cycle for appropriate movement
    pwm_3.start(0)
    for dc in range(0, 181, 5):
        pwm_3.ChangeDutyCycle(dc / 18 + 2)

        # Pause at 180 degrees for 2 seconds
    time.sleep(1)

        # Move from 180 to 0 degrees
    for dc in range(180, -1, -5):
        pwm_3.ChangeDutyCycle(dc / 18 + 2)
            

        # Pause at 0 degrees for 2 seconds
    time.sleep(1)
   # pwm_3.start(0)

# MQTT callback when a message is received
def on_message(client, userdata, message):
    ph_value = float(message.payload.decode("utf-8"))
    update_ph_label(ph_value)
    if ph_value < 6:
        control_servo_1()
    elif ph_value > 8:
        control_servo_2()
    #
        

# Function to update the pH label in the GUI
def update_ph_label(value):
    ph_label.config(text="pH Value: {:.2f}".format(value))

# Create an MQTT client
client = mqtt.Client()
client.on_message = on_message
client.connect(broker_address, port)
client.subscribe(topic)
client.loop_start()

# GUI setup
root = tk.Tk()
root.title("pH Value Display")

# Set the style
style = ttk.Style()
style.configure("TLabel", font=("Arial", 24), padding=10)
style.configure("TFrame", background="#F0F0F0")
style.configure("TButton", font=("Arial", 18), padding=10, width=20)

# pH label
ph_label = ttk.Label(root, text="pH Value: ")
ph_label.pack(pady=20)

# Action label
action_label = ttk.Label(root, text="")
action_label.pack(pady=10)

# Add a frame for better layout
frame = ttk.Frame(root, style="TFrame")
frame.pack(pady=20)

# Dispense button for feeder
feeder_button = ttk.Button(frame, text="Dispense Feeder", command=control_feeder, style="TButton")
feeder_button.grid(row=0, column=0, padx=10, pady=10)

# Start the GUI main loop
root.mainloop()
