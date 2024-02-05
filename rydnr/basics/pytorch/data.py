"""
rydnr/basics/pytorch/data.py

This file defines the Data class.

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
import matplotlib.pyplot as plt
from pythoneda.shared import BaseObject
import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
from typing import Tuple


class Data(BaseObject):
    """
    Notebook for the Data chapter in PyTorch tutorial:
    https://pytorch.org/tutorials/beginner/basics/data_tutorial.html

    Class name: Data

    Responsibilities:
        - Provide the code of the Data chapter.

    Collaborators:
        - None
    """

    def __init__(self):
        """
        Creates a new Data instance.
        """
        super().__init__()

    def create_data(self) -> Tuple:
        training_data = datasets.FashionMNIST(
            root="data", train=True, download=True, transform=ToTensor()
        )
        test_data = datasets.FashionMNIST(
            root="data", train=False, download=True, transform=ToTensor()
        )
        return (training_data, test_data)

    def show(self, trainingData):
        labels_map = {
            0: "T-Shirt",
            1: "Trouser",
            2: "Pullover",
            3: "Dress",
            4: "Coat",
            5: "Sandal",
            6: "Shirt",
            7: "Sneaker",
            8: "Bag",
            9: "Ankle Boot",
        }
        figure = plt.figure(figsize=(8, 8))
        cols, rows = 3, 3
        for i in range(1, cols * rows + 1):
            sample_idx = torch.randint(len(trainingData), size=(1,)).item()
            img, label = trainingData[sample_idx]
            figure.add_subplot(rows, cols, i)
            plt.title(labels_map[label])
            plt.axis("off")
            plt.imshow(img.squeeze(), cmap="gray")
        plt.show()

    def dataloader(self, trainingData, testData) -> Tuple:
        train_dataloader = DataLoader(trainingData, batch_size=64, shuffle=True)
        test_dataloader = DataLoader(testData, batch_size=64, shuffle=True)
        return (train_dataloader, test_dataloader)

    def show_dataloaders(self, trainingDataloader):
        train_features, train_labels = next(iter(trainingDataloader))
        print(f"Feature batch shape: {train_features.size()}")
        print(f"Labels batch shape: {train_labels.size()}")
        img = train_features[0].squeeze()
        label = train_labels[0]
        plt.imshow(img, cmap="gray")
        plt.show()
        print(f"Label: {label}")

    def main(self):
        training_data, test_data = self.create_data()
        # self.show(training_data)
        train_dataloader, test_dataloader = self.dataloader(training_data, test_data)

        self.show_dataloaders(train_dataloader)


if __name__ == "__main__":
    Data().main()


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
