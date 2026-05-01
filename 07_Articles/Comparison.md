# The Evolutionary LLM Timeline: BERT to GPT-3

*Comparing the architectures that defined the modern AI era.*

| Feature | BERT (Google, Oct 2018) | GPT-1 (OpenAI, Jun 2018) | GPT-2 (OpenAI, Feb 2019) | GPT-3 (OpenAI, May 2020) |
| :--- | :--- | :--- | :--- | :--- |
| **Architecture** | Encoder only | Decoder only | Decoder only | Decoder only |
| **Reads** | Bidirectionally (All at once) | Left to right only | Left to right only | Left to right only |
| **Pre-training Task** | MLM (Guess hidden word) + NSP (Guess next sentence) | Next word prediction | Next word prediction | Next word prediction |
| **Solves Polysemy?** | ✅ Yes (Looks left & right to understand context) | ⚠️ Partially (Only sees past words) | ⚠️ Better (Scale helps it guess context) | ✅ Yes (Massive context window clarifies meaning) |
| **Best Used For** | Understanding, classification, search, QA | Basic text generation | Zero-shot text generation | Few-shot reasoning, coding, translation, logic |
| **Real-World Used In** | Google Search, Gmail spam filter | N/A (Proof of concept only) | Copywriting tools, early chatbots | ChatGPT's direct predecessor (GPT-3.5) |
| **Parameters** | 110M (Base) / 340M (Large) | ~117M | 1.5 Billion | 175 Billion |
| **Dataset Size** | 3.3 Billion words (Books + Wiki) | ~5 Billion words (BookCorpus) | 40 GB (WebText from Reddit) | 570 GB (Filtered Common Crawl + Books) |
| **Context Window** | 512 tokens (~400 words) | 512 tokens (~400 words) | 1024 tokens (~800 words) | 2048 tokens (~1600 words) |
| **Fine-Tuning Strategy**| **Required.** Add task-specific output layers (e.g., a classification head) and train on labeled data. | **Required.** Add task-specific heads, but only train the final layer to save compute. | **Optional.** Showed you *could* skip it, but fine-tuning still yielded the absolute best results. | **Largely replaced** by Prompt Engineering (In-Context Learning). Why Fine-Tune when the prompt works? |
| **Key Innovation** | Proved that reading both left & right context creates unmatched reading comprehension. | Proved that a Decoder can be pre-trained generally and fine-tuned for specific tasks. | Proved that scale creates "emergent abilities"—it learned tasks it was never trained for. | Proved that "In-Context Learning" (learning from prompts) matches Fine-Tuning performance. |
| **Zero/Few-Shot Ability**| ❌ None. Will output gibberish if not fine-tuned for the specific task. | ❌ None. Relies entirely on fine-tuning for new tasks. | ✅ **Zero-Shot capable.** Can do tasks with zero examples just from the prompt formatting. | ✅✅ **Few-Shot master.** Give it 3 examples in the prompt, and it performs like a fine-tuned model. |
| **The "Elevator Pitch"**| "I am the ultimate Open-Book Exam student. I can find the exact answer hidden in your text." | "I am the basic foundation. I proved the Decoder architecture actually works." | "I am the accidental genius. I read the internet and learned skills no one taught me." | "I am the master improv actor. Show me 3 examples, and I will mimic any skill instantly." |
