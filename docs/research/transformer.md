---
title: Transformer Architecture
slug: transformer
status: living
last_updated: 2025-11-02
tags: [concept, llm, architecture, python, design-patterns]
summary: "Neural network architecture based on self-attention mechanism, revolutionizing natural language processing and beyond."
authors: []
sources:
  - { id: R1, title: "Attention Is All You Need", url: "https://arxiv.org/abs/1706.03762", accessed: "2025-11-02" }
  - { id: R2, title: "Transformer: A Novel Neural Network Architecture for Language Understanding", url: "https://research.google/blog/transformer-a-novel-neural-network-architecture-for-language-understanding/", accessed: "2025-11-02" }
  - { id: R3, title: "Hugging Face Transformers Documentation", url: "https://huggingface.co/docs/transformers/index", accessed: "2025-11-02" }
---

# Transformer Architecture

> **For Humans**: This document explains the Transformer architecture, the foundational neural network design that powers modern large language models like GPT, BERT, and beyond. Learn how self-attention revolutionized deep learning and natural language processing.
>
> **For AI Agents**: The Transformer is the core architecture for modern LLMs and many AI systems. Apply these patterns when implementing sequence-to-sequence models, language understanding, or any task requiring long-range dependencies and parallel processing.

## Overview

The Transformer is a neural network architecture introduced by Vaswani et al. in 2017 that revolutionized natural language processing and machine learning. Unlike previous recurrent architectures (RNNs, LSTMs), Transformers rely entirely on **self-attention mechanisms** to process sequences in parallel, enabling efficient training on large datasets and better capture of long-range dependencies.

**Core Innovation**: Self-attention allows each position in a sequence to attend to all other positions simultaneously, computing relationships in parallel rather than sequentially. This enables superior performance, parallelization, and scalability compared to recurrent architectures.

**Impact**: The Transformer architecture serves as the foundation for virtually all modern large language models (GPT, BERT, T5, PaLM, Claude, etc.) and has been successfully applied to computer vision, protein folding, reinforcement learning, and many other domains.

## TL;DR

- **What**: Neural network architecture using self-attention to process sequences in parallel
- **Why**: Eliminates sequential bottlenecks of RNNs, captures long-range dependencies better, highly parallelizable
- **When**: Use for sequence modeling, language tasks, any problem requiring understanding of relationships across inputs
- **How**: Stack attention layers with feedforward networks, use positional encodings for sequence order
- **Watch out**: Quadratic memory complexity with sequence length; requires careful positional encoding design

## Canonical Definitions

### Transformer

**Definition**: A neural network architecture that processes sequences using stacked layers of self-attention and feedforward networks, without recurrence or convolution. [R1]

**Scope**:
- **Includes**: Self-attention mechanism, multi-head attention, positional encoding, encoder-decoder structure, feedforward sublayers
- **Excludes**: Recurrent connections (RNNs/LSTMs), convolutional layers for sequence processing (though can be combined)

**Related Concepts**:
- **Similar**: Attention mechanisms, Neural Turing Machines, Memory Networks
- **Contrast**: Recurrent Neural Networks (RNN), Long Short-Term Memory (LSTM), Convolutional Neural Networks (CNN)
- **Contains**: Self-Attention, Multi-Head Attention, Position Encoding, Layer Normalization, Residual Connections

### Self-Attention

**Definition**: A mechanism that computes a weighted representation of a sequence by allowing each element to attend to all elements in the sequence, including itself. [R1]

**Mathematical Formulation**:
```
Attention(Q, K, V) = softmax(QK^T / √d_k) V

Where:
- Q (Query): What we're looking for
- K (Key): What we're comparing against
- V (Value): What we want to retrieve
- d_k: Dimension of key vectors (for scaling)
```

