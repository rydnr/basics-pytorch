# vim: set fileencoding=utf-8
"""
pythoneda/tools/artifact/new_domain/new_domain.py

This file defines the NewDomain class.

Copyright (C) 2024-today rydnr's pythoneda-tools-artifact/new-domain

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
from torch import nn


class QuickstartNeuralNetwork(nn.Module):
    """
    Defines the NeuralNetwork used in PyTorch's quickstart tutorial: https://pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html

    Class name: QuickstartNeuralNetwork

    Responsibilities:
        - Define the topology of a neural network.

    Collaborators:
        - None
    """

    _token = None

    def __init__(self):
        """
        Creates a new QuickstartNeuralNetwork instance.
        """
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28 * 28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
