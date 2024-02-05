"""
rydnr/basics/pytorch/build_model.py

This file defines the BuildModel class.

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
import os
from pythoneda.shared import BaseObject
from rydnr.basics.pytorch import QuickstartNeuralNetwork
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


class BuildModel(BaseObject):
    """
    Notebook for the "Build the Neural Network" chapter in PyTorch tutorial:
    https://pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html

    Class name: BuildModel

    Responsibilities:
        - Provide the code of the "Build the Neural Network" chapter.

    Collaborators:
        - None
    """

    def __init__(self):
        """
        Creates a new BuildModel instance.
        """
        super().__init__()

    def get_device(self):
        return (
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )

    def create_model(self, device):
        return QuickstartNeuralNetwork().to(device)

    def predict(self, model, device):
        X = torch.rand(1, 28, 28, device=device)
        logits = model(X)
        pred_probab = nn.Softmax(dim=1)(logits)
        return pred_probab.argmax(1)

    def random_minibatch(self):
        return torch.rand(3, 28, 28)

    def image_to_array(self, image):
        flatten = nn.Flatten()
        return flatten(image)

    def linear_flat_image(self, flatImage):
        layer1 = nn.Linear(in_features=28 * 28, out_features=20)
        return layer1(flatImage)

    def nonlinear(self, layer):
        return nn.ReLU()(layer)

    def sequence(self):
        return nn.Sequential(
            nn.Flatten(),
            nn.Linear(in_features=28 * 28, out_features=20),
            nn.ReLU(),
            nn.Linear(20, 10),
        )

    def softmax(self):
        return nn.Softmax(dim=1)

    def main(self):
        device = self.get_device()
        model = self.create_model(device)
        # self.predict(model, device)
        # self.random_minibatch()
        # input_image = self.random_minibatch()
        # flat_image = self.image_to_array(input_image)
        # hidden1 = self.linear_flat_image(flat_image)
        # hidden1 = self.nonlinear(hidden1)
        # logits = self.sequence()(input_image)
        # pred_probab = self.softmax()(logits)

        print(f"Model structure: {model}\n\n")

        for name, param in model.named_parameters():
            print(f"Layer: {name} | Size: {param.size()} | Values : {param[:2]} \n")


if __name__ == "__main__":
    BuildModel().main()


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
