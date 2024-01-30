"""
rydnr/basics/pytorch/installed.py

This file defines the Installed class.

Copyright (C) 2023-today rydnr's https://github.com/rydnr/basics-pytorch

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from pythoneda.shared import BaseObject
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor


class Quickstart(BaseObject):
    """
    Shows common tasks.

    Class name: Quickstart

    Responsibilities:
        - Shows common tasks.

    Collaborators:
        - None
    """

    def __init__(self):
        """
        Creates a new Installed instance.
        """
        super().__init__()

    def download_training_data_from_open_datasets(self):
        training_data = datasets.FashionMNIST(
            root="data",
            train=True,
            download=True,
            transform=ToTensor(),
        )


if __name__ == "__main__":
    Quickstart().download_training_data_from_open_datasets()
