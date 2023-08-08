"""
This module contains the code to train a neural network on the MNIST dataset. The
model will later be used to extracter the numbers on the Sudoku board.
"""

import torch, torchvision, copy
from torch import nn, optim
import torchvision.transforms as transforms

BATCH_SIZE = 64
transform = torchvision.transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5), (0.5,))])

# Get training and test dset
training_set = torchvision.datasets.MNIST(root='./dataset', train=True, download=False, transform=transform)
test_set = torchvision.datasets.MNIST("./dataset/", train=False, download=False, transform=transform)

# Load train and test data
train_data_loader = torch.utils.data.DataLoader(training_set, batch_size=BATCH_SIZE) 
test_data_loader = torch.utils.data.DataLoader(test_set, batch_size=BATCH_SIZE) 

model = nn.Sequential(nn.Conv2d(1, 6, 5, padding=2), nn.ReLU(), nn.AvgPool2d(2, stride=2),
                       nn.Conv2d(6, 16, 5, padding=0),nn.ReLU(), nn.AvgPool2d(2, stride=2),
                       nn.Flatten(), nn.Linear(400, 120), nn.ReLU(), nn.Linear(120, 84),
                       nn.ReLU(),nn.Linear(84, 10)
                       )

def test_model(model: nn.Sequential, data: torch.utils.data.DataLoader) -> float:
    """Tests the model's accuracy.

    Args:
        model: the cnn model.
        data: the loaded test data.
    
    Returns:
        A floating point number representing the accuracy of the model as a percentage.
    """

    total = 0
    num_correct = 0
    for i, (images, labels) in enumerate(data):
        images = images.cuda()
        x = model(images)
        _, prediction = torch.max(x, 1)
        prediction = prediction.data.cpu()
        total += x.size(0)
        num_correct += torch.sum(prediction == labels)
    return num_correct * 100 /  total

def train_model(num_epochs: int = 5, lr: float = 0.001, device: str = "cpu") -> nn.Sequential:
    """Trains CNN model and returns the model with the highest accuracy.
    
    Args:
        num_epochs: number of epochs that the model will be trained for.
        lr: learning rate of the model.
        device: the device the the model will use to train on.
    
    Returns:
        A trained nn.Sequential model.
    """
    cnn = model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(cnn.parameters(), lr=lr)
    max_accuracy = 0
    for epoch in range(num_epochs):
        for i, (image, labels) in enumerate(train_data_loader):
            image = image.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            prediction = cnn(image)
            loss = criterion(prediction, labels)
            loss.backward()
            optimizer.step()
        accuracy = float(test_model(cnn, test_data_loader))
        if accuracy > max_accuracy:
            best_model = copy.deepcopy(cnn)
            max_accuracy = accuracy
        print(f'Epoch: {epoch + 1} Accuracy : {accuracy}%')
    
    print(f"Returning Best Model with Accuracy: {max_accuracy}")
    return best_model

# if __name__ == "__main__":
    # if torch.cuda.is_available():
    #     device = torch.device("cuda:0")
    # else:
    #     device = torch.device("cpu")
    #     print("No Cuda Available")

    # model.train()
    # trained_model = train_model(device=device)

    # NOTE: Uncommenting this will overwrite saved model
    # torch.save(trained_model.state_dict(), "trained_mnist_cnn.pth") 

