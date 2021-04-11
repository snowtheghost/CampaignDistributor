from flaskapp import app  # from __init__.py

if __name__ == '__main__':
    # app.run(debug=True)  # Debug mode for development
    app.run(host='192.168.2.10', port=9000)