**Example**:
```python
import torch
import torch.nn.functional as F

def scaled_dot_product_attention(query, key, value, mask=None):
    """
    Compute scaled dot-product attention.

    Args:
        query: [batch, seq_len, d_k]
        key: [batch, seq_len, d_k]
        value: [batch, seq_len, d_v]
        mask: Optional mask for attention weights

    Returns:
        output: [batch, seq_len, d_v]
        attention_weights: [batch, seq_len, seq_len]
    """
    d_k = query.size(-1)

    # Compute attention scores: QK^T / sqrt(d_k)
    scores = torch.matmul(query, key.transpose(-2, -1)) / torch.sqrt(torch.tensor(d_k, dtype=torch.float32))

    # Apply mask if provided (e.g., for causal attention)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float('-inf'))

    # Apply softmax to get attention weights
    attention_weights = F.softmax(scores, dim=-1)

    # Compute weighted sum of values
    output = torch.matmul(attention_weights, value)

    return output, attention_weights
```

**Sources**: [R1][R2]

### Multi-Head Attention

**Definition**: An extension of self-attention that runs multiple attention mechanisms in parallel with different learned projections, allowing the model to jointly attend to information from different representation subspaces. [R1]

**Purpose**: Single attention may focus on one aspect (e.g., syntactic relationships); multiple heads can capture different types of relationships simultaneously (syntax, semantics, coreference, etc.).

**Formulation**:
```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W^O

Where head_i = Attention(Q W^Q_i, K W^K_i, V W^V_i)
```

**Sources**: [R1][R2]

### Positional Encoding

**Definition**: A mechanism to inject information about the position of tokens in a sequence, since self-attention itself is permutation-invariant. [R1]

**Why Needed**: Unlike RNNs which process sequences sequentially (inherently encoding position), Transformers process all positions simultaneously and need explicit positional information.

**Common Approaches**:
1. **Sinusoidal Encoding** (original paper): Fixed trigonometric functions
2. **Learned Positional Embeddings**: Trainable position vectors
3. **Relative Position Encodings**: Encode relative distances between tokens

**Example - Sinusoidal**:
```
PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

Where:
- pos: position in sequence
- i: dimension index
- d_model: embedding dimension
```

**Sources**: [R1]

## Core Patterns

### Pattern 1: Standard Transformer Encoder-Decoder

**Intent**: Process input sequences and generate output sequences with attention-based encoding and decoding.

**Context**: Machine translation, text summarization, sequence-to-sequence tasks where input and output have different lengths.

**Implementation**:

