### Transformer Architecture

***The class explained the Transformer architecture, with the "Monalisa of the AI" diagram with the Encoder and Decoder stack.***

```
Paper Used: Attention is All You Need
v1 - 2017
v7 - 2023
```

---

### Encoder Stack

1. **Input Raw data** is tokenized, Converted to vector & positional encoding is added to obtain the final embedding. This final embedding will be sent as an input to the Encoder Stack.
2. **Encoder** takes this input, runs self attention parallelly with 8 heads (multi head attention) [Will be explained below] and this gives a continuous representation. **Point to Note -** Self attention is performed as Softmax (Dot Product (Q.K / Sq.rt (Dimension) (dk)) x V.
3. This continuous representation is sent through an **Add & Norm layer**. Addition layer is placed to solve the vanishing gradient problem. This is by residual addition from the input vector.
    - The residual connection shortens the effective gradient path because it bypasses layers — so it's one mechanism solving one core problem.
5. **Normalization** performs a layer normalization, to ensure that the numbers are not off scale and are manageable.
6. The data from this **ADD & NORM layer** is then fed to the feed forward layer. This is done by expanding the embedding to a higher dimension from 512 to 2048 to ensure to capture all the patterns and then contracted again.This can be represented as **(512 → 2048 → 512)**.
7. The representation from Feed forward layer is then sent to the ADD & NORM layer once again and the final representation (**contextual representation**) is then available as the output from the Encoder.

```
- The Encoder stack isn't just one encoder — it's N encoders stacked
        - Typically 6 in the original "Attention Is All You Need" paper
- The output of one feeds into the next, progressively refining the representation.
```

---

### Decoder Understanding:

1. **The decoder** starts with the output embeddings (the words it has transformed so far). These are shifted one position to the right and the Positional encoding is then added to it.
2. This data then goes into **Masked Multi-Head attention block**. The masking ensures that when the model is predicting the word i, it sees the words that came before it (positions less than i) so that it does not "cheat" by reading the rest of the sentence. (*Multi head attention will be explained below*)
3. Just like the encoder, every sublayer in the decoder is immediately followed by an **Add & Layer Normalization** (*explained in the encoder stack*)
4. **Encoder Decoder Attention layer** - this is where the encoder output is taken as input by the decoder.
        - Queries (Q) = Come from the previous decoder layer
        - Keys (K) and Values (V) metrices come from the Encoder output.
        - This allows the decoder to attend to the entire sentence while it decides which word to write next.
5. After this, the data flows to another **Add & Norm** and then to the **Position wise feed forward network** and then another **Add & Norm layer**.
6. The decoder stack similar to encoder stack **happens 6 times** too and the final output coming out is passed through Linear transformation and the softmax function.
        - The softmax produces a probability distribution over the entire vocabulary. The model then picks the word with the highest probability or uses additional           strategies if it needs to pick multiple options. 

**Summary:** *The decoder uses what its written so far, masks the future, looks back at encoder's thinking to stay in the lane, processes it and uses the softmax ranking to pick the next word.*
