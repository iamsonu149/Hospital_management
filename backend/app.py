from application import create_app
from application.celery_init import celery_init_app

app = create_app()
celery_app = celery_init_app(app)
celery_app.autodiscover_tasks(["application"])
import application.tasks
if __name__ == "__main__":
    app.run(debug=True)
