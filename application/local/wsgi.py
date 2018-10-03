from app import app as webapp

if __name__ == "__main__":
    webapp.run(host=webapp.config["LISTENING_HOST"],
            port=int(webapp.config["LISTENING_PORT"]))
