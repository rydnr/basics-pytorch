"""
rydnr/basics/pytorch/__init__.py

This file ensures rydnr.basics.pytorch is a namespace.

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
__path__ = __import__("pkgutil").extend_path(__path__, __name__)

from .custom_image_dataset import CustomImageDataset
from .data import Data
from .installed import Installed
from .quickstart import Quickstart
from .quickstart_neural_network import QuickstartNeuralNetwork
from .tensors import Tensors
