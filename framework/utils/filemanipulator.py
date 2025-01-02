import os
import pathlib as pl
import wx
import shutil


class FileManipulator(wx.FileSystem):
    def __init__(self,  filepath: str):
        super().__init__()
        if filepath is None:
            filepath = os.path.dirname(__file__)
        self.ChangePathTo(filepath, True)
        self.__watcher = wx.FileSystemWatcher()
        self.__watcher.Add(filepath)

    @property
    def watcher(self) -> wx.FileSystemWatcher:
        return self.__watcher

    def change_path_to(self, location: str, is_dir: bool) -> None:
        self.__watcher.RemoveAll()
        self.ChangePathTo(location, is_dir)
        self.__watcher.Add(location)

    def listdir(self, is_absolute: bool = False) -> list:
        files = os.listdir(self.GetPath())
        return files if not is_absolute else [self.GetPath() + file for file in files]

    def get_absolute_path(self, file: str) -> str:
        return self.GetPath() + file if file in self.listdir() else ''

    def delete_file(self, filepath: str) -> None:
        if self.is_dir(filepath):
            shutil.rmtree(filepath, ignore_errors=True)
        else:
            os.remove(filepath)

    @staticmethod
    def open_file(filepath: str) -> None:
        os.startfile(filepath)

    @staticmethod
    def is_dir(filepath: str) -> bool:
        return pl.Path(filepath).is_dir()

    @staticmethod
    def is_file(filepath: str) -> bool:
        return pl.Path(filepath).is_file()
