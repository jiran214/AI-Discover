import abc


class NoteSpider(abc.ABC):

    @abc.abstractmethod
    def get_note_search_list(self, query, top_n, *args, **kwargs): ...

    @abc.abstractmethod
    def get_note_detail(self, note_id): ...

    @abc.abstractmethod
    def get_note_summary(self, note_id): ...

    @abc.abstractmethod
    def get_notes(self, *args, **kwargs): ...