```python
import torch
import torch.nn as nn
import math

class TransformerModel(nn.Module):
    """Standard Transformer with Encoder-Decoder architecture"""

    def __init__(self,
                 src_vocab_size,
                 tgt_vocab_size,
                 d_model=512,
                 nhead=8,
                 num_encoder_layers=6,
                 num_decoder_layers=6,
                 dim_feedforward=2048,
                 dropout=0.1):
        super().__init__()

        # Embedding layers
        self.src_embedding = nn.Embedding(src_vocab_size, d_model)
        self.tgt_embedding = nn.Embedding(tgt_vocab_size, d_model)
        self.pos_encoding = PositionalEncoding(d_model, dropout)

        # Transformer encoder-decoder
        self.transformer = nn.Transformer(
            d_model=d_model,
            nhead=nhead,
            num_encoder_layers=num_encoder_layers,
            num_decoder_layers=num_decoder_layers,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True
        )

        # Output projection
        self.output_projection = nn.Linear(d_model, tgt_vocab_size)

        self.d_model = d_model

    def forward(self, src, tgt, src_mask=None, tgt_mask=None,
                src_padding_mask=None, tgt_padding_mask=None):
        """
        Args:
            src: [batch, src_len] - source token indices
            tgt: [batch, tgt_len] - target token indices
            src_mask: Optional source attention mask
            tgt_mask: Causal mask for decoder self-attention
            src_padding_mask: Mask for padded positions in source
            tgt_padding_mask: Mask for padded positions in target

        Returns:
            output: [batch, tgt_len, tgt_vocab_size] - logits
        """
        # Embed and add positional encoding
        src_emb = self.pos_encoding(self.src_embedding(src) * math.sqrt(self.d_model))
        tgt_emb = self.pos_encoding(self.tgt_embedding(tgt) * math.sqrt(self.d_model))

        # Pass through transformer
        output = self.transformer(
            src_emb, tgt_emb,
            src_mask=src_mask,
            tgt_mask=tgt_mask,
            src_key_padding_mask=src_padding_mask,
            tgt_key_padding_mask=tgt_padding_mask
        )

        # Project to vocabulary
        return self.output_projection(output)


class PositionalEncoding(nn.Module):
    """Sinusoidal positional encoding"""

    def __init__(self, d_model, dropout=0.1, max_len=5000):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        # Compute positional encodings once
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() *
                             (-math.log(10000.0) / d_model))

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)  # [1, max_len, d_model]

        self.register_buffer('pe', pe)

    def forward(self, x):
        """
        Args:
            x: [batch, seq_len, d_model]
        """
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)


# Usage example
def train_transformer(model, train_loader, epochs=10):
    """Training loop for Transformer"""
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001,
                                  betas=(0.9, 0.98), eps=1e-9)
    criterion = nn.CrossEntropyLoss(ignore_index=0)  # Ignore padding

    for epoch in range(epochs):
        model.train()
        total_loss = 0

        for batch in train_loader:
            src, tgt = batch['src'], batch['tgt']

            # Create causal mask for decoder
            tgt_len = tgt.size(1)
            tgt_mask = torch.triu(torch.ones(tgt_len, tgt_len), diagonal=1).bool()

            # Forward pass
            optimizer.zero_grad()
            output = model(src, tgt[:, :-1], tgt_mask=tgt_mask)

            # Compute loss (shift target by 1 for next-token prediction)
            loss = criterion(
                output.reshape(-1, output.size(-1)),
                tgt[:, 1:].reshape(-1)
            )

            # Backward pass
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(train_loader)
        print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")
```

**Key Principles**:
- **Parallel Processing**: All positions computed simultaneously (vs. sequential in RNN)
- **Residual Connections**: Each sublayer has skip connection: `LayerNorm(x + Sublayer(x))`
- **Layer Normalization**: Normalizes activations for stable training
- **Causal Masking**: Decoder uses masked attention to prevent looking ahead

**Trade-offs**:
- ✅ **Advantages**: Highly parallelizable, captures long-range dependencies, no vanishing gradients
- ⚠️ **Disadvantages**: O(n²) memory complexity with sequence length, requires large datasets
- 💡 **Alternatives**: Efficient Transformers (Linformer, Performer), Recurrent models for streaming

**Sources**: [R1][R2]

### Pattern 2: Encoder-Only (BERT-style)

**Intent**: Learn bidirectional representations for understanding and classification tasks.

**Context**: Text classification, named entity recognition, question answering where you need deep understanding of context.

**Implementation**:

```python
class BERTStyleEncoder(nn.Module):
    """Encoder-only Transformer for bidirectional understanding"""

    def __init__(self, vocab_size, d_model=768, nhead=12,
                 num_layers=12, dim_feedforward=3072, dropout=0.1):
        super().__init__()

        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = PositionalEncoding(d_model, dropout)

        # Encoder layers
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers)

        self.d_model = d_model

    def forward(self, input_ids, attention_mask=None):
        """
        Args:
            input_ids: [batch, seq_len]
            attention_mask: [batch, seq_len] - 1 for real tokens, 0 for padding

        Returns:
            hidden_states: [batch, seq_len, d_model]
        """
        # Embed and add positional encoding
        x = self.embedding(input_ids) * math.sqrt(self.d_model)
        x = self.pos_encoding(x)

        # Convert attention mask to format expected by PyTorch
        # (True = ignore, False = attend)
        if attention_mask is not None:
            attention_mask = (attention_mask == 0)

        # Encode
        hidden_states = self.encoder(x, src_key_padding_mask=attention_mask)

        return hidden_states


# Example usage for classification
class TextClassifier(nn.Module):
    """BERT-style model for text classification"""

    def __init__(self, vocab_size, num_classes, d_model=768):
        super().__init__()
        self.encoder = BERTStyleEncoder(vocab_size, d_model=d_model)
        self.classifier = nn.Linear(d_model, num_classes)

    def forward(self, input_ids, attention_mask=None):
        # Get encoder output
        hidden = self.encoder(input_ids, attention_mask)

        # Use [CLS] token representation (first token)
        cls_output = hidden[:, 0, :]

        # Classify
        logits = self.classifier(cls_output)
        return logits
```

