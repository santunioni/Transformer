from dotenv import load_dotenv, find_dotenv

from src.app import app

if __name__ == "__main__":
    load_dotenv(find_dotenv("local.env"))
    app.start()
