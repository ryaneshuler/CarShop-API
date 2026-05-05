from app import create_app

app = create_app('DevelopmentConfig')

if __name__ == '__main__':
    app.run(port=5001, debug=True)