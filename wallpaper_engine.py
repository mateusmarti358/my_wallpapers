from abc import ABC, abstractmethod


class WallpaperEngine(ABC):
    def get_name(self):
        return self.__class__.__name__

    @abstractmethod
    def is_running(self) -> bool:
        pass

    @abstractmethod
    def needs_to_preload(self) -> bool:
        pass

    @abstractmethod
    def listloaded(self) -> list[str]:
        pass

    @abstractmethod
    def preload(self, wallpaper):
        pass

    @abstractmethod
    def listactive(self) -> list[tuple[str, str]]:
        pass

    @abstractmethod
    def wallpaper(self, monitor_name: str, wallpaper_path):
        pass
