from abc import ABC, abstractmethod


class IRAG(ABC) :

    @abstractmethod
    def generate_response(query : str, context : str ) -> str:
        pass