"""
rydnr/basics/pytorch/tensors.py

This file defines the Tensors class.

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
import numpy as np
import torch


class Tensors(BaseObject):
    """
    Notebook for the Tensors chapter in PyTorch tutorial:
    https://pytorch.org/tutorials/beginner/basics/tensors_tutorial.html

    Class name: Tensors

    Responsibilities:
        - Provide the code of the Tensors chapter.

    Collaborators:
        - None
    """

    def __init__(self):
        """
        Creates a new Tensors instance.
        """
        super().__init__()

    def create_data(self):
        data = [[1, 2], [3, 4]]
        x_data = torch.tensor(data)
        x_ones = torch.ones_like(x_data)
        print(x_ones)
        x_rand = torch.rand_like(x_data, dtype=torch.float)
        print(x_rand)

    def create_data_from_numpy(self):
        data = [[1, 2], [3, 4]]
        np_array = np.array(data)
        x_np = torch.from_numpy(np_array)
        print(x_np)

    def shape(self):
        shape = (
            2,
            3,
        )
        rand_tensor = torch.rand(shape)
        ones_tensor = torch.ones(shape)
        zeros_tensor = torch.zeros(shape)

        print(rand_tensor)
        print(ones_tensor)
        print(zeros_tensor)

    def attributes(self):
        tensor = torch.rand(3, 4)
        if torch.cuda.is_available():
            tensor = tensor.to("cuda")
        print(f"shape: {tensor.shape}")
        print(f"datatype: {tensor.dtype}")
        print(f"device: {tensor.device}")

    def indexing(self):
        tensor = torch.ones(4, 4)
        print(f"First row: {tensor[0]}")
        print(f"First column: {tensor[:, 0]}")
        print(f"Last column: {tensor[..., -1]}")
        tensor[:, 1] = 0
        print(tensor)

    def concat(self):
        tensor = torch.rand(4, 4)
        ones = torch.ones(4, 4)
        zeros = torch.zeros(4, 4)
        print(torch.cat([tensor, zeros, ones], dim=1))

    def matmul(self):
        tensor = torch.rand(4, 4)
        # This computes the matrix multiplication between two tensors. y1, y2, y3 will have the same value
        # ``tensor.T`` returns the transpose of a tensor
        y1 = tensor @ tensor.T
        y2 = tensor.matmul(tensor.T)
        y3 = torch.rand_like(y1)
        print(tensor)
        torch.matmul(tensor, tensor.T, out=y3)
        print(y3)

    def mul(self):
        tensor = torch.rand(4, 4)
        # This computes the element-wise product. z1, z2, z3 will have the same value
        z1 = tensor * tensor
        z2 = tensor.mul(tensor)
        z3 = torch.rand_like(tensor)
        print(tensor)
        torch.mul(tensor, tensor, out=z3)
        print(z3)

    def item(self):
        tensor = torch.rand(4, 4)
        agg = tensor.sum()
        agg_item = agg.item()
        print(agg_item, type(agg_item))

    def inplace(self):
        tensor = torch.rand(4, 4)
        print(tensor)
        tensor.add_(5)
        print(tensor)

    def to_numpy(self):
        t = torch.ones(5)
        n = t.numpy()
        t.add_(1)
        print(f"t: {t}")
        print(f"n: {n}")

    def from_numpy(self):
        n = np.ones(5)
        t = torch.from_numpy(n)
        np.add(n, 1, out=n)
        print(f"t: {t}")
        print(f"n: {n}")

    def main(self):
        # self.create_data()
        # self.create_data_from_numpy()
        # self.shape()
        # self.attributes()
        # self.indexing()
        # self.concat()
        # self.matmul()
        # self.mul()
        # self.item()
        # self.inplace()
        # self.to_numpy()
        self.from_numpy()


if __name__ == "__main__":
    Tensors().main()


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