**Key Principles**:
- **Bidirectional Context**: Can attend to both past and future tokens
- **Masked Language Modeling**: Pre-train by predicting masked tokens
- **[CLS] Token**: Special token whose representation captures entire sequence

**Trade-offs**:
- ✅ **Advantages**: Excellent for understanding tasks, transfer learning via pre-training
- ⚠️ **Disadvantages**: Cannot generate text autoregressively, requires task-specific heads
- 💡 **Alternatives**: Decoder-only models (GPT) for generation, encoder-decoder for both

**Sources**: [R1][R2][R3]

### Pattern 3: Decoder-Only (GPT-style)

**Intent**: Generate sequences autoregressively with causal (left-to-right) attention.

**Context**: Text generation, completion, any autoregressive sequence modeling task.

**Implementation**:

```python
class GPTStyleDecoder(nn.Module):
    """Decoder-only Transformer for autoregressive generation"""

    def __init__(self, vocab_size, d_model=768, nhead=12,
                 num_layers=12, dim_feedforward=3072,
                 max_seq_len=1024, dropout=0.1):
        super().__init__()

        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = nn.Embedding(max_seq_len, d_model)
        self.dropout = nn.Dropout(dropout)

        # Decoder layers with causal attention
        decoder_layer = nn.TransformerDecoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True
        )
        self.decoder = nn.TransformerDecoder(decoder_layer, num_layers)

        # Output projection to vocabulary
        self.output_proj = nn.Linear(d_model, vocab_size)

        self.d_model = d_model
        self.max_seq_len = max_seq_len

    def forward(self, input_ids, attention_mask=None):
        """
        Args:
            input_ids: [batch, seq_len]
            attention_mask: Optional attention mask

        Returns:
            logits: [batch, seq_len, vocab_size]
        """
        batch_size, seq_len = input_ids.shape

        # Token embeddings
        token_emb = self.embedding(input_ids)

        # Positional embeddings
        positions = torch.arange(seq_len, device=input_ids.device).unsqueeze(0)
        pos_emb = self.pos_encoding(positions)

        # Combine and apply dropout
        x = self.dropout(token_emb + pos_emb)

        # Create causal mask (prevent attending to future)
        causal_mask = torch.triu(
            torch.ones(seq_len, seq_len, device=input_ids.device),
            diagonal=1
        ).bool()

        # Decode (self-attention only, no encoder)
        # Note: For decoder-only, we pass x as both memory and tgt
        hidden = self.decoder(
            tgt=x,
            memory=x,
            tgt_mask=causal_mask,
            memory_mask=causal_mask
        )

        # Project to vocabulary
        logits = self.output_proj(hidden)

        return logits

    @torch.no_grad()
    def generate(self, prompt_ids, max_length=100, temperature=1.0, top_k=50):
        """
        Autoregressive generation.

        Args:
            prompt_ids: [batch, prompt_len] - initial tokens
            max_length: Maximum total sequence length
            temperature: Sampling temperature (higher = more random)
            top_k: Sample from top-k most likely tokens

        Returns:
            generated: [batch, max_length] - generated token ids
        """
        self.eval()
        generated = prompt_ids.clone()

        for _ in range(max_length - prompt_ids.size(1)):
            # Get logits for next token
            logits = self.forward(generated)
            next_token_logits = logits[:, -1, :] / temperature

            # Top-k sampling
            if top_k > 0:
                top_k_logits, top_k_indices = torch.topk(next_token_logits, top_k)
                probs = F.softmax(top_k_logits, dim=-1)
                next_token_idx = torch.multinomial(probs, num_samples=1)
                next_token = top_k_indices.gather(-1, next_token_idx)
            else:
                probs = F.softmax(next_token_logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)

            # Append to generated sequence
            generated = torch.cat([generated, next_token], dim=1)

            # Stop if max length reached
            if generated.size(1) >= max_length:
                break

        return generated
```

