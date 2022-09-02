from app import create_app, pokify_util

app = create_app()

if __name__ == '__main__':
    pokify_util.configure()
    app.run(debug=True)

