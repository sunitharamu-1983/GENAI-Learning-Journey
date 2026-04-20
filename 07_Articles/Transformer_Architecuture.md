### Transformer Architecture

***The class explained the Transformer architecture, with the "Monalisa of the AI" diagram with the Encoder and Decoder stack.***

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
- The Encoder stack isn't just one encoder — it's N encoders stacked (typically 6 in the original "Attention Is All You Need" paper).
- The output of one feeds into the next, progressively refining the representation.
```
