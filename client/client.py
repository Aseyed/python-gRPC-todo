from proto import todo_pb2, todo_pb2_grpc
import os
import time
import grpc


def run(text):
    pid = os.getpid()
    with grpc.insecure_channel("localhost:5000") as channel:
        stub = todo_pb2_grpc.TasksStub(channel)
        try:
            start = time.time()
            # res = todo_pb2.Task()
            res = stub.Add(todo_pb2.Text(text=text))

            print(res.text)
            print(res.done)
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            channel.unsubscribe(close)
            exit(1)


def close(channel):
    channel.close()


if __name__ == '__main__':
    run("hello")
