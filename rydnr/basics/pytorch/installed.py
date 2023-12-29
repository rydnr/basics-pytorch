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
from pythoneda import BaseObject
import torch


class Installed(BaseObject):
    """
    Simple smoke test to check PyTorch is available.

    Class name: Installed

    Responsibilities:
        - Runs some smoke test.

    Collaborators:
        - None
    """

    def __init__(self):
        """
        Creates a new Installed instance.
        """
        super().__init__()
        x = torch.rand(5, 3)
        print(x)