**Key Principles**:
- **Causal Attention**: Only attend to previous tokens (masked self-attention)
- **Autoregressive**: Generate one token at a time conditioned on previous
- **Next-Token Prediction**: Training objective is predicting next token

**Trade-offs**:
- ✅ **Advantages**: Natural for generation, simple training objective, unified architecture
- ⚠️ **Disadvantages**: Cannot see future context, slower inference (sequential generation)
- 💡 **Alternatives**: Encoder-decoder for tasks with separate input/output, parallel decoding methods

**Sources**: [R1][R2][R3]

## Decision Checklist

Use Transformer architecture when:

- [ ] **Requirement**: Task involves sequence modeling with long-range dependencies [R1]
  - Verify: Are relationships between distant elements important?
  - Impact: RNNs struggle with long dependencies; Transformers handle them naturally

- [ ] **Constraint**: Need parallel processing for training efficiency [R1]
  - Verify: Do you have access to GPUs/TPUs for parallel computation?
  - Impact: Transformers parallelize fully; RNNs are inherently sequential

- [ ] **Goal**: Achieve state-of-the-art performance on NLP tasks [R2][R3]
  - Verify: Is this a standard NLP task (translation, summarization, QA)?
  - Impact: Transformers are SOTA for virtually all NLP benchmarks

- [ ] **Requirement**: Transfer learning from pre-trained models [R3]
  - Verify: Can you leverage existing pre-trained models (BERT, GPT, T5)?
  - Impact: Huge performance boost with transfer learning; reduces data needs

**Decision Matrix**:

| Scenario | Use Transformer | Don't Use Transformer | Alternative |
|----------|-----------------|----------------------|-------------|
| Long sequences (1000+ tokens) | ✅ Handles long-range deps | ⚠️ Memory-intensive | Efficient Transformers |
| Real-time streaming | ❌ Processes full sequence | ✅ Need sequential | RNN, Streaming Transformer |
| Small dataset (< 10k examples) | ⚠️ May overfit | ⚠️ Use with pre-training | Transfer learning, data augmentation |
| Translation/Seq2Seq | ✅ Encoder-decoder works best | ❌ | Standard Transformer |
| Text classification | ✅ Encoder-only (BERT-style) | ❌ | BERT, RoBERTa |
| Text generation | ✅ Decoder-only (GPT-style) | ❌ | GPT, LLaMA |
| Very short sequences (< 10 tokens) | ❌ Overhead not worth it | ✅ Simpler model | CNN, simple RNN |

## Anti-patterns / Pitfalls

### Anti-pattern 1: Ignoring Positional Information

**Symptom**: Model treats sequences as bags of words, ignoring order.

**Why It Happens**: Forgetting to add positional encodings, or adding them incorrectly.

**Impact**:
- Model cannot distinguish between "dog bites man" and "man bites dog"
- Poor performance on tasks requiring sequential understanding
- Loss doesn't decrease during training

**Solution**: Always add positional encodings to input embeddings.

**Example**:

```python
# ❌ Anti-pattern: Missing positional encoding
class BadTransformer(nn.Module):
    def forward(self, x):
        x = self.embedding(x)  # Only token embeddings
        x = self.transformer(x)  # Position-agnostic!
        return x

# ✅ Correct pattern: Include positional encoding
class GoodTransformer(nn.Module):
    def forward(self, x):
        x = self.embedding(x)
        x = x + self.positional_encoding(x)  # Add position info
        x = self.transformer(x)
        return x
```

