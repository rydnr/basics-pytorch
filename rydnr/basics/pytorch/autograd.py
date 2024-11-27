"""
rydnr/basics/pytorch/autograd.py

This file defines the Autograd class.

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


class Autograd(BaseObject):
    """
    Notebook for the Autograd chapter in PyTorch tutorial:
    https://pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html

    Class name: Autograd

    Responsibilities:
        - Provide the code of the Autograd chapter.

    Collaborators:
        - None
    """

    def __init__(self):
        """
        Creates a new Autograd instance.
        """
        super().__init__()

    def loss(self):
        x = torch.ones(5)
        y = torch.zeros(3)
        w = torch.randn(5, 3, requires_grad=True)
        b = torch.randn(3, requires_grad=True)
        z = torch.matmul(x, w) + b
        loss = torch.nn.functional.binary_cross_entropy_with_logits(z, y)
        loss.backward()
        print(w.grad)
        print(b.grad)
        return (x, y, w, b, z, loss)

    def disable_gradient_tracking(self, x, w, b):
        z = torch.matmul(x, w) + b
        print(z.requires_grad)

        with torch.no_grad():
            z = torch.matmul(x, w) + b
        print(z.requires_grad)

    def jacobian_product(self):
        inp = torch.eye(4, 5, requires_grad=True)
        print(inp)
        print(inp + 1)
        print((inp + 1).pow(2))
        print((inp + 1).pow(2).t())
        out = (inp + 1).pow(2).t()
        out.backward(torch.ones_like(out), retain_graph=True)
        print(f"First call\n{inp.grad}")
        out.backward(torch.ones_like(out), retain_graph=True)
        print(f"\nSecond call\n{inp.grad}")
        inp.grad.zero_()
        out.backward(torch.ones_like(out), retain_graph=True)
        print(f"\nCall after zeroing gradients\n{inp.grad}")

    def main(self):
        # x, y, w, b, z, loss = self.loss()
        # self.disable_gradient_tracking(x, w, b)
        self.jacobian_product()


if __name__ == "__main__":
    Autograd().main()


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
