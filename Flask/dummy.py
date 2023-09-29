# from flask import Flask
# from flask_restful import Resource, Api
# import time
# import threading

# app = Flask(__name__)
# api = Api(app)

# def task(msg):
#     print("started task for ", msg)
#     time.sleep(5)
#     print("completed task for ", msg)

# class HelloWorld(Resource):
#     def post(self):
#         msg = "REST API"
#         threading.Thread(target=task).start()
#         return {"message":"Main fucntion compelted"}
    
# api.add_resource(HelloWorld, '/load')

# if __name__ == '__main__':
#     app.run(debug=True)