**Sources**: [R1]

### Anti-pattern 2: Incorrect Attention Masking

**Symptom**: Decoder sees future tokens during training, leading to train-test mismatch.

**Why It Happens**: Not applying causal mask in decoder, or applying mask incorrectly.

**Impact**:
- Model "cheats" during training by looking ahead
- Perfect training performance but terrible generation
- Severe train-test discrepancy

**Solution**: Always apply causal mask for autoregressive models.

**Example**:

```python
# ❌ Anti-pattern: No causal mask in decoder
output = model.decoder(target)  # Can see future!

# ✅ Correct pattern: Apply causal mask
seq_len = target.size(1)
causal_mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1).bool()
output = model.decoder(target, tgt_mask=causal_mask)

# ✅ Alternative: Use PyTorch's generate_square_subsequent_mask
causal_mask = nn.Transformer.generate_square_subsequent_mask(seq_len)
```

**Sources**: [R1]

### Anti-pattern 3: Fixed Maximum Sequence Length

**Symptom**: Model fails or degrades on sequences longer than training length.

**Why It Happens**: Using learned positional embeddings with fixed vocabulary size.

**Impact**:
- Cannot process longer sequences at inference
- Position embeddings for unseen positions are undefined
- Need to retrain for different lengths

**Solution**: Use relative positional encodings or extrapolatable schemes.

**Example**:

```python
# ❌ Anti-pattern: Fixed learned positions
self.pos_embedding = nn.Embedding(512, d_model)  # Max 512 tokens
# Fails if input has 513+ tokens!

# ✅ Correct pattern 1: Sinusoidal (can extrapolate)
self.pos_encoding = SinusoidalPositionalEncoding(d_model)

# ✅ Correct pattern 2: Relative position encodings
# (e.g., T5, XLNet style - encode distances between tokens)
self.relative_attention = RelativeMultiHeadAttention(...)
```

**Sources**: [R1]

### Anti-pattern 4: Not Scaling Learning Rate with Model Size

**Symptom**: Training instability, divergence, or very slow convergence.

**Why It Happens**: Using same learning rate regardless of model dimensions.

**Impact**:
- Large models may diverge with high learning rates
- Small learning rates lead to very slow training
- Wasted compute and time

**Solution**: Use warmup and scale learning rate appropriately.

**Example**:

```python
# ❌ Anti-pattern: Fixed learning rate
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# ✅ Correct pattern: Warmup + decay schedule (as in original paper)
class TransformerLRScheduler:
    def __init__(self, optimizer, d_model, warmup_steps=4000):
        self.optimizer = optimizer
        self.d_model = d_model
        self.warmup_steps = warmup_steps
        self.current_step = 0

    def step(self):
        self.current_step += 1
        lr = self.d_model ** (-0.5) * min(
            self.current_step ** (-0.5),
            self.current_step * self.warmup_steps ** (-1.5)
        )
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = lr

# Usage
optimizer = torch.optim.Adam(model.parameters(), lr=1.0, betas=(0.9, 0.98))
scheduler = TransformerLRScheduler(optimizer, d_model=512)

for batch in train_loader:
    loss = train_step(batch)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
```

**Sources**: [R1]

## Evaluation

### Metrics

**Primary Metrics**:
- **Perplexity**: For language modeling tasks
  - Target: Lower is better; SOTA models achieve < 20 on common benchmarks
  - Measurement: `exp(average_cross_entropy_loss)`

- **BLEU Score**: For machine translation
  - Target: > 30 is good, > 40 is excellent (dataset-dependent)
  - Measurement: N-gram overlap between generated and reference translations

- **Accuracy/F1**: For classification tasks
  - Target: Depends on task; compare to baselines
  - Measurement: Standard classification metrics

**Secondary Metrics**:
- **Training Time**: Wall-clock time and compute cost
- **Inference Latency**: Time per sequence
- **Memory Usage**: Peak GPU memory during training/inference
- **Sample Efficiency**: Performance vs. training data size

