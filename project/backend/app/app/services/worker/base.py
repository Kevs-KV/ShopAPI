from celery import Task

from app.utils.application_builder.installation import ApplicationBuilderDatabaseComponents


class DatabaseTask(Task):
    _repositories = None

    @property
    def repositories(self) -> dict:
        if self._repositories is None:
            self._repositories = ApplicationBuilderDatabaseComponents().get_repositories()
        return self._repositories
