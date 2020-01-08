from proto import todo_pb2, todo_pb2_grpc
from concurrent import futures
import threading
import time
import grpc


class Listener(todo_pb2_grpc.TasksServicer):
    isLeaf = True

    def __init__(self):
        self.counter = 0
        self.lastTime = time.time()

    def Add(self, request, context):
        self.counter += 1
        print(self.counter)
        print(request.text)
        my_task = todo_pb2.Task(text=request.text, done=False)
        return my_task

    @staticmethod
    def render_GET(request):
        task = todo_pb2.Task()
        task.text = 'Hello There!'
        task.done = True
        return task.SerializeToString()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))  # TODO what is worker
    todo_pb2_grpc.add_TasksServicer_to_server(Listener(), server)

    server.add_insecure_port('[::]:5000')  # TODO search about pattern
    server.start()

    try:
        while True:
            print("server on: threads %i" % (threading.active_count()))
            time.sleep(10)
    except KeyboardInterrupt:
        print("keyboard interrupt")
        server.stop(0)


if __name__ == "__main__":
    serve()
