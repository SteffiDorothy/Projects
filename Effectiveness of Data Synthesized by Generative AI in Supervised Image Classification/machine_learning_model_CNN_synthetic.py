import os
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
from collections import Counter
import random


class SyntheticFoodCNN(nn.Module):
    def __init__(self, num_classes):
        super(SyntheticFoodCNN, self).__init__()

        # Feature extraction
        self.features = nn.Sequential(
            # First conv block
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Second conv block
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Third conv block
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Fourth conv block
            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.Dropout2d(0.3),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        # Classifier
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


class SyntheticFoodDataset(Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        try:
            image = Image.open(self.image_paths[idx]).convert('RGB')
            label = self.labels[idx]

            if self.transform:
                image = self.transform(image)

            return image, label
        except Exception as e:
            print(f"Error loading image {self.image_paths[idx]}: {str(e)}")
            # Return a default image in case of error
            return torch.zeros((3, 224, 224)), label


def extract_class_from_filename(filename):
    """Extract class name from generated image filename"""
    # Split by '_generated_image' and take the first part
    class_name = filename.split('_generated_image')[0]
    return class_name


def custom_train_test_split(image_paths, labels, test_size=0.2):
    """Custom split that handles classes with single images"""
    # Create dictionary of class indices for each label
    label_to_indices = {}
    for idx, label in enumerate(labels):
        if label not in label_to_indices:
            label_to_indices[label] = []
        label_to_indices[label].append(idx)

    train_indices = []
    test_indices = []

    # Handle each class separately
    for label, indices in label_to_indices.items():
        if len(indices) == 1:
            # If only one image, put it in training set
            train_indices.extend(indices)
        else:
            # Otherwise, split randomly maintaining ratio
            n_test = max(1, int(len(indices) * test_size))
            test_idx = random.sample(indices, n_test)
            train_idx = list(set(indices) - set(test_idx))

            train_indices.extend(train_idx)
            test_indices.extend(test_idx)

    # Create train and test sets
    train_paths = [image_paths[i] for i in train_indices]
    test_paths = [image_paths[i] for i in test_indices]
    train_labels = [labels[i] for i in train_indices]
    test_labels = [labels[i] for i in test_indices]

    return train_paths, test_paths, train_labels, test_labels


def prepare_data(data_dir):
    """Organize data and create class mappings"""
    image_paths = []
    labels = []
    class_names = set()

    # Collect all valid image files
    valid_extensions = {'.png', '.jpg', '.jpeg'}
    for file in os.listdir(data_dir):
        if file.lower().endswith(tuple(valid_extensions)) and '_generated_image' in file:
            try:
                class_name = extract_class_from_filename(file)
                class_names.add(class_name)
                full_path = os.path.join(data_dir, file)
                # Verify image can be opened
                with Image.open(full_path) as img:
                    img.verify()
                image_paths.append(full_path)
                labels.append(class_name)
            except Exception as e:
                print(f"Skipping corrupted image {file}: {str(e)}")

    # Convert class names to indices
    class_names = sorted(list(class_names))
    class_to_idx = {name: idx for idx, name in enumerate(class_names)}
    labels = [class_to_idx[label] for label in labels]

    # Print class distribution
    label_counts = Counter([class_names[label] for label in labels])
    print("\nClass distribution:")
    for class_name, count in label_counts.items():
        print(f"{class_name}: {count} images")

    return image_paths, labels, class_names


def train_model(model, train_loader, val_loader, criterion, optimizer,
                num_epochs=10, device='cuda', patience=5):
    best_val_acc = 0
    train_losses = []
    val_accuracies = []
    patience_counter = 0

    for epoch in range(num_epochs):
        # Training phase
        model.train()
        running_loss = 0.0
        progress_bar = tqdm(train_loader, desc=f'Epoch {epoch + 1}/{num_epochs}')

        for inputs, labels in progress_bar:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            progress_bar.set_postfix({'loss': loss.item()})

        epoch_loss = running_loss / len(train_loader)
        train_losses.append(epoch_loss)

        # Validation phase
        val_acc = evaluate_model(model, val_loader, device)
        val_accuracies.append(val_acc)

        print(f'Epoch {epoch + 1}: Loss = {epoch_loss:.4f}, Val Accuracy = {val_acc:.2f}%')

        # Save best model and check for early stopping
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_acc': val_acc,
            }, 'best_synthetic_food_classifier.pth')
            patience_counter = 0
        else:
            patience_counter += 1

        if patience_counter >= patience:
            print(f'\nEarly stopping triggered after {epoch + 1} epochs')
            break

    return train_losses, val_accuracies



def evaluate_model(model, loader, device='cuda'):
    if not loader.dataset:
        return 0.0

    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total if total > 0 else 0
    return accuracy


def main():
    # Set random seeds
    torch.manual_seed(42)
    np.random.seed(42)
    random.seed(42)

    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')

    # Data directory
    data_dir = "/Users/ehushubhamshaw/Desktop/Machine_learning/Final_project_ml/DataSynthesizer/Datasets/DiegoP-S/DatasetSynthesis"

    # Prepare data
    image_paths, labels, class_names = prepare_data(data_dir)
    num_classes = len(class_names)
    print(f'\nFound {num_classes} classes')

    # Custom split that handles single-image classes
    train_paths, val_paths, train_labels, val_labels = custom_train_test_split(
        image_paths, labels, test_size=0.2
    )

    print(f'\nTraining set: {len(train_paths)} images')
    print(f'Validation set: {len(val_paths)} images')

    # Define transforms
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.9, 1.1)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    # Create datasets and loaders
    train_dataset = SyntheticFoodDataset(train_paths, train_labels, transform=transform)
    val_dataset = SyntheticFoodDataset(val_paths, val_labels, transform=val_transform)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=4)

    # Initialize model, criterion, and optimizer
    model = SyntheticFoodCNN(num_classes=num_classes).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Train model
    train_losses, val_accuracies = train_model(
        model, train_loader, val_loader, criterion, optimizer,
        num_epochs=25, device=device, patience=5
    )

    # Plot results
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.plot(train_losses)
    plt.title('Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')

    plt.subplot(1, 2, 2)
    plt.plot(val_accuracies)
    plt.title('Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')

    plt.tight_layout()
    plt.savefig('training_results.png')
    plt.show()

    # Save class mapping
    import json
    class_mapping = {idx: name for idx, name in enumerate(class_names)}
    with open('class_mapping.json', 'w') as f:
        json.dump(class_mapping, f, indent=4)


if __name__ == '__main__':
    main()