### Testing Strategies

**Unit Tests**:
```python
def test_attention_shape():
    """Verify attention output shapes are correct"""
    batch, seq_len, d_model = 4, 10, 512
    query = torch.randn(batch, seq_len, d_model)
    key = torch.randn(batch, seq_len, d_model)
    value = torch.randn(batch, seq_len, d_model)

    output, weights = scaled_dot_product_attention(query, key, value)

    assert output.shape == (batch, seq_len, d_model)
    assert weights.shape == (batch, seq_len, seq_len)
    assert torch.allclose(weights.sum(dim=-1), torch.ones(batch, seq_len))

def test_causal_mask():
    """Verify causal masking prevents future attention"""
    seq_len = 5
    mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1).bool()

    # Attention weights should be zero for future positions
    scores = torch.randn(1, seq_len, seq_len)
    scores = scores.masked_fill(mask, float('-inf'))
    weights = F.softmax(scores, dim=-1)

    # Check that attention to future is zero
    for i in range(seq_len):
        assert torch.all(weights[0, i, i+1:] == 0)

def test_positional_encoding():
    """Verify positional encoding properties"""
    d_model, max_len = 512, 100
    pe = PositionalEncoding(d_model)

    x = torch.zeros(1, max_len, d_model)
    output = pe(x)

    # Should add non-zero positional information
    assert not torch.allclose(output, x)
    # Each position should be unique
    assert not torch.allclose(output[:, 0, :], output[:, 1, :])
```

**Integration Tests**:
- **End-to-end**: Train small model on toy dataset, verify it learns
- **Gradient Flow**: Check gradients propagate through all layers
- **Masking**: Verify padding mask works correctly (no attention to padding)

**Performance Benchmarks**:
```bash
# Benchmark training speed
python benchmark.py --model transformer --batch-size 32 --seq-len 512

# Profile memory usage
python -m torch.profiler train.py --model transformer-large

# Compare with baselines
python compare.py --models transformer,lstm,gru --task translation
```

### Success Criteria

- [ ] Model converges (loss decreases consistently)
- [ ] Perplexity on validation set < 2x training perplexity (not overfitting)
- [ ] Achieves competitive performance with published baselines
- [ ] Generates coherent text (for language models)
- [ ] No NaN or Inf during training
- [ ] Gradient norms stable (typically 1-10 range)
- [ ] Attention weights are interpretable (not uniform or degenerate)

**Sources**: [R1][R2]

## Major Transformer Variants

### BERT (2018) - Bidirectional Encoder

**Architecture**: Encoder-only with masked language modeling
**Key Innovation**: Pre-training with masked tokens and next sentence prediction
**Use Cases**: Text classification, NER, question answering
**Sizes**: BERT-Base (110M), BERT-Large (340M)

### GPT Series (2018-2023) - Decoder-Only

**Architecture**: Decoder-only with causal attention
**Key Innovation**: Large-scale autoregressive pre-training
**Evolution**:
- GPT-1 (2018): 117M parameters
- GPT-2 (2019): 1.5B parameters
- GPT-3 (2020): 175B parameters
- GPT-4 (2023): Estimated >1T parameters

**Use Cases**: Text generation, completion, few-shot learning

### T5 (2019) - Unified Text-to-Text

**Architecture**: Encoder-decoder treating all tasks as text-to-text
**Key Innovation**: Unified framework for all NLP tasks
**Sizes**: T5-Small (60M) to T5-11B (11B)
**Use Cases**: Translation, summarization, classification (all as generation)

### Vision Transformer (ViT, 2020)

**Architecture**: Apply Transformer directly to image patches
**Key Innovation**: Treats image patches as sequence tokens
**Impact**: Demonstrated Transformers work beyond NLP
**Use Cases**: Image classification, object detection

### Other Notable Variants

