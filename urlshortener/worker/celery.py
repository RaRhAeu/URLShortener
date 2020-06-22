from celery import Celery


def init_app(self, app):
    self.name = app.import_name
    self.config_from_object(app.config)
    self.conf.timezone = 'UTC'
    TaskBase = self.Task

    class ContextTask(TaskBase):

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    self.Task = ContextTask


celery = Celery()
Celery.init_app = init_app
