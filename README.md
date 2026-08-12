# mini-lm

A small C++ project for learning how language models work by building one from the ground up.

The goal is not to create another production ML framework. The goal is to implement the important pieces explicitly enough to understand the complete path from tensors and backpropagation to training and running a small language model.

## Goals

- Build the core ML components in modern C++.
- Understand tensor representation, neural networks and automatic differentiation.
- Train simple models before moving to language modelling.
- Implement attention and a small Transformer-based language model.
- Keep training and inference clearly separated.
- Eventually train and run a small custom language model.
- Use OpenML for selected datasets and experiments.

## Milestones

### M1 — Tensor and Autograd

Build the numerical foundation.

- Tensor storage
- Shape and strides
- Indexing
- Basic tensor operations
- Matrix multiplication
- Neural network forward pass
- Automatic differentiation
- MSE loss
- SGD
- Train a simple model such as `y = 3x + 2`

### M2 — Datasets and Classification

Build the first complete ML workflow.

- Dataset abstraction
- Samples and batches
- DataLoader
- Train/validation split
- Cross-entropy loss
- MLP
- Optimizers
- OpenML integration
- Train and evaluate a classifier using an OpenML dataset

### M3 — Language Modelling

Move from general ML to text.

- Character-level tokenizer
- Vocabulary
- Text datasets
- Sequence batching
- Embeddings
- Next-token prediction
- Simple language model
- Text generation

### M4 — Transformer

Build the actual language model architecture.

- Q/K/V projections
- Scaled dot-product attention
- Causal masking
- Multi-head attention
- Layer normalization
- Feed-forward network
- Residual connections
- Transformer blocks
- Small GPT-like language model
- Train a small custom model

### M5 — Runtime

Separate model execution from training.

- Model serialization
- Model loading
- Inference-only tensor operations
- Runtime without autograd or optimizers
- Text generation
- Sampling
- KV cache
- Performance improvements
- Optional SIMD, threading and quantization

## Applications

The repository contains several applications built on top of the libraries.

### `train`

Training application.

Responsible for:

- loading datasets
- configuring models
- training
- validation
- checkpoints
- metrics

### `runtime-example`

Minimal example showing how to embed the inference runtime in a C++ application.

Conceptually:

```cpp
#include <mini_lm/runtime.hpp>

int main()
{
    mini_lm::Runtime runtime{"model.mlm"};

    auto result = runtime.generate("Hello");

    std::cout << result << '\n';
}
```

This application should remain intentionally small and serve as documentation for consumers of the runtime library.

### `frontend`

Interactive frontend built on top of the runtime.

Responsible for user-facing functionality such as:

- loading a model
- entering prompts
- configuring generation parameters
- displaying generated tokens/text
- inspecting basic runtime statistics

The frontend must consume the same public runtime API as any external application.

## mini-lm API

`mini-lm` should expose a small public C++ API that can be integrated into external applications without depending on the training stack.

The API should primarily provide access to:

- model loading
- tokenization
- prompt evaluation
- text generation
- generation configuration
- runtime statistics
- model metadata

A possible high-level API:

```cpp
#include <mini_lm/runtime.hpp>

mini_lm::Runtime runtime{"model.mlm"};

mini_lm::GenerationConfig config{
    .max_tokens = 128,
    .temperature = 0.8f,
    .top_k = 40,
};

auto result = runtime.generate(
    "The meaning of life is",
    config
);
```

For applications that need more control, the runtime may also expose lower-level operations:

```cpp
auto tokens = runtime.tokenize("Hello world");

for (auto token : tokens) {
    runtime.evaluate(token);
}

auto next = runtime.sample();
```

The public API should remain independent from:

- autograd
- optimizers
- datasets
- OpenML
- training loops

This makes the runtime usable as a normal C++ dependency in applications that only need inference.

Potential integrations include:

```text
Desktop application
Game / game engine
CLI tool
Embedded service
Backend process
Existing C++ application
Custom UI
```

The `runtime-example` application should act as the reference consumer of this API, while `frontend` should prove that a larger application can be built entirely on top of the same public interface.

## Architecture

```text
                   ┌──────────────┐
                   │    OpenML    │
                   └──────┬───────┘
                          │
                       Dataset
                          │
                          ▼
Tensor ──► Autograd ──► NN ──► Transformer
  │                         │
  │                         ▼
  │                       Model
  │                         │
  └─────────────────────────┤
                            ▼
                         Runtime
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
          runtime-example          frontend
                            │
                            ▼
                      external apps
```

Training-specific functionality such as datasets, autograd and optimizers should not be required by the inference runtime.

## Repository Structure

```text
mini-lm/
├── libs/
│   ├── tensor/
│   ├── math/
│   ├── autograd/
│   ├── nn/
│   ├── optim/
│   ├── dataset/
│   ├── openml/
│   ├── tokenizer/
│   ├── transformer/
│   ├── model/
│   └── runtime/
│
├── apps/
│   ├── train/
│   ├── runtime-example/
│   └── frontend/
│
├── tests/
└── CMakeLists.txt
```

Each library should expose a small public API and remain a separate CMake target.

The project starts deliberately simple: CPU, `float32`, contiguous tensors and straightforward implementations. Optimizations and more sophisticated abstractions are introduced only when there is a concrete reason for them.

The first target is simple:

> Make a C++ model learn `y = 3x + 2`.

Then make it predict tokens.