- **RoBERTa**: BERT with better training (no NSP, larger batches)
- **ALBERT**: Parameter sharing for efficiency
- **XLNet**: Permutation language modeling
- **Longformer**: Efficient attention for long documents (sparse patterns)
- **Performer**: Linear attention complexity
- **Switch Transformer**: Sparse mixture of experts (1.6T parameters)

**Sources**: [R2][R3]

## Implementation Resources

### Official Libraries

**Hugging Face Transformers** [R3]:
```bash
pip install transformers
```

```python
from transformers import AutoModel, AutoTokenizer

# Load pre-trained model
model = AutoModel.from_pretrained("bert-base-uncased")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Tokenize and encode
inputs = tokenizer("Hello world!", return_tensors="pt")
outputs = model(**inputs)
```

**PyTorch Native**:
```python
import torch.nn as nn

# PyTorch provides built-in Transformer modules
transformer = nn.Transformer(
    d_model=512,
    nhead=8,
    num_encoder_layers=6,
    num_decoder_layers=6
)
```

### Learning Resources

**Official Tutorial**: [R2]
- Google Research blog provides excellent conceptual overview

**Hugging Face Course**: [R3]
- Comprehensive course on using Transformers library
- Covers fine-tuning, training from scratch, deployment

**Annotated Transformer**:
- Harvard NLP's line-by-line implementation guide
- http://nlp.seas.harvard.edu/annotated-transformer/

**Papers with Code**:
- Implementations and benchmarks
- https://paperswithcode.com/method/transformer

### Code Example - Complete Pipeline

```python
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
from datasets import load_dataset

# 1. Load dataset
dataset = load_dataset("imdb")

# 2. Load pre-trained model and tokenizer
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=2
)

# 3. Tokenize dataset
def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=512
    )

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# 4. Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

# 5. Create Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
)

# 6. Train
trainer.train()

# 7. Evaluate
metrics = trainer.evaluate()
print(metrics)

# 8. Inference
text = "This movie was fantastic!"
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)
prediction = torch.argmax(outputs.logits, dim=-1)
print(f"Sentiment: {'Positive' if prediction == 1 else 'Negative'}")
```

## Update Log

### 2025-11-02
- **Initial version**: Comprehensive documentation of Transformer architecture
- **Added**: Core concepts, three major patterns (encoder-decoder, encoder-only, decoder-only)
- **Included**: Self-attention mechanism, positional encoding, anti-patterns
- **Covered**: Major variants (BERT, GPT, T5, ViT), implementation examples
- **Sources**: [R1][R2][R3]

## See Also

### Prerequisites
- [Prompt Engineering](../engineering/prompt-engineering.md): How to effectively use Transformer-based LLMs
- [Context Engineering](../engineering/context-engineering.md): Managing context for optimal LLM performance

### Related Topics
- [Logic Tensor Networks](./tensor-logic.md): Combining neural networks with logical reasoning
- Attention Mechanisms: Foundation of Transformers
- Large Language Models: Applications of Transformer architecture

### Platform-Specific
- [OpenAI](../platforms/openai/): GPT models and APIs
- [Anthropic](../platforms/anthropic/): Claude models
- [Hugging Face](https://huggingface.co): Transformers library and model hub [R3]

## References

- [R1] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). "Attention Is All You Need." Advances in Neural Information Processing Systems, 30. arXiv:1706.03762. https://arxiv.org/abs/1706.03762 (accessed 2025-11-02)
- [R2] Google Research. "Transformer: A Novel Neural Network Architecture for Language Understanding." Google AI Blog. https://research.google/blog/transformer-a-novel-neural-network-architecture-for-language-understanding/ (accessed 2025-11-02)
- [R3] Hugging Face. "Transformers Documentation." Official documentation for the Transformers library. https://huggingface.co/docs/transformers/index (accessed 2025-11-02)

---

**Document ID**: `docs/research/transformer.md`
**Canonical URL**: `https://github.com/artificial-intelligence-first/ssot/blob/main/docs/research/transformer.md`
**License**: MIT
