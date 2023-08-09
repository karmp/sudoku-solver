"""
This module contains the code to train a neural network on the MNIST dataset. The
model will later be used to extracter the numbers on the Sudoku board.
"""

import torch, torchvision, copy
from torch import nn, optim
import torchvision.transforms as transforms
from torch.optim.lr_scheduler import ReduceLROnPlateau
from pathlib import Path

BATCH_SIZE = 64
transform = torchvision.transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])

# Get training and test dset
training_set = torchvision.datasets.MNIST(root='./dataset', train=True, download=False, transform=transform)
test_set = torchvision.datasets.MNIST("./dataset/", train=False, download=False, transform=transform)

# Load train and test data
train_data_loader = torch.utils.data.DataLoader(training_set, batch_size=BATCH_SIZE) 
test_data_loader = torch.utils.data.DataLoader(test_set, batch_size=BATCH_SIZE) 

# Setup CNN model
model = nn.Sequential(
    nn.Conv2d(1, 6, 5, padding=2), 
    nn.ReLU(), 
    nn.BatchNorm2d(6),
    nn.MaxPool2d(2, stride=2),

    nn.Conv2d(6, 16, 5, padding=0),
    nn.ReLU(),
    nn.BatchNorm2d(16),
    nn.MaxPool2d(2, stride=2),

    nn.Flatten(), 
    nn.Linear(400, 120), 
    nn.ReLU(),
    nn.Dropout(0.4),

    nn.Linear(120, 84),
    nn.ReLU(),
    nn.Linear(84, 10),
    
    nn.Softmax(dim=1)
    )

def test_model(model: nn.Sequential, data: torch.utils.data.DataLoader, criterion) -> tuple:
    """Tests the model's accuracy.

    Args:
        model: the cnn model.
        data: the loaded test data.
        criterion: the criterion that the model will use to evaluate loss.
    
    Returns:
        A tuple containing the accuracy of the model as a percentage and validation loss.
    """
    model.eval()
    total = 0
    num_correct = 0
    validation_loss = 0
    num_samples = 0
    for images, labels in data:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        # Calculate model accuracy
        _, prediction = torch.max(outputs, 1)
        prediction = prediction.data.to(device)
        total += outputs.size(0)
        num_correct += torch.sum(prediction == labels)
        
        # Calculate avg_loss
        loss = criterion(outputs, labels)
        validation_loss += loss.item() * images.size(0)
        num_samples += images.size(0)
    model.train()
    return ((num_correct / total) * 100,  validation_loss / num_samples)

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
    optimizer = optim.SGD(cnn.parameters(), lr=lr)
    scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=10, verbose=True)
    max_accuracy = 0
    # Train model and return best model
    for epoch in range(num_epochs):
        for image, labels in train_data_loader:
            image, labels = image.to(device), labels.to(device)
            optimizer.zero_grad()
            prediction = cnn(image)
            loss = criterion(prediction, labels)
            loss.backward()
            optimizer.step()
        
        accuracy, avg_loss = test_model(cnn, test_data_loader, criterion)
        if accuracy > max_accuracy:
            best_model = copy.deepcopy(cnn)
            max_accuracy = accuracy
        scheduler.step(avg_loss)
        print(f'Epoch: {epoch + 1} Accuracy : {accuracy:.4f}%  Loss : {avg_loss:.4f}')
    
    print(f"Returning Best Model with Accuracy: {max_accuracy}")
    return best_model

if __name__ == "__main__":
    if torch.cuda.is_available():
        device = torch.device("cuda:0")
    else:
        device = torch.device("cpu")
        print("No Cuda Available")

    model.train()
    trained_model = train_model(num_epochs=35, lr=0.01, device=device)

    # NOTE: Uncommenting this will overwrite the saved model with the same name
    torch.save(trained_model.state_dict(), Path("img_processing", "trained_mnist_cnn2.pth")) 

