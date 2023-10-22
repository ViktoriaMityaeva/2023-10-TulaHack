from celery import Celery

# Create a Celery instance
celery = Celery('helloworld', broker='redis://redis:6379/0')

# Define a task
@celery.task
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    celery.start()