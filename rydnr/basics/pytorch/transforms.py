"""
rydnr/basics/pytorch/transforms.py

This file defines the Transforms class.

Copyright (C) 2024-today rydnr's https://github.com/rydnr/basics-pytorch

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
from torchvision import datasets
from torchvision.transforms import ToTensor, Lambda


class Transforms(BaseObject):
    """
    Notebook for the Transforms chapter in PyTorch tutorial:
    https://pytorch.org/tutorials/beginner/basics/transforms_tutorial.html

    Class name: Transforms

    Responsibilities:
        - Provide the code of the Transforms chapter.

    Collaborators:
        - None
    """

    def __init__(self):
        """
        Creates a new Transforms instance.
        """
        super().__init__()

    def create_data(self):
        return datasets.FashionMNIST(
            root="data",
            train=True,
            download=True,
            transform=ToTensor(),
            target_transform=Lambda(
                lambda y: torch.zeros(10, dtype=torch.float).scatter_(
                    0, torch.tensor(y), value=1
                )
            ),
        )

    def main(self):
        training_data = self.create_data()
        # self.show(training_data)


if __name__ == "__main__":
    Transforms().main()


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
