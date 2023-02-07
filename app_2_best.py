from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import sqlite3

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/')
@cross_origin(origin="*",supports_credentials=True)
def hello_world():
	return "All OK!"

@app.route("/polygons", methods=["GET", "POST"])
@cross_origin(origin="*",supports_credentials=True)
def polyggon_handler():
    if request.method == "GET":
        polygs = get_all_polygons()
        return jsonify(polygons=polygs)
    elif request.method == "POST":
        polygon = request.get_json()
        save_polygon(polygon)
        return "OK", 201

@app.route("/polygons/<int:poly_id>", methods=["GET", "PUT", "DELETE"])
@cross_origin(origin="*",supports_credentials=True)
def single_polygon_handler(poly_id):
    if request.method == "GET":
        poly = get_polygon(poly_id)
        return jsonify(polygon=poly)
    elif request.method == "PUT":
        polygon = request.get_json()
        update_polygon(poly_id, polygon)
        return "OK", 200
    elif request.method == "DELETE":
        delete_polygon(poly_id)
        return "OK", 200

def get_all_polygons():
    conn = sqlite3.connect("polygons.db")
    c = conn.cursor()
    c.execute("SELECT * FROM polygon")
    polys = c.fetchall()
    conn.close()
    return polys

def get_polygon(poly_id):
    conn = sqlite3.connect("polygons.db")
    c = conn.cursor()
    c.execute("SELECT * FROM polygon WHERE id=?", (poly_id,))
    poly = c.fetchone()
    conn.close()
    return poly

def save_polygon(polygon):
    conn = sqlite3.connect("polygons.db")
    c = conn.cursor()
    c.execute("INSERT INTO polygon (name, coordinates) VALUES (?, ?)", (polygon["name"], polygon["coordinates"]))
    conn.commit()
    conn.close()

def update_polygon(poly_id, polygon):
    conn = sqlite3.connect("polygons.db")
    c = conn.cursor()
    c.execute("UPDATE polygon SET name=?, coordinates=? WHERE id=?", (polygon["name"], polygon["coordinates"], poly_id))
    conn.commit()
    conn.close()

def delete_polygon(poly_id):
    conn = sqlite3.connect("polygons.db")
    c = conn.cursor()
    c.execute("DELETE FROM polygon WHERE id=?", (poly_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    app.run(debug=True)
