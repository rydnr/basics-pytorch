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
import os
from pythoneda.shared import BaseObject
from rydnr.basics.pytorch import QuickstartNeuralNetwork
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
        return datasets.FashionMNIST(
            root="data", train=True, download=True, transform=ToTensor()
        )

    def download_test_data_from_open_datasets(self):
        return datasets.FashionMNIST(
            root="data", train=False, download=True, transform=ToTensor()
        )

    def define_model(self, device):
        return QuickstartNeuralNetwork().to(device)

    def train(self, dataloader, model, loss_fn, optimizer, device):
        size = len(dataloader.dataset)
        model.train()
        for batch, (X, y) in enumerate(dataloader):
            X, y = X.to(device), y.to(device)

            # Compute prediction error
            pred = model(X)
            loss = loss_fn(pred, y)

            # Backpropagation
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            if batch % 100 == 0:
                loss, current = loss.item(), (batch + 1) * len(X)
                print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

    def test(self, dataloader, model, loss_fn, device):
        size = len(dataloader.dataset)
        num_batches = len(dataloader)
        model.eval()
        test_loss, correct = 0, 0
        with torch.no_grad():
            for X, y in dataloader:
                X, y = X.to(device), y.to(device)
                pred = model(X)
                test_loss += loss_fn(pred, y).item()
                correct += (pred.argmax(1) == y).type(torch.float).sum().item()
        test_loss /= num_batches
        correct /= size
        print(
            f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n"
        )

    def save(self, model, file: str):
        torch.save(model.state_dict(), file)

    def prepare_model(self, trainDataloader, testDataloader, device):
        for X, y in test_dataloader:
            print(f"Shape of X [N, C, H, W]: {X.shape}")
            print(f"Shape of y: {y.shape} {y.dtype}")
            break

        model = self.define_model(device)

        loss_fn = nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)

        epochs = 5
        for t in range(epochs):
            print(f"Epoch {t+1}\n-------------------------------")
            self.train(train_dataloader, model, loss_fn, optimizer, device)
            self.test(test_dataloader, model, loss_fn, device)
            print("Done!")

        self.save(model, "quickstart.pth")

    def load_model(self, trainingDataloader, testDataloader, device):
        file = os.path.join(os.getcwd(), "quickstart.pth")
        if os.path.exists(file):
            result = QuickstartNeuralNetwork().to(device)
            result.load_state_dict(torch.load(file))
        else:
            result = self.prepare_model(trainingDataloader, testDataloader, device)

        return result

    def predict(self, model, testData, device):
        classes = [
            "T-shirt/top",
            "Trouser",
            "Pullover",
            "Dress",
            "Coat",
            "Sandal",
            "Shirt",
            "Sneaker",
            "Bag",
            "Ankle boot",
        ]

        model.eval()
        x, y = testData[0][0], testData[0][1]
        with torch.no_grad():
            x = x.to(device)
            pred = model(x)
            predicted, actual = classes[pred[0].argmax(0)], classes[y]
            print(f'Predicted: "{predicted}", Actual: "{actual}"')

    def main(self):
        device = (
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )
        print(f"Using {device} device")

        batch_size = 64

        training_data = self.download_training_data_from_open_datasets()
        test_data = self.download_test_data_from_open_datasets()

        training_dataloader = DataLoader(training_data, batch_size=batch_size)
        test_dataloader = DataLoader(test_data, batch_size=batch_size)

        model = self.load_model(training_dataloader, test_dataloader, device)
        self.predict(model, test_data, device)


if __name__ == "__main__":
    Quickstart().main()

# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
