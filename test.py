import os
import streamlit as st 
from pathlib import Path
import image_recognition
import sqlite3

conn = sqlite3.connect("test.db", isolation_level=None)


with open("/Users/maddoxsciuchetti/p-BSB/Handwerk_vision.py/sources/Bildschirmfoto 2025-10-29 um 15.38.36.png", "rb") as file: 
    image_data = file.read()
    conn.execute('INSERT INTO documents (title, data) VALUES (?,?)', ("image", image_data))

conn.execute("SELECT data FROM documents WHERE id=1")
data = conn.execute('SELECT image documents Data').fetchall()

with open('stored_image.jpg', "wb") as file: 
    file.write(data)





