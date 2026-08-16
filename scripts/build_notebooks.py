#!/usr/bin/env python3
"""
build_notebooks.py - Generates the 9 assignment notebooks (Question_1 .. Question_9).

Run with the project venv python, then execute each notebook with:
    python -m nbconvert --to notebook --execute --inplace <notebook>
"""
import os
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from nbformat import write

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BOOT = """import os, sys, pathlib, warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
PROJECT_ROOT = pathlib.Path(os.path.abspath(os.getcwd()))
for p in [PROJECT_ROOT] + list(PROJECT_ROOT.parents):
    if (p / 'images_dataSAT').is_dir():
        PROJECT_ROOT = p
        break
os.chdir(PROJECT_ROOT)
print('Project root:', PROJECT_ROOT)"""


def notebook(title, cells):
    nb = new_notebook()
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.cells = [new_markdown_cell(f"# {title}")] + cells
    return nb


def save(nb, rel_path):
    path = os.path.join(PROJECT_ROOT, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        write(nb, f)
    print("wrote", path)


# ============================================================================
# Question 1 - Module 1: Comparison of Memory-Based and Generator-Based Loading
# ============================================================================
Q1 = notebook("Module 1: Comparison of Memory-Based and Generator-Based Data Loading", [
    new_markdown_cell("""> **Assignment (10 points):** Compare loading all satellite images into memory vs. loading them lazily with a generator.

Data layout used by all labs:

```
images_dataSAT/
├── class_0_non_agri/   (non-agricultural land)
└── class_1_agri/       (agricultural land)
```"""),
    new_code_cell(BOOT),
    new_code_cell("""import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

dir_non_agri = './images_dataSAT/class_0_non_agri/'
dir_agri     = './images_dataSAT/class_1_agri/'

def get_image_paths(directory):
    return sorted([os.path.join(directory, f) for f in os.listdir(directory)
                   if os.path.isfile(os.path.join(directory, f))])"""),
    new_markdown_cell("## Memory-based loading: load **all** images into RAM at once"),
    new_code_cell("""def load_all_images(directory):
    paths = get_image_paths(directory)
    images = np.array([np.array(Image.open(p).resize((64, 64))) for p in paths])
    return paths, images

non_agri_paths, non_agri_images = load_all_images(dir_non_agri)
agri_paths,     agri_images     = load_all_images(dir_agri)

image_data   = np.concatenate([non_agri_images, agri_images])
image_labels = np.array([0] * len(non_agri_images) + [1] * len(agri_images))

print('image_data shape :', image_data.shape)
print('image_data memory: %.1f MB' % (image_data.nbytes / 1e6))"""),
    new_markdown_cell("### Task 1: Determine the shape (dimensions) of a single image stored in the `image_data` variable"),
    new_code_cell("""single_image = image_data[0]
print('Shape of a single image:', single_image.shape)
print('Data type              :', single_image.dtype)"""),
    new_markdown_cell("### Task 2: Display the first four images in `'./images_dataSAT/class_0_non_agri/'`"),
    new_code_cell("""fig, axes = plt.subplots(1, 4, figsize=(12, 3))
for i in range(4):
    axes[i].imshow(non_agri_images[i])
    axes[i].set_title(f'Non-Agri image {i}')
    axes[i].axis('off')
plt.tight_layout()
plt.show()"""),
    new_markdown_cell("### Task 3: Create `agri_images_paths` — full paths of all images in `dir_agri`, **sorted**"),
    new_code_cell("""agri_images_paths = [os.path.join(dir_agri, f) for f in os.listdir(dir_agri)
                    if os.path.isfile(os.path.join(dir_agri, f))]
agri_images_paths.sort()

print('Number of paths:', len(agri_images_paths))
print('First 5 paths  :')
for p in agri_images_paths[:5]:
    print(' ', p)"""),
    new_markdown_cell("### Task 4: Number of agricultural land images in `'./images_dataSAT/class_1_agri/'`"),
    new_code_cell("""num_agri_images = len(agri_images_paths)
print(f'Number of agricultural land images: {num_agri_images}')"""),
    new_markdown_cell("### Task 5: Display the first four agricultural land images"),
    new_code_cell("""fig, axes = plt.subplots(1, 4, figsize=(12, 3))
for i in range(4):
    img = np.array(Image.open(agri_images_paths[i]).resize((64, 64)))
    axes[i].imshow(img)
    axes[i].set_title(f'Agri image {i}')
    axes[i].axis('off')
plt.tight_layout()
plt.show()"""),
    new_markdown_cell("## Generator-based loading: lazy, one batch at a time"),
    new_code_cell("""def custom_data_generator(list_of_paths, labels, batch_size=8, image_size=(64, 64), shuffle=True):
    indices = list(range(len(list_of_paths)))
    while True:
        if shuffle:
            np.random.shuffle(indices)
        for start in range(0, len(indices), batch_size):
            batch_idx = indices[start:start + batch_size]
            batch_images = np.array([np.array(Image.open(list_of_paths[i]).resize(image_size)) for i in batch_idx])
            batch_labels = np.array([labels[i] for i in batch_idx])
            yield batch_images, batch_labels

all_paths = agri_paths + non_agri_paths
all_path_labels = [1] * len(agri_paths) + [0] * len(non_agri_paths)

gen = custom_data_generator(all_paths, all_path_labels, batch_size=8)
X_batch, y_batch = next(gen)
print('One generator batch shape:', X_batch.shape)
print('Batch labels             :', y_batch)"""),
    new_code_cell("""import sys
print('Full in-memory array : %.1f MB' % (image_data.nbytes / 1e6))
print('Generator object     : %d bytes (lazy, loads only one batch at a time)' % sys.getsizeof(gen))"""),
    new_markdown_cell("""> **Conclusion:** memory-based loading loads the whole dataset into RAM at once (here ~95 MB, and it grows linearly with dataset size), while generator-based loading reads and preprocesses one small batch at a time, keeping memory usage flat — the memory-efficient strategy for large geospatial datasets."""),
])
save(Q1, "Question_1/Lab1_Comparison_Memory_Generator.ipynb")

# ============================================================================
# Question 2 - Module 1: Data Loading and Augmentation Using Keras
# ============================================================================
Q2 = notebook("Module 1: Data Loading and Augmentation Using Keras", [
    new_markdown_cell("> **Assignment (8 points):** Build a Keras data pipeline with a custom generator and augmentation."),
    new_code_cell(BOOT),
    new_code_cell("""import os, random
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import tensorflow as tf

base_directory = './images_dataSAT'
random.seed(42)"""),
    new_markdown_cell("### Task 1: Create `all_image_paths` — paths of all files in both folders (`class_0_non_agri` and `class_1_agri`) inside the base directory"),
    new_code_cell("""all_image_paths = []
for folder_name in ['class_0_non_agri', 'class_1_agri']:
    folder_path = os.path.join(base_directory, folder_name)
    all_image_paths.extend([os.path.join(folder_path, f) for f in os.listdir(folder_path)
                            if os.path.isfile(os.path.join(folder_path, f))])

print('Total image paths:', len(all_image_paths))
print(all_image_paths[:3])"""),
    new_markdown_cell("### Task 2: Bind paths & labels with `zip` into `temp`, then randomly select and print 5 image paths with their labels"),
    new_code_cell("""labels = [0 if 'class_0' in p else 1 for p in all_image_paths]

temp = list(zip(all_image_paths, labels))

selected = random.sample(temp, 5)
for path, label in selected:
    print(path, '->', label)"""),
    new_markdown_cell("## Custom data generator (with optional on-the-fly augmentation)"),
    new_code_cell("""def custom_data_generator(list_of_files, labels, batch_size=8, image_size=(64, 64),
                          shuffle=True, augment=False):
    indices = list(range(len(list_of_files)))
    while True:
        if shuffle:
            random.shuffle(indices)
        for start in range(0, len(indices), batch_size):
            batch_idx = indices[start:start + batch_size]
            batch_images = []
            for i in batch_idx:
                img = np.array(Image.open(list_of_files[i]).convert('RGB').resize(image_size))
                if augment:
                    img_t = tf.image.random_flip_left_right(tf.convert_to_tensor(img))
                    img_t = tf.image.random_flip_up_down(img_t)
                    img_t = tf.image.random_brightness(img_t, max_delta=0.2)
                    img = img_t.numpy()
                batch_images.append(img)
            X_batch = np.stack(batch_images).astype('float32') / 255.0
            y_batch = np.array([labels[i] for i in batch_idx])
            yield X_batch, y_batch"""),
    new_markdown_cell("### Task 3: Generate a batch of data (batch size = 8) by invoking `custom_data_generator`"),
    new_code_cell("""train_gen = custom_data_generator(all_image_paths, labels, batch_size=8, augment=False)
X_batch, y_batch = next(train_gen)
print('Batch shape:', X_batch.shape)
print('Labels     :', y_batch)"""),
    new_markdown_cell("## Augmentation demo — original vs. augmented versions of the same image"),
    new_code_cell("""fig, axes = plt.subplots(1, 4, figsize=(12, 3))
img = np.array(Image.open(all_image_paths[0]).convert('RGB').resize((64, 64)))
axes[0].imshow(img)
axes[0].set_title('Original')
axes[0].axis('off')
for k in range(3):
    img_t = tf.image.random_flip_left_right(tf.convert_to_tensor(img))
    img_t = tf.image.random_flip_up_down(img_t)
    img_t = tf.image.random_brightness(img_t, max_delta=0.2)
    axes[k + 1].imshow(img_t.numpy())
    axes[k + 1].set_title(f'Augmented {k + 1}')
    axes[k + 1].axis('off')
plt.tight_layout()
plt.show()"""),
    new_markdown_cell("### Task 4: Create validation data using a batch size of 8"),
    new_code_cell("""split = int(len(all_image_paths) * 0.8)
train_paths = all_image_paths[:split]
val_paths   = all_image_paths[split:]
train_labels = labels[:split]
val_labels   = labels[split:]

val_gen = custom_data_generator(val_paths, val_labels, batch_size=8)
X_val, y_val = next(val_gen)
print('Validation batch shape:', X_val.shape)
print('Validation labels     :', y_val)"""),
    new_markdown_cell("## Keras native pipeline (extra): `image_dataset_from_directory`"),
    new_code_cell("""train_dataset = tf.keras.utils.image_dataset_from_directory(
    base_directory, labels='inferred', label_mode='binary', color_mode='rgb',
    batch_size=8, image_size=(64, 64), validation_split=0.2, subset='training',
    seed=42, shuffle=True)

val_dataset = tf.keras.utils.image_dataset_from_directory(
    base_directory, labels='inferred', label_mode='binary', color_mode='rgb',
    batch_size=8, image_size=(64, 64), validation_split=0.2, subset='validation',
    seed=42, shuffle=True)

for x, y in train_dataset.take(1):
    print('tf.data batch:', x.shape, y.shape)"""),
])
save(Q2, "Question_2/Lab2_Keras_Data_Loading_Augmentation.ipynb")

# ============================================================================
# Question 3 - Module 1: Data Loading and Augmentation Using PyTorch
# ============================================================================
Q3 = notebook("Module 1: Data Loading and Augmentation Using PyTorch", [
    new_markdown_cell("> **Assignment (10 points):** PyTorch data pipeline with `torchvision.datasets.ImageFolder` and a custom transform pipeline."),
    new_code_cell(BOOT),
    new_code_cell("""import numpy as np
import matplotlib.pyplot as plt
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

data_dir = './images_dataSAT'
print('PyTorch version:', torch.__version__)"""),
    new_markdown_cell("### Task 1: Create the transformation pipeline `custom_transform`"),
    new_code_cell("""custom_transform = transforms.Compose([
    transforms.Resize((64, 64)),            # 1. image size = 64 x 64 pixels
    transforms.RandomHorizontalFlip(p=0.5), # 2. random horizontal flip, probability 0.5
    transforms.RandomVerticalFlip(p=0.2),   # 3. random vertical flip, probability 0.2
    transforms.RandomRotation(45),          # 4. random rotation of 45 degrees
    transforms.ToTensor(),                  # PIL -> Tensor (needed by the DataLoader)
])
print(custom_transform)"""),
    new_markdown_cell("### Task 2: Load `imagefolder_dataset` using `datasets.ImageFolder` with `custom_transform`"),
    new_code_cell("""imagefolder_dataset = datasets.ImageFolder(root=data_dir, transform=custom_transform)
print('Dataset size  :', len(imagefolder_dataset))
print('Class names   :', imagefolder_dataset.classes)"""),
    new_markdown_cell("### Task 3: Print the class name and the class index from `imagefolder_dataset`"),
    new_code_cell("""for class_name, class_index in imagefolder_dataset.class_to_idx.items():
    print(f'{class_name}: {class_index}')"""),
    new_markdown_cell("### Task 4: Retrieve a batch of images and labels from `imagefolder_loader` and display their shapes"),
    new_code_cell("""imagefolder_loader = DataLoader(imagefolder_dataset, batch_size=8, shuffle=True)
images, labels = next(iter(imagefolder_loader))
print('images shape:', images.shape)
print('labels shape:', labels.shape, '->', labels)"""),
    new_markdown_cell("### Task 5: Display the images in the batch"),
    new_code_cell("""fig, axes = plt.subplots(2, 4, figsize=(12, 6))
for i in range(8):
    ax = axes[i // 4][i % 4]
    img = images[i].permute(1, 2, 0).numpy()
    img = (img - img.min()) / (img.max() - img.min() + 1e-8)
    ax.imshow(img)
    ax.set_title(imagefolder_dataset.classes[labels[i].item()])
    ax.axis('off')
plt.tight_layout()
plt.show()"""),
])
save(Q3, "Question_3/Lab3_PyTorch_Data_Loading_Augmentation.ipynb")

# ============================================================================
# Question 4 - Module 2: Train and Evaluate a Keras-Based Classifier
# ============================================================================
Q4 = notebook("Module 2: Train and Evaluate a Keras-Based Classifier", [
    new_markdown_cell("> **Assignment (12 points):** Build, compile and train a CNN for agricultural vs non-agricultural land classification with Keras."),
    new_code_cell(BOOT),
    new_code_cell("""import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

tf.random.set_seed(42)
dataset_path = './images_dataSAT'
print('TensorFlow version:', tf.__version__)"""),
    new_markdown_cell("### Task 1: Recursively walk `dataset_path` with `os.walk` to create `fnames` (all image files)"),
    new_code_cell("""fnames = []
for root, dirs, files in os.walk(dataset_path):
    for f in files:
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            fnames.append(os.path.join(root, f))

print('Total image files:', len(fnames))
print(fnames[:3])"""),
    new_markdown_cell("### Task 2: Create `validation_generator` from `dataset_path`"),
    new_code_cell("""from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2,
)

train_generator = datagen.flow_from_directory(
    dataset_path, target_size=(64, 64), batch_size=32, class_mode='binary',
    subset='training', shuffle=True, seed=42)

validation_generator = datagen.flow_from_directory(
    dataset_path, target_size=(64, 64), batch_size=32, class_mode='binary',
    subset='validation', shuffle=False, seed=42)"""),
    new_markdown_cell("### Task 3: Count the total number of layers in this CNN model"),
    new_code_cell("""def build_cnn(input_shape=(64, 64, 3)):
    return tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=input_shape),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid'),
    ])

model = build_cnn()
print('Total number of layers in the CNN model:', len(model.layers))"""),
    new_markdown_cell("### Task 4: Create and compile `test_model` — four Conv2D layers and five Dense layers"),
    new_code_cell("""test_model = build_cnn()

conv_count   = sum(isinstance(l, tf.keras.layers.Conv2D) for l in test_model.layers)
dense_count  = sum(isinstance(l, tf.keras.layers.Dense) for l in test_model.layers)
print('Conv2D layers:', conv_count, '| Dense layers:', dense_count,
      '| Total layers:', len(test_model.layers))

test_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
test_model.summary()"""),
    new_markdown_cell("### Task 5: Create the checkpoint callback for the model with maximum accuracy"),
    new_code_cell("""os.makedirs('models', exist_ok=True)

checkpoint = tf.keras.callbacks.ModelCheckpoint(
    filepath='models/best_cnn.keras',
    monitor='val_accuracy',     # keep the model with the highest accuracy
    mode='max',
    save_best_only=True,
    verbose=1,
)

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss', patience=3, restore_best_weights=True)"""),
    new_markdown_cell("## Train the model"),
    new_code_cell("""history = test_model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=5,
    steps_per_epoch=len(train_generator),
    callbacks=[checkpoint, early_stopping],
    verbose=1,
)"""),
    new_markdown_cell("### Task 6: Plot the graph for training loss and validation loss"),
    new_code_cell("""plt.figure(figsize=(8, 5))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.savefig('models/keras_cnn_loss.png')
plt.show()"""),
    new_markdown_cell("## Save the trained model (reused by Module 3) and evaluate quickly"),
    new_code_cell("""test_model.save('models/cnn_model.keras')
print('Model saved -> models/cnn_model.keras')

validation_generator.reset()
y_true = validation_generator.classes
y_pred = (test_model.predict(validation_generator, verbose=0).flatten() > 0.5).astype(int)

from sklearn.metrics import accuracy_score, f1_score
print('Validation accuracy:', round(accuracy_score(y_true, y_pred), 4))
print('Validation F1     :', round(f1_score(y_true, y_pred), 4))"""),
])
save(Q4, "Question_4/Lab4_Keras_Classifier.ipynb")

# ============================================================================
# Question 5 - Module 2: Implement and Test a PyTorch-Based Classifier
# ============================================================================
Q5 = notebook("Module 2: Implement and Test a PyTorch-Based Classifier", [
    new_markdown_cell("> **Assignment (20 points):** Full PyTorch CNN training pipeline with questions + plots + predictions."),
    new_code_cell(BOOT),
    new_code_cell("""import os, random, time
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split
from tqdm import tqdm
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

random.seed(42)
np.random.seed(42)
torch.manual_seed(42)

data_dir = './images_dataSAT'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Device:', device)"""),
    new_markdown_cell("""### Task 1 (Question): Why is random initialization useful for the model?

**Answer:** Random initialization breaks the *symmetry* between neurons — if all weights started with the same value, every neuron in a layer would compute identical gradients and be updated identically, so the network could never learn diverse features. Random small initial values also help gradients flow properly through the network (avoiding vanishing/exploding gradients) and allow different neurons to specialize on different patterns, which is essential for training deep models."""),
    new_markdown_cell("### Task 2: Create the training transformation pipeline `train_transform` using `transforms.Compose`"),
    new_code_cell("""train_transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomVerticalFlip(p=0.2),
    transforms.RandomRotation(45),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
print(train_transform)"""),
    new_markdown_cell("### Task 3: Create the validation transformation pipeline `val_transform`"),
    new_code_cell("""val_transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
print(val_transform)"""),
    new_markdown_cell("## Datasets (70% train / 30% validation)"),
    new_code_cell("""train_dataset = datasets.ImageFolder(data_dir, transform=train_transform)
val_dataset   = datasets.ImageFolder(data_dir, transform=val_transform)

train_size = int(0.7 * len(train_dataset))
val_size   = len(train_dataset) - train_size

train_dataset, _ = random_split(train_dataset, [train_size, val_size])
val_dataset,   _ = random_split(val_dataset, [val_size, train_size])

print('Train samples:', len(train_dataset), '| Val samples:', len(val_dataset))"""),
    new_markdown_cell("### Task 4: Create `val_loader` for the validation dataset"),
    new_code_cell("""train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader   = DataLoader(val_dataset, batch_size=32, shuffle=False)
print('Train batches:', len(train_loader), '| Val batches:', len(val_loader))"""),
    new_markdown_cell("## CNN model definition"),
    new_code_cell("""class CNNClassifier(nn.Module):
    def __init__(self, num_classes=1):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(128, 256, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256 * 4 * 4, 512), nn.ReLU(),
            nn.Linear(512, 256), nn.ReLU(),
            nn.Linear(256, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, num_classes),
        )

    def forward(self, x):
        return self.classifier(self.features(x))

model = CNNClassifier()
print(model)"""),
    new_markdown_cell("""### Task 5 (Question): What is `tqdm` used for?

**Answer:** `tqdm` is a Python library that adds a progress bar to any loop. During training it shows the current iteration, elapsed time and the estimated remaining time (ETA), which makes monitoring long training epochs much easier."""),
    new_markdown_cell("""### Task 6 (Question): Why are `train_loss`, `train_correct` and `train_total` set to 0 in every epoch?

**Answer:** These variables accumulate statistics for the *current* epoch only. If they were not reset, the values from previous epochs would carry over and the reported loss/accuracy would be cumulative and meaningless. Resetting them at the start of each epoch gives fresh per-epoch metrics."""),
    new_markdown_cell("""### Task 7 (Question): Why do you need to use `torch.no_grad()` in the validation loop?

**Answer:** During validation we only need forward predictions — no gradients. `torch.no_grad()` disables autograd, so no computation graph is built or stored for backpropagation, which saves a lot of memory and speeds up evaluation."""),
    new_markdown_cell("""### Task 8 (Question): What are two different metrics on which the model can be evaluated for best performance during training?

**Answer:** The two most common metrics are **validation accuracy** and **validation loss**. Alternative pairs such as **precision** and **recall** (or the **F1-score**) can also be used, especially for imbalanced datasets."""),
    new_markdown_cell("## Training loop (implements the reset pattern of Tasks 5–8)"),
    new_code_cell("""criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

EPOCHS = 5
history = {'train_loss': [], 'val_loss': [], 'train_acc': [], 'val_acc': []}

model = model.to(device)

for epoch in range(EPOCHS):
    model.train()
    train_loss, train_correct, train_total = 0.0, 0, 0
    for images, labels in tqdm(train_loader, desc=f'Epoch {epoch + 1}/{EPOCHS}'):
        images, labels = images.to(device), labels.to(device).float().unsqueeze(1)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        train_loss += loss.item() * images.size(0)
        preds = (torch.sigmoid(outputs) > 0.5).float()
        train_correct += (preds == labels).sum().item()
        train_total += labels.numel()

    model.eval()
    val_loss, val_correct, val_total = 0.0, 0, 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device).float().unsqueeze(1)
            outputs = model(images)
            loss = criterion(outputs, labels)
            val_loss += loss.item() * images.size(0)
            preds = (torch.sigmoid(outputs) > 0.5).float()
            val_correct += (preds == labels).sum().item()
            val_total += labels.numel()

    history['train_loss'].append(train_loss / train_total)
    history['val_loss'].append(val_loss / val_total)
    history['train_acc'].append(train_correct / train_total)
    history['val_acc'].append(val_correct / val_total)
    print(f'Epoch {epoch + 1}: train_loss={history["train_loss"][-1]:.4f} '
          f'val_loss={history["val_loss"][-1]:.4f} '
          f'train_acc={history["train_acc"][-1]:.4f} '
          f'val_acc={history["val_acc"][-1]:.4f}')"""),
    new_markdown_cell("### Task 9: Plot the Model Loss from the training history of the model"),
    new_code_cell("""plt.figure(figsize=(8, 5))
plt.plot(history['train_loss'], label='Training Loss')
plt.plot(history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.savefig('models/pytorch_cnn_loss.png')
plt.show()"""),
    new_markdown_cell("### Task 10: Get `all_preds` (predictions) and `all_labels` (ground truth) from `val_loader`"),
    new_code_cell("""all_preds = []
all_labels = []
model.eval()
with torch.no_grad():
    for images, labels in val_loader:
        images = images.to(device)
        outputs = torch.sigmoid(model(images))
        preds = (outputs > 0.5).long().squeeze(1).cpu()
        all_preds.extend(preds.tolist())
        all_labels.extend(labels.tolist())

print('Number of predictions:', len(all_preds))
print('First 10 predictions :', all_preds[:10])
print('First 10 labels      :', all_labels[:10])"""),
    new_markdown_cell("## Evaluation metrics"),
    new_code_cell("""print('Accuracy :', round(accuracy_score(all_labels, all_preds), 4))
print('Precision:', round(precision_score(all_labels, all_preds), 4))
print('Recall   :', round(recall_score(all_labels, all_preds), 4))
print('F1 score :', round(f1_score(all_labels, all_preds), 4))
print('Confusion matrix:')
print(confusion_matrix(all_labels, all_preds))

os.makedirs('models', exist_ok=True)
torch.save(model.state_dict(), 'models/pytorch_cnn.pth')
print('Model saved -> models/pytorch_cnn.pth')"""),
])
save(Q5, "Question_5/Lab5_PyTorch_Classifier.ipynb")

# ============================================================================
# Question 6 - Module 2: Comparative Analysis of Keras and PyTorch Models
# ============================================================================
Q6 = notebook("Module 2: Comparative Analysis of Keras and PyTorch Models", [
    new_markdown_cell("> **Assignment (10 points):** Compare the trained Keras and PyTorch CNN classifiers with the same evaluation helper."),
    new_code_cell(BOOT),
    new_code_cell("""import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score, roc_curve

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'"""),
    new_markdown_cell("## Shared evaluation helper: `print_metrics`"),
    new_code_cell("""def print_metrics(y_true, y_pred, model_name):
    acc  = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    rec  = recall_score(y_true, y_pred)
    f1   = f1_score(y_true, y_pred)
    cm   = confusion_matrix(y_true, y_pred)
    print(f'\\n========== {model_name} ==========')
    print(f'Accuracy : {acc:.4f}')
    print(f'Precision: {prec:.4f}')
    print(f'Recall   : {rec:.4f}')
    print(f'F1 score : {f1:.4f}')
    print(f'Confusion matrix:\\n{cm}')

    auc = roc_auc_score(y_true, y_pred)
    fpr, tpr, _ = roc_curve(y_true, y_pred)
    plt.figure(figsize=(5, 4))
    plt.plot(fpr, tpr, label=f'{model_name} (AUC={auc:.3f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend()
    plt.grid(True)
    os.makedirs('models', exist_ok=True)
    plt.savefig(f'models/roc_{model_name.replace(" ", "_")}.png')
    plt.show()

    return {'accuracy': acc, 'precision': prec, 'recall': rec, 'f1': f1,
            'confusion_matrix': cm, 'auc': auc}"""),
    new_markdown_cell("""### Task 1 (Question): What does the code `preds > 0.5` in `preds = (preds > 0.5).astype(int).flatten()` do?

**Answer:** The model's output is a sigmoid probability in the range [0, 1]. `preds > 0.5` compares every probability with the 0.5 threshold and returns a boolean array (True → predicted positive class, False → negative class). `.astype(int)` converts the booleans to integer labels 1/0 and `.flatten()` turns the array into a single one-dimensional array. The whole line therefore converts continuous probability scores into hard binary predictions."""),
    new_markdown_cell("## Keras model: reload, predict, evaluate"),
    new_code_cell("""from tensorflow.keras.preprocessing.image import ImageDataGenerator

keras_model = tf.keras.models.load_model('models/cnn_model.keras')

datagen = ImageDataGenerator(rescale=1. / 255)
test_generator = datagen.flow_from_directory(
    './images_dataSAT', target_size=(64, 64), batch_size=32,
    class_mode='binary', shuffle=False, seed=42)

y_true_keras = test_generator.classes
y_prob_keras = keras_model.predict(test_generator, verbose=0).flatten()
y_pred_keras = (y_prob_keras > 0.5).astype(int).flatten()"""),
    new_markdown_cell("### Task 2: Print the performance metrics for the Keras model using `print_metrics`"),
    new_code_cell("""keras_metrics = print_metrics(y_true_keras, y_pred_keras, 'Keras CNN Model')"""),
    new_markdown_cell("""### Task 3 (Question): What is the significance of the F1 score?

**Answer:** The F1 score is the **harmonic mean of precision and recall** (F1 = 2·P·R / (P + R)). It provides a single balanced measure of model performance and is especially useful for **imbalanced datasets**: a high F1 means the model is good both at not missing positives (high recall) and at not producing false positives (high precision)."""),
    new_markdown_cell("## PyTorch model: reload, predict, evaluate"),
    new_code_cell("""class CNNClassifier(nn.Module):
    def __init__(self, num_classes=1):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(128, 256, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256 * 4 * 4, 512), nn.ReLU(),
            nn.Linear(512, 256), nn.ReLU(),
            nn.Linear(256, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, num_classes),
        )

    def forward(self, x):
        return self.classifier(self.features(x))

pt_model = CNNClassifier()
pt_model.load_state_dict(torch.load('models/pytorch_cnn.pth', map_location='cpu', weights_only=True))
pt_model.eval()

val_transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
val_dataset = datasets.ImageFolder('./images_dataSAT', transform=val_transform)
val_dataset, _ = random_split(val_dataset, [1800, 4200])
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

y_true_torch = []
y_prob_torch = []
with torch.no_grad():
    for images, labels in val_loader:
        out = torch.sigmoid(pt_model(images))
        y_prob_torch.extend(out.squeeze(1).tolist())
        y_true_torch.extend(labels.tolist())

y_true_torch = np.array(y_true_torch)
y_prob_torch = np.array(y_prob_torch)
y_pred_torch = (y_prob_torch > 0.5).astype(int).flatten()"""),
    new_markdown_cell("### Task 4: Print the performance metrics for the PyTorch model using `print_metrics`"),
    new_code_cell("""torch_metrics = print_metrics(y_true_torch, y_pred_torch, 'PyTorch CNN Model')"""),
    new_markdown_cell("### Task 5 (Question): What is the total number of false negatives in the confusion matrix for the PyTorch model evaluated above?"),
    new_code_cell("""cm = torch_metrics['confusion_matrix']
fn = int(cm[1][0])          # class 1 (agricultural) predicted as class 0 (non-agricultural)
print('Confusion matrix:')
print(cm)
print()
print(f'Total number of false negatives (FN) for the PyTorch model: {fn}')"""),
    new_markdown_cell("""**Answer:** A false negative means an agricultural image (class 1) was wrongly predicted as non-agricultural (class 0). Looking at the confusion matrix of the PyTorch model, the bottom-left cell (row = class 1, column = class 0) gives the total FN count, printed in the cell above."""),
    new_markdown_cell("## Side-by-side summary"),
    new_code_cell("""print(f'{"Metric":<12}{"Keras CNN":<14}{"PyTorch CNN":<14}')
for key in ['accuracy', 'precision', 'recall', 'f1', 'auc']:
    print(f'{key:<12}{keras_metrics[key]:<14.4f}{torch_metrics[key]:<14.4f}')"""),
])
save(Q6, "Question_6/Lab6_Comparative_Analysis.ipynb")

# ============================================================================
# Question 7 - Module 3: Vision Transformers in Keras
# ============================================================================
Q7 = notebook("Module 3: Vision Transformers in Keras", [
    new_markdown_cell("> **Assignment (10 points):** Extract CNN feature maps, feed them into a Vision Transformer, build and train a CNN-ViT hybrid model."),
    new_code_cell(BOOT),
    new_code_cell("""import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

tf.random.set_seed(42)"""),
    new_markdown_cell("### Task 1: Load the pre-trained CNN model in `cnn_model` using `load_model()` and print the summary"),
    new_code_cell("""cnn_model = tf.keras.models.load_model('models/cnn_model.keras')
cnn_model.summary()"""),
    new_markdown_cell("### Task 2: Based on `model.summary()`, get the name of the layer for feature extraction in `feature_layer_name`"),
    new_code_cell("""feature_layer_name = [l.name for l in cnn_model.layers
                      if isinstance(l, tf.keras.layers.MaxPooling2D)][-1]
print('Feature extraction layer:', feature_layer_name)

# Rebuild the CNN as a feature extractor that ends at feature_layer_name,
# reusing the exact same (pretrained) layer instances.
inputs = tf.keras.Input(shape=(64, 64, 3))
x = inputs
for layer in cnn_model.layers:
    x = layer(x)
    if layer.name == feature_layer_name:
        break
feature_extractor = tf.keras.Model(inputs=inputs, outputs=x)
feature_extractor.trainable = False
feature_extractor.summary()"""),
    new_markdown_cell("## CNN-ViT hybrid architecture (Task 3)"),
    new_code_cell("""def mlp_block(x, hidden_units, dropout_rate):
    for units in hidden_units:
        x = tf.keras.layers.Dense(units, activation='gelu')(x)
        x = tf.keras.layers.Dropout(dropout_rate)(x)
    return x


def transformer_encoder_block(x, embed_dim, num_heads, ff_dim, dropout_rate=0.1):
    residual = x
    x = tf.keras.layers.LayerNormalization(epsilon=1e-6)(x)
    x = tf.keras.layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim, dropout=dropout_rate)(x, x)
    x = tf.keras.layers.Dropout(dropout_rate)(x)
    x = tf.keras.layers.Add()([residual, x])

    residual = x
    x = tf.keras.layers.LayerNormalization(epsilon=1e-6)(x)
    x = mlp_block(x, [ff_dim, embed_dim], dropout_rate)
    x = tf.keras.layers.Add()([residual, x])
    return x


def build_cnn_vit_hybrid(feature_extractor, embed_dim=128, num_heads=4, ff_dim=256,
                         num_transformer_layers=4, dropout_rate=0.1, num_classes=1):
    inputs = tf.keras.Input(shape=(64, 64, 3))
    feature_maps = feature_extractor(inputs)          # (None, 4, 4, 256)

    h, w, c = feature_maps.shape[1], feature_maps.shape[2], feature_maps.shape[3]
    num_patches = h * w                                # 16 tokens
    patches = tf.keras.layers.Reshape((num_patches, c))(feature_maps)

    x = tf.keras.layers.Dense(embed_dim)(patches)      # patch embedding
    positions = tf.range(start=0, limit=num_patches, delta=1)
    pos_embedding = tf.keras.layers.Embedding(input_dim=num_patches, output_dim=embed_dim)(positions)
    x = x + pos_embedding

    for _ in range(num_transformer_layers):
        x = transformer_encoder_block(x, embed_dim, num_heads, ff_dim, dropout_rate)

    x = tf.keras.layers.LayerNormalization(epsilon=1e-6)(x)
    x = tf.keras.layers.GlobalAveragePooling1D()(x)
    x = tf.keras.layers.Dropout(dropout_rate)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation='sigmoid')(x)

    return tf.keras.Model(inputs=inputs, outputs=outputs, name='cnn_vit_hybrid')


hybrid_model = build_cnn_vit_hybrid(feature_extractor)
hybrid_model.summary()"""),
    new_markdown_cell("### Task 4: Compile `hybrid_model`"),
    new_code_cell("""hybrid_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss='binary_crossentropy',
    metrics=['accuracy'],
)"""),
    new_markdown_cell("### Task 5: Define the training configuration of `hybrid_model`"),
    new_code_cell("""from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    rescale=1. / 255, rotation_range=20, width_shift_range=0.2,
    height_shift_range=0.2, zoom_range=0.2, horizontal_flip=True,
    validation_split=0.2,
)
train_generator = datagen.flow_from_directory(
    './images_dataSAT', target_size=(64, 64), batch_size=32, class_mode='binary',
    subset='training', shuffle=True, seed=42)
validation_generator = datagen.flow_from_directory(
    './images_dataSAT', target_size=(64, 64), batch_size=32, class_mode='binary',
    subset='validation', shuffle=False, seed=42)

EPOCHS = 5
BATCH_SIZE = 32

os.makedirs('models', exist_ok=True)
checkpoint_vit = tf.keras.callbacks.ModelCheckpoint(
    'models/vit_hybrid.keras', monitor='val_accuracy', mode='max', save_best_only=True)
early_stop_vit = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss', patience=3, restore_best_weights=True)

history_vit = hybrid_model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=EPOCHS,
    callbacks=[checkpoint_vit, early_stop_vit],
    verbose=1,
)"""),
    new_markdown_cell("## Plot losses and save the hybrid model"),
    new_code_cell("""plt.figure(figsize=(8, 5))
plt.plot(history_vit.history['loss'], label='Training Loss')
plt.plot(history_vit.history['val_loss'], label='Validation Loss')
plt.title('Hybrid CNN-ViT Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.savefig('models/vit_hybrid_loss.png')
plt.show()

hybrid_model.save('models/vit_hybrid.keras')
print('Hybrid model saved -> models/vit_hybrid.keras')"""),
])
save(Q7, "Question_7/Lab7_Vision_Transformers_Keras.ipynb")

# ============================================================================
# Question 8 - Module 3: Vision Transformers in PyTorch
# ============================================================================
Q8 = notebook("Module 3: Vision Transformers in PyTorch", [
    new_markdown_cell("> **Assignment (12 points):** CNN-ViT hybrid in PyTorch — train a base hybrid `model` and a larger `model_test` (embed_dim=768, heads=12, depth=12), then compare validation loss and training time."),
    new_code_cell(BOOT),
    new_code_cell("""import os, random, time
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split
from tqdm import tqdm

random.seed(42)
np.random.seed(42)
torch.manual_seed(42)

data_dir = './images_dataSAT'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Device:', device)"""),
    new_markdown_cell("### Task 1: Create `train_transform` for the training dataset"),
    new_code_cell("""train_transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomVerticalFlip(p=0.2),
    transforms.RandomRotation(45),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
print(train_transform)"""),
    new_markdown_cell("### Task 2: Create `val_transform` for the validation dataset"),
    new_code_cell("""val_transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
print(val_transform)"""),
    new_markdown_cell("### Task 3: Create `train_loader` and `val_loader` using `train_dataset` and `val_dataset`"),
    new_code_cell("""train_dataset = datasets.ImageFolder(data_dir, transform=train_transform)
val_dataset   = datasets.ImageFolder(data_dir, transform=val_transform)

train_dataset, _ = random_split(train_dataset, [600, len(train_dataset) - 600])
val_dataset,   _ = random_split(val_dataset, [400, len(val_dataset) - 400])

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader   = DataLoader(val_dataset, batch_size=32, shuffle=False)
print('Train batches:', len(train_loader), '| Val batches:', len(val_loader))"""),
    new_markdown_cell("## CNN-ViT hybrid model definition"),
    new_code_cell("""class CNNViTHybrid(nn.Module):
    def __init__(self, embed_dim=128, num_heads=4, transformer_depth=4, num_classes=1):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(128, 256, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.num_patches = 4 * 4                       # CNN feature map -> tokens
        self.patch_embed = nn.Linear(256, embed_dim)   # project each token to embed_dim
        self.pos_embed = nn.Parameter(torch.randn(1, self.num_patches, embed_dim) * 0.02)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim, nhead=num_heads, dim_feedforward=4 * embed_dim,
            batch_first=True, dropout=0.1, norm_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=transformer_depth)
        self.head = nn.Sequential(nn.LayerNorm(embed_dim), nn.Linear(embed_dim, num_classes))

    def forward(self, x):
        x = self.cnn(x)                                # (B, 256, 4, 4)
        B, C, H, W = x.shape
        x = x.permute(0, 2, 3, 1).reshape(B, H * W, C) # (B, 16, 256) tokens
        x = self.patch_embed(x) + self.pos_embed       # (B, 16, embed_dim)
        x = self.transformer(x)                        # transformer over 16 tokens
        x = x.mean(dim=1)                              # global pooling
        return self.head(x)"""),
    new_markdown_cell("## Generic training helper"),
    new_code_cell("""def train_model(model, train_loader, val_loader, epochs=5, lr=1e-4, device='cpu'):
    model = model.to(device)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    hist = {'train_loss': [], 'val_loss': [], 'train_acc': [], 'val_acc': []}
    start = time.time()

    for epoch in range(epochs):
        model.train()
        train_loss, train_correct, train_total = 0.0, 0, 0
        for images, labels in tqdm(train_loader, desc=f'Epoch {epoch + 1}/{epochs}', leave=False):
            images, labels = images.to(device), labels.to(device).float().unsqueeze(1)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * images.size(0)
            preds = (torch.sigmoid(outputs) > 0.5).float()
            train_correct += (preds == labels).sum().item()
            train_total += labels.numel()

        model.eval()
        val_loss, val_correct, val_total = 0.0, 0, 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device).float().unsqueeze(1)
                outputs = model(images)
                val_loss += criterion(outputs, labels).item() * images.size(0)
                preds = (torch.sigmoid(outputs) > 0.5).float()
                val_correct += (preds == labels).sum().item()
                val_total += labels.numel()

        hist['train_loss'].append(train_loss / train_total)
        hist['val_loss'].append(val_loss / val_total)
        hist['train_acc'].append(train_correct / train_total)
        hist['val_acc'].append(val_correct / val_total)

    elapsed = time.time() - start
    return hist, elapsed"""),
    new_markdown_cell("## Train the base hybrid `model` (small config)"),
    new_code_cell("""model = CNNViTHybrid(embed_dim=128, num_heads=4, transformer_depth=4)
history_model, time_model = train_model(model, train_loader, val_loader, epochs=5, device=device)
print(f'Base ViT  -> val_acc={history_model["val_acc"][-1]:.4f}, training time={time_model:.1f}s')"""),
    new_markdown_cell("### Task 4: Design and train the CNN-ViT hybrid `model_test` — epochs=5, mlp heads=12, embed_dim=768, transformer block depth=12"),
    new_code_cell("""model_test = CNNViTHybrid(embed_dim=768, num_heads=12, transformer_depth=12)
history_model_test, time_model_test = train_model(model_test, train_loader, val_loader, epochs=5, device=device)
print(f'model_test -> val_acc={history_model_test["val_acc"][-1]:.4f}, training time={time_model_test:.1f}s')

os.makedirs('models', exist_ok=True)
torch.save(model_test.state_dict(), 'models/pytorch_vit_test.pth')
print('model_test saved -> models/pytorch_vit_test.pth')"""),
    new_markdown_cell("### Task 5: Compare the performance of `model` with `model_test` by plotting the validation loss"),
    new_code_cell("""plt.figure(figsize=(8, 5))
plt.plot(history_model['val_loss'], label='model (embed=128, heads=4, depth=4)')
plt.plot(history_model_test['val_loss'], label='model_test (embed=768, heads=12, depth=12)')
plt.title('Validation Loss Comparison: model vs model_test')
plt.xlabel('Epoch')
plt.ylabel('Validation Loss')
plt.legend()
plt.grid(True)
plt.savefig('models/vit_pytorch_val_loss_comparison.png')
plt.show()"""),
    new_markdown_cell("### Task 6: Compare the training times of `model` with `model_test`"),
    new_code_cell("""times = [time_model, time_model_test]
names = ['model', 'model_test']

plt.figure(figsize=(7, 5))
bars = plt.bar(names, times, color=['steelblue', 'coral'])
plt.title('Training Time Comparison (seconds)')
plt.ylabel('Training time (s)')
for bar, t in zip(bars, times):
    plt.text(bar.get_x() + bar.get_width() / 2, t, f'{t:.1f}s', ha='center', va='bottom')
plt.grid(True, axis='y')
plt.savefig('models/vit_pytorch_time_comparison.png')
plt.show()"""),
])
save(Q8, "Question_8/Lab8_Vision_Transformers_PyTorch.ipynb")

# ============================================================================
# Question 9 - Module 3: Land Classification: CNN-Transformer Integration Evaluation
# ============================================================================
Q9 = notebook("Module 3: Land Classification: CNN-Transformer Integration Evaluation", [
    new_markdown_cell("> **Assignment (8 points):** Final evaluation of the Keras and PyTorch CNN-ViT hybrid models on the land classification task."),
    new_code_cell(BOOT),
    new_code_cell("""import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, roc_auc_score, roc_curve)"""),
    new_markdown_cell("## Shared evaluation helper: `print_metrics`"),
    new_code_cell("""def print_metrics(y_true, y_pred, model_name):
    acc  = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    rec  = recall_score(y_true, y_pred)
    f1   = f1_score(y_true, y_pred)
    cm   = confusion_matrix(y_true, y_pred)
    print(f'\\n========== {model_name} ==========')
    print(f'Accuracy : {acc:.4f}')
    print(f'Precision: {prec:.4f}')
    print(f'Recall   : {rec:.4f}')
    print(f'F1 score : {f1:.4f}')
    print(f'Confusion matrix:\\n{cm}')

    auc = roc_auc_score(y_true, y_pred)
    fpr, tpr, _ = roc_curve(y_true, y_pred)
    plt.figure(figsize=(5, 4))
    plt.plot(fpr, tpr, label=f'{model_name} (AUC={auc:.3f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend()
    plt.grid(True)
    os.makedirs('models', exist_ok=True)
    plt.savefig(f'models/roc_{model_name.replace(" ", "_")}.png')
    plt.show()

    return {'accuracy': acc, 'precision': prec, 'recall': rec, 'f1': f1,
            'confusion_matrix': cm, 'auc': auc}"""),
    new_markdown_cell("### Task 1: Define the dataset directory, dataloader and model hyperparameters (same as used during training)"),
    new_code_cell("""data_dir = './images_dataSAT'
BATCH_SIZE = 32

val_transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
val_dataset = datasets.ImageFolder(data_dir, transform=val_transform)
val_dataset, _ = random_split(val_dataset, [400, len(val_dataset) - 400])
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

# Model hyperparameters (identical to training)
EMBED_DIM = 768
NUM_HEADS = 12
TRANSFORMER_DEPTH = 12"""),
    new_markdown_cell("### Task 2: Instantiate the PyTorch model"),
    new_code_cell("""class CNNViTHybrid(nn.Module):
    def __init__(self, embed_dim=128, num_heads=4, transformer_depth=4, num_classes=1):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(128, 256, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.num_patches = 4 * 4
        self.patch_embed = nn.Linear(256, embed_dim)
        self.pos_embed = nn.Parameter(torch.randn(1, self.num_patches, embed_dim) * 0.02)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim, nhead=num_heads, dim_feedforward=4 * embed_dim,
            batch_first=True, dropout=0.1, norm_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=transformer_depth)
        self.head = nn.Sequential(nn.LayerNorm(embed_dim), nn.Linear(embed_dim, num_classes))

    def forward(self, x):
        x = self.cnn(x)
        B, C, H, W = x.shape
        x = x.permute(0, 2, 3, 1).reshape(B, H * W, C)
        x = self.patch_embed(x) + self.pos_embed
        x = self.transformer(x)
        x = x.mean(dim=1)
        return self.head(x)


model_pt = CNNViTHybrid(embed_dim=EMBED_DIM, num_heads=NUM_HEADS, transformer_depth=TRANSFORMER_DEPTH)
model_pt.load_state_dict(torch.load('models/pytorch_vit_test.pth', map_location='cpu', weights_only=True))
model_pt.eval()
print('PyTorch hybrid model instantiated (768 / 12 / 12)')

y_true_pt = []
y_prob_pt = []
with torch.no_grad():
    for images, labels in val_loader:
        out = torch.sigmoid(model_pt(images))
        y_prob_pt.extend(out.squeeze(1).tolist())
        y_true_pt.extend(labels.tolist())

y_true_pt = np.array(y_true_pt)
y_pred_pt = (np.array(y_prob_pt) > 0.5).astype(int).flatten()"""),
    new_markdown_cell("### Task 3: Print the evaluation metrics for the **Keras** ViT model named `Keras CNN-Vit Hybrid Model`"),
    new_code_cell("""keras_vit = tf.keras.models.load_model('models/vit_hybrid.keras')

datagen = ImageDataGenerator(rescale=1. / 255)
test_generator = datagen.flow_from_directory(
    data_dir, target_size=(64, 64), batch_size=BATCH_SIZE,
    class_mode='binary', shuffle=False, seed=42)

y_true_keras = test_generator.classes
y_prob_keras = keras_vit.predict(test_generator, verbose=0).flatten()
y_pred_keras = (y_prob_keras > 0.5).astype(int).flatten()

keras_metrics = print_metrics(y_true_keras, y_pred_keras, 'Keras CNN-Vit Hybrid Model')"""),
    new_markdown_cell("### Task 4: Print the evaluation metrics for the **PyTorch** ViT model named `PyTorch CNN-Vit Hybrid Model`"),
    new_code_cell("""torch_metrics = print_metrics(y_true_pt, y_pred_pt, 'PyTorch CNN-Vit Hybrid Model')"""),
    new_markdown_cell("## Final comparison"),
    new_code_cell("""print(f'{"Metric":<12}{"Keras CNN-Vit":<16}{"PyTorch CNN-Vit":<16}')
for key in ['accuracy', 'precision', 'recall', 'f1', 'auc']:
    print(f'{key:<12}{keras_metrics[key]:<16.4f}{torch_metrics[key]:<16.4f}')"""),
])
save(Q9, "Question_9/Lab9_CNN_Transformer_Evaluation.ipynb")

print("All 9 notebooks generated.")
