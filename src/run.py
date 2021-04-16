from flaskapp import app  # from __init__.py
import os
from dotenv import load_dotenv

if __name__ == '__main__':
    # app.run(debug=True)  # Debug mode for development

    load_dotenv()
    app.run(host=os.getenv("HOST"), port=os.getenv("PORT"))
