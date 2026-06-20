# Meeting Summary — Introduction to LangChain: Standalone LLM Calls, Streaming & Multi-Model Pipelines
**Date:** June 14, 2026
**Meeting Started:** 7:59 AM
**Duration:** 159 minutes (scheduled) — **NOTE: This summary covers only the FIRST HALF of the session.** Sunitha's laptop ran out of charge partway through and the meeting/transcript was cut off mid-class (around the 2:39:00 mark, while Laxmi was beginning to explain chatbot memory management). A second half summary would be needed separately if the recording/transcript becomes available.
**Platform:** Microsoft Teams
**Instructor:** Laxmi Narayen (Applied Research Scientist, OpenStream.ai)

---

## Participants

Asha Ponraj, Devi Narayanan, Kamalam Jayaraman, Kannabiran G, Laxmi Narayen, Mohamed Arsh J, Muniappan Mohanraj, neelsvel1, Rajkannu, Ramesh Kandasamy, Sabarinathan J, Sathiyarajan Mariyappan, Shobana Samyayyah, Sri Ranjith, Srinivasan Mariappan, Sundar B, Sunitha Ramu, Suresh Soundararajan, Venkatesan Prahalanathan, Vijayarajan Packrisamy

---

## Session Overview (Covered So Far)

This was the introductory session to **LangChain**, building directly on the prompt engineering and DSPy work from previous weeks. The session covered:
1. Recap of the prompt-engineering hackathon leaderboard
2. Day's agenda: LangChain introduction → parallel calls → (time permitting) RAG with Wikipedia data
3. Standalone SDK calls to OpenAI, Anthropic, and Gemini — and why this approach is painful
4. Five core problems that motivate LangChain's existence
5. Introduction to LangChain as an open-source framework (GitHub stats, ecosystem)
6. LangChain's unified interface — `invoke`, `.content`, streaming
7. Using Ollama models (local) through LangChain
8. Streaming responses via LangChain (SSE explained)
9. Multi-LLM pipelines using LCEL (LangChain Expression Language)
10. Extensive Q&A — including several of Sunitha's own detailed questions
11. **Cut off** — Laxmi had just begun introducing chatbot memory/history management when the transcript ends

---

## Part 1 — Opening and Hackathon Recap (00:00 – 19:47)

### Hackathon Leaderboard Recap

Laxmi opened by acknowledging the prompt engineering hackathon (the Kaggle LLM Science Exam competition covered in earlier sessions):

> *"We had a hackathon and we have a lot of you guys give the submissions. So we have Naveen sir topping the leaderboard so far, with Nataraj and Ram closely following. Great job to everybody who gave it an attempt. But if you've not given it an attempt, please do give it a try."*

**Why the hackathon was introduced:**
> *"We understand that we have to cover a lot of mileage here and there, but we still had requests from people saying they still don't know how to make simple LLM calls and how to consume these prompts that we have just made via DSPy. So we had to introduce this, and I think this was really helpful in trying to consolidate whatever we have seen so far."*

### Today's Agenda

> *"Today we will be looking at, hopefully if time permits, we'll have like a two, two and a half hour session. So we will be looking at introduction to LangChain to start with. We will then move on to look at how to make parallel calls with LangChain. And then, looking at how time permits, we will also look at RAG — let's say we have Wikipedia data and how can we implement the RAG system in LangChain."*

**Note:** Given the session was cut off partway, RAG content (if covered later in the actual class) is **not** included in this summary, since the transcript only captures the first half.

---

## Part 2 — Environment Setup (19:47 – 24:39)

### Required Installations

> *"We are going to use anything and everything that's associated with LangChain, right? So we need LangChain, LLMs like OpenAI, Anthropic, Google AI, and so on. For the purpose of this tutorial, I'm going to use the DSPy environment that we've already utilized — it's just like something on top of it — then I'm going to use LangChain."*

```bash
pip install langchain
pip install openai anthropic google-generativeai
```

### API Key Management via .env

```python
# .env file structure:
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
```

```python
import os
from dotenv import load_dotenv

load_dotenv()
# Then print confirmation without exposing the key itself
```

**Why use .env files specifically:**
> *"First of all, putting API keys into your environment is not advisable, right? Because anybody can see it — if your agents can see it and so on. So it's better to [use] standard secret files that your agents are programmed to kind of skip, and .env files are one among them. If you want, you can also load it as a separate .py file, or save it as separate .txt files, config.txt, or any kind of config files."*

### Asha Ponraj's Request for Context

Partway through setup, Asha interrupted to ask for a primer:

> **Asha:** *"Lakshmi, sorry to interrupt — could you please give us a short intro on what is LangChain and what we use it for?"*

> **Laxmi:** *"Yeah, yeah, yeah, I haven't started into LangChain at all yet... when I start I will do that, just give me 15 minutes, I'll go there."*

(This context was delivered later — see Part 4 below.)

---

## Part 3 — Standalone LLM Calls: The Pain Points (24:39 – 53:56)

### What is an SDK?

> *"SDK here stands for a Software Development Kit, right? And this is a very detailed collection of shippable tools and shippable parts — moving parts from the software itself. Each provider has their own SDK, and each of these SDKs has to go through their own kind of authorization, and this will also involve their own response formats as well."*

### OpenAI SDK Example

```python
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain to me in simple words what neural networks are"}
    ]
)

openai_response = response.choices[0].message.content
print(openai_response)
```

**Key point on SDK is NOT open source:**

> **Laxmi:** *"Just tell me one thing — is this an open source library? Is this supposed to be an open source library?"*
> **Ramesh Kandasamy:** *"It is not open source, yeah."*
> **Laxmi:** *"Exactly right. So you cannot contribute... I have not seen anybody contributing to OpenAI because they have a closed system and a very strict [policy related] to contributing."*

**Note on SDK updates:**
> *"Every time there's an update to the SDK, and let's say the model goes deprecated, you are kind of forced to adapt your code to the new SDK guideline — which would also involve changing the models as well, because as we know currently GPT-3 [or] GPT-3.5 are no more available, just like Gemini 1.5 not being available for consumption."*

### Anthropic SDK Example

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-haiku-4-5",  # example model name used in class
    max_tokens=256,
    system="You are a helpful assistant.",
    messages=[
        {"role": "user", "content": "Explain in simple words to me what neural networks are"}
    ]
)

claude_answer = response.content[0].text
print(claude_answer)
```

**Key differences flagged:**
> *"This is required for Claude, whereas the other APIs did not prompt us for such explicit [max_tokens]... and then the system message in Claude can be sent via the system [parameter] itself instead of sending it as a JSON where we said the role is this, the role is this."*

### Gemini SDK Example

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        max_output_tokens=256,  # not mandatory in Gemini, unlike Anthropic
        system_instruction="You are a helpful assistant."
    ),
    contents="Explain to me in simple words what neural networks are"
)

gemini_answer = response.text
print(gemini_answer)
```

**Laxmi's framing of Gemini:**
> *"Gemini model is a little tangential, right? Because there you will have to use generate_content or the generative AI library — they are more focused on trying to have the Gen AI type libraries."*

### The Core Takeaway — Three Different Extraction Patterns

| Provider | How to extract the answer |
|----------|---------------------------|
| OpenAI | `response.choices[0].message.content` |
| Anthropic (Claude) | `response.content[0].text` |
| Gemini | `response.text` |

> *"The first problem is: same answer extracted in three different ways... If you want a single helper [function], first of all this involves a lot of code rewriting. So let's say I'm gonna define one helper function — `define extract_responses` — and then I'm gonna say if model == OpenAI, do this; if model == Claude, do this; else do this. And if it's gonna be Grok, it's gonna be totally different again."*

---

## Part 4 — The Five Problems That Motivate LangChain (53:56 – 53:56, consolidated)

Laxmi explicitly listed **five problems** with using raw SDKs directly:

1. **Lots of repetitive code** — you must write custom handling logic per SDK.
   > *"You will have to define software systems that [are] custom to each of these SDK types separately."*

2. **Multiple different authentications** — each provider has its own auth flow and key format.

3. **Conversation history / memory management differs completely per provider.**
   > *"For OpenAI I have to pass it as a JSON where I specify the role of the user, the role of the system... For Claude it's similar but different again, where system prompt has to be sent separately, the user message has to be sent separately... And then comes Gemini, which has to take all of this as config type system instructions and contents."*

4. **Rewiring a lot of code** if you want to switch providers.
   > *"Because ideally, as I have told you already, the industry doesn't use just one LLM for all the purposes."*

5. **Streaming is hard across multiple providers** — different streaming mechanisms per SDK.
   > *"Streaming when you are using a multi-API system or multi-SDK system in this space — it's hard."*

**Real-world example for why multi-LLM matters (Laxmi's academic research analogy):**
> *"One good example would be that I may use OpenAI as a content rater model and I may use Gemini as a content verifier and rephraser model. I may use Anthropic as the fact verifier model... So it's better to have three different checks yourself via different models."*

### The Natural Conclusion

> *"If you are already thinking of building something that kind of normalizes and regularizes these API usages across multiple system spaces and across multiple development kits itself — then you are already thinking of an idea like LangChain."*

---

## Part 5 — What is LangChain? (53:56 – 59:45)

### Definition

> *"LangChain is an open source framework... this is the agentic LangChain agentic engineering platform."*

**GitHub statistics shared:**
- **~3,930 active contributors**
- **~282,000 reported users**
- Current release: **LangChain Core 1.4.7**

### Connecting Back to GitHub Contribution Skills

> *"Whatever we saw in class — the pull, the merge, the fork, add and pull and merge — so the concept of GitHub contributions are quite the same. The concept of open source contribution that you guys practiced is quite the same here as well. So whatever we saw, we did not see for nothing. We did not waste our time. If you are really interested, you can go on to contribute to the LangChain GitHub — be part of the open source community of LangChain as well."*

### What Problem LangChain Solves

> *"While these LLMs are powerful on their own way, they are isolated — they don't know about your private data, they cannot access internet, and they are not updated with [recent] information. They don't remember past conversations until you explicitly pass them. LangChain can bridge this gap by chaining LLMs together with our external data. You can have RAG systems, you can create APIs, you can connect multiple LLMs together — all of this via a unified modular system."*

### LangChain Ecosystem Components

| Component | What it does |
|-----------|--------------|
| **LangGraph** | Builds agents that can handle multiple tasks across multiple frameworks |
| **Prompt Templates** | Pre-built prompt structures you can import instead of hardcoding prompts |
| **Chains** | A sequence of linked operations (e.g., format input → pass to LLM → get output → normalize) |
| **Memory management** | Handles conversation history automatically |
| **Agent management** | Manages autonomous agent behavior |
| **Vector stores / retrieval** | Supports RAG-style document retrieval |

> *"A chain is like a sequence of operations linked together, right? For example, let's say you have a user input, you would want to format it into a particular prompt, pass it into an LLM, then get the output, and send it in a normalized format. LangChain helps you do this — chaining is possible."*

### Why Use LangChain — Laxmi's Honest Take

> *"Usually why LangChain — that's the question that people answer in classes, and I wouldn't say the first use case is addition of real-time data or your company's data itself or RAG systems itself. I would say it's **rapid prototyping** — because multi-LLM involves, as we just saw, multiple approaches to make them accessible. LangChain lets us do that easily."*

---

## Part 6 — Q&A: When Should You Use LangChain? (59:45 – 01:04:10)

### Muniappan Mohanraj's Question — Single LLM Use Case

> **Muniappan:** *"Even though if we are using a single LLM, is it good to use LangChain, or if you use single LLM is LangChain not required?"*

> **Laxmi:** *"If you're using single LLM, I would then ask for what purpose. If you are using a single LLM for the purpose of, let's say, building some kind of augmented retrieval [RAG], then LangChain is extremely useful — because LangChain lets you handle memory management easily, and also retrieval from your particular document. But if you're just asking simple questions — like how we did yesterday, trying to invoke one LLM just to give answers for your test file — then that single LLM call is fine. But if you are doing a wrapper around one LLM or multiple LLMs into a bigger application, then I would suggest to go with LangChain."*

### SQL Database Example (Laxmi's Own Illustration)

> *"Let's say I am trying to query from a SQL database. Two ways to do it: one way is to pass the entire database content into an LLM and ask it to generate answers — not intuitive, because that's going to involve a lot of cost. But the other way is to have a SQL query generator. This way you compensate for hallucinations and stay only with respect to the answers in the dataset. LangChain already gives you the SQL query chain also as a development feature inside this toolkit itself."*

### Muniappan's Follow-up — Copilot Analogy

> **Muniappan:** *"In layman terms, if we can say in the VS Code Copilot, there are multiple agents configured, like Claude or GPT-5, and if we give 'auto' it automatically chooses the LLM based on our request — is the understanding correct?"*

> **Laxmi:** *"Yeah, but you don't have to let LangChain select it — it's like a normalized input-output framework, and you can use LangChain for management of input and output automatically. You don't have to let LangChain select it, but yes, your understanding is right."*

**Layman summary Laxmi gave:**
> *"In layman's terms, if you are building an application around an LLM, LangChain is a useful management framework. That's the layman term."*

---

## Part 7 — LangChain's Unified Interface (01:04:10 – 01:13:35)

### The Core Idea

> *"In layman's term, I see LangChain as one interface for everything — every LLM. LangChain wraps every provider behind the same interface. Using the same code, you can call different API providers."*

### The Three Universal Patterns

| LangChain Pattern | What it always does, regardless of provider |
|--------------------|----------------------------------------------|
| `model.invoke(question)` | Always returns an AI-generated message with `.content` string |
| `model.stream(question)` | Always yields stream chunks |
| `ChatPromptTemplate` | Provides templates that work across all models |
| `RunnableWithMessageHistory` | Manages conversation history automatically |

### Code — Calling Three Providers with the Same Interface

```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
# Gemini import similarly (langchain_google_genai)
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory

models = {
    "openai": ChatOpenAI(model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"]),
    "claude": ChatAnthropic(model="claude-haiku-4-5", api_key=os.environ["ANTHROPIC_API_KEY"]),
    "gemini": ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=os.environ["GEMINI_API_KEY"])
}

question = "Explain to me in simple words what neural networks are"

for model_name, model in models.items():
    response = model.invoke(question)
    print(model_name, response.content)
```

> *"You see how easy it is — the ease of consolidating multiple [calls]... is done easy via this `invoke`. This `invoke` always returns an AI message with `.content` string. Same format, no changes in format, every time."*

### Sathiyarajan's Question — LangChain vs Triton/PyTorch

> **Sathiyarajan:** *"What's the difference between OpenAI's return, PyTorch, and LangChain?"*

> **Laxmi:** *"LangChain is a matter of integrating all of it — it's an application orchestration framework. It's basically closer to the logic of writing itself... PyTorch is different — it's a compiler language by itself, it's not a framework. To tell you the exact difference: LangChain is close to the application interface itself, where you write application logic on top of an existing system like an LLM. But [Triton] is a language — it's kind of like a language where you write code that's close to a compiler for GPU kernels. It's close to CUDA C++ code. So these are totally two different things."*

*(Note: This directly echoes Sunitha's own earlier Python/PyTorch/Triton/LangChain question from a prior session — confirms the same framework vs. language distinction.)*

---

## Part 8 — Using Ollama (Local Models) with LangChain (01:17:35 – 01:34:12)

### Setup

```python
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llama_model = ChatOllama(model="llama3.2", temperature=0.5)
qwen_model = ChatOllama(model="qwen2.5:3b", temperature=0.5)  # example, with quantization mentioned
```

**On temperature:**
> *"Temperature is basically a way of you trying to say how creative you want the model to be... A good temperature will be anywhere between 0.5 to 0.66, and temperature can be set for any model — it has to be set, actually."*

### Usage — Same `.invoke()` Pattern

```python
response = llama_model.invoke("Explain to me in simple words what neural networks are")
print(response.content)
```

> *"One thing that you will have to just do is always use this LangChain `.invoke` type [pattern], right? So all you are going to do is `llama_model.invoke(...)` and then `.content`. It's extremely easy for us to just work with that."*

**Sunitha Ramu's question — separate handle for Ollama LLM:**

> **Sunitha:** *"Here ChatOllama is used, right? And is there an Ollama LLM also available, which is an alternate for this?"*

> **Laxmi:** *"What do you mean — Llama index? Yeah, you have separate chat handles also... I don't think there's a separate chat Llama. There's LlamaIndex I know inside [the ecosystem], but yeah, you can use it from `ChatOllama` itself."*

Laxmi confirmed: *"Any LLM that you see will always have a handle to be present"* — i.e., LangChain provides a consistent `Chat<Provider>` naming pattern (ChatOpenAI, ChatAnthropic, ChatOllama, etc.)

### Sunitha's Question — Why No System Prompt Used?

> **Sunitha:** *"In the original code, right — is there any reason why we haven't used the system prompt for LangChain?"*

> **Laxmi:** *"For the system prompt — yeah, I mean you can give system prompt as well, but since here it was not required and I just wanted to explain, I did not give it... When you use LangChain, one thing you'll have to be a little cautious about is that the system prompt is directly present from the chat prompt template — by default it takes the default system prompt. Suppose if you will have to pass a separate system prompt, then you will have to define it... by default you are a useful [assistant] — that will already be present."*

---

## Part 9 — Streaming with LangChain (01:34:26 – 01:40:01)

### Code — Streaming vs Non-Streaming

```python
question = "Explain to me in simple words what neural networks are"

# Non-streaming (invoke):
for provider_name, model in models.items():
    response = model.invoke(question)
    print(provider_name, response.content)

# Streaming:
for provider_name, model in models.items():
    print(provider_name)
    for chunk in model.stream(question):
        print(chunk.content)
```

> *"As you can see, we are just streaming the responses here, and the responses are quite fast, and it's also an integrated output system where you don't have to separately work with each of the streaming codes yourself. All you have to do is take the provider, say `model.stream`, and the chunk will be given one by one as you go."*

### Vijayarajan's Question — Streaming vs Non-Streaming, When to Use Which?

> **Vijayarajan:** *"What is the difference between stream and the other one [invoke], and when can we use it in real time?"*

> **Laxmi:** *"What is happening here is when I say stream, as soon as a particular set of strings or characters are being generated, the characters are sent out and displayed directly. So in non-streaming, what happens is the application sends a prompt to the model, the model generates the entire output response, bundles it into one single package — a bigger payload — and sends it back once everything is done generating. Streaming is that as soon as a model computes the very first token, or a set of chunks, it pushes it down to the open network. There's something called SSE — Server Sent Events — so it establishes a pipe, and via the pipe it keeps sending as it's generated."*

| | Non-Streaming | Streaming |
|--|---------------|-----------|
| Mechanism | Waits for full response, sends as one payload | Sends tokens/chunks as they're generated |
| Underlying tech | Standard HTTP request/response | SSE (Server Sent Events) — a persistent pipe |
| User experience | Wait, then see full text | See text appear progressively (like ChatGPT typing effect) |
| LangChain syntax | `model.invoke(question)` | `for chunk in model.stream(question)` |

---

## Part 10 — Technical Issues and PR/WhatsApp Sharing (01:40:01 – 01:48:50)

Microsoft Teams chat messages were failing to send for Laxmi throughout this segment — a recurring issue she mentioned was tied to Noordeen's absence:

> *"I'm not sure why my system is giving this... issue. Please bear with me. I think probably next week once Noordeen is back, this problem should not be there."*

**Workaround — sharing via WhatsApp instead of Teams:**

> *"Let me do one thing — let me push it to GitHub... Let me share it in WhatsApp. Again, the pull request has to be merged by Noordeen, right? Because some of you don't have access to WhatsApp on office laptops or something."*

Sathiyarajan Mariyappan volunteered to handle the merge coordination:
> *"Lakshmi, you share in the WhatsApp, I'll add the comment to the [PR]... I did the commit for the optimizers, right?"*

**Break announced:** Class broke until **10:10 AM IST** (per Asha Ponraj's confirmation in chat).

---

## Part 11 — Multi-LLM Pipelines via LCEL (LangChain Expression Language) (02:08:38 – onwards)

### Quick Recap Laxmi Gave Before This Section

> *"We started the class with looking at language model calls — how different language model calls are defined by different SDKs and companies. We went on to start with OpenAI, then Anthropic, then Gemini. We realized isolation of development results in different problems: overall terminology and input/output approach is different, different authentication, conversation memory management is a problem, we have to rewrite a lot of code, streaming is a problem. Then we looked at one interface for all — LangChain — which uses different APIs for OpenAI, Anthropic, Gemini, Grok, whatnot. Any LLM you see, there will be a contribution to incorporate it. We saw how all calls are easy with just `invoke` and `.content`. Then we saw streaming, the difference between streamable and non-streamable calls."*

### The New Concept — Two-Step Chain (Pipeline)

**Goal:** Use one LLM (OpenAI) to generate a topic, then pass that topic to a different LLM (Anthropic/Claude) to explain it — chaining two different providers together in one pipeline.

### Code

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# Step 1: Define the topic-generation prompt
generate_topic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Give me one interesting big topic to learn about {field}. Just the topic name, nothing else."),
    ("human", "{field}")
])

# Step 2: Define the topic-explanation prompt
explain_topic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Explain the topic in exactly two sentences for a beginner."),
    ("human", "{topic}")
])

# Step 3: Build the pipeline using LCEL (pipe operator |)
pipeline = (
    generate_topic_prompt
    | ChatOpenAI(model="gpt-4o-mini")
    | StrOutputParser()
    | (lambda x: {"topic": x})           # wrap output into a dict with key "topic"
    | explain_topic_prompt
    | ChatAnthropic(model="claude-haiku-4-5")
    | StrOutputParser()
)

result = pipeline.invoke({"field": "AI"})
print(result)
```

**Laxmi's explanation of the flow:**
> *"This is going to be the pipeline itself... First I'm going to take the generate_topic_prompt — that goes inside ChatOpenAI model using 4o-mini. The output is then taken by a string output parser. The topic will then be defined into a variable — I'll say `topic`. The variable `topic` then takes this current topic... So what we are then going to do is take this topic and send it inside the explain_topic_prompt, which will then be passed inside Claude (Anthropic), which is going to explain whatever the topic is about in exactly two sentences, like we asked for. And then we would have a string output parser. So this is like a pipeline — I've exactly defined the system to work like a pipe."*

### Sunitha Ramu's Detailed Clarifying Questions (Extended Exchange)

**Question 1 — Where is the field being passed?**

> **Sunitha:** *"Actually, generate_topic_prompt requires a field, right, to be passed along with it. Where are we defining it?"*
> **Laxmi:** *"Here, right? ...when I invoke it."*
> **Sunitha:** *"Then why are we using `lambda topic: topic` separately as topic = topic?"*
> **Laxmi:** *"Because then that topic has to be stored inside the variable `explain_topic` — I am putting it into a variable called `topic` so that lambda is just putting the value inside that variable. That's all, nothing much."*

**Question 2 — What is "pipeline" exactly?**

> **Sunitha:** *"So pipeline — is it something that we have to separately define, or is it [built into LangChain]?"*
> **Laxmi:** *"Pipeline is a part of this LCEL — LangChain Expression Language. It just says the data flows in the same order of the pipeline, starting from the first to the last."*

**Question 3 — How are we sure the lambda gets the topic value correctly?**

> **Sunitha:** *"So how are we assured that `lambda topic: topic` will get the topic value from the STR output parser? We are not giving topic explicitly — it should be extracted from the output, isn't it?"*
> **Laxmi:** *"That's why we use a parser — output parser. We assume that 4o-mini is just going to give me one output — one word or one topic output. That one topic output will be passed and saved as a string."*
> **Sunitha:** *"But did we tell it the output should be of this format?"*
> **Laxmi:** *"Yeah, we have — we said 'don't add any expression, just the topic name.' No description, nothing — just the topic name, nothing."*

### Shobana Samyayyah's Clarifying Question — Purpose of Pipeline

> **Shobana:** *"In the pipeline we are calling, we are using two variables — topic and field. Is this pipeline used to ask multiple questions to the model and get the response in a single output?"*

> **Laxmi:** *"No, ma'am, it's the other way around. This is used to pass a single input to multiple elements — instead of having multiple inputs to a single LLM, this is single input to multiple LLMs starting. This is the prompt you use to have a topic or a field that should go inside your prompt, and this will first generate a topic around that field, and that topic will then be explained by Anthropic [Claude]."*

> **Shobana (follow-up):** *"OK, so maybe the use case would be when I want to execute some task that involves multiple LLMs working in tandem with multiple tangible variables, then this pipeline will be extremely useful?"*

> **Laxmi:** *"Exactly... multiple LLMs have to work in tandem with multiple tangible variables, then this pipeline will be extremely useful."*

### Mohamed Arsh J's Confirmation

> **Mohamed Arsh J:** *"So it's basically like you're getting an output from one LLM and we are passing it to the other LLM — that's it, just for now?"*

> **Laxmi:** *"Correct, sir. Passing input to the first LLM, getting an output from the first LLM, passing that output as input to the second, and getting an output again."*

> **Mohamed Arsh J:** *"This is what we use — like one LLM we can use for content generation, another for image generation. This will be helpful in those kind of applications?"*

> **Laxmi:** *"Exactly, sir. Very well, sir."*

### Shobana's Question — Does LangChain Normalize the Output Format?

> **Shobana:** *"We saw before — how the individual model accepts the request and gives the response that differs. This STR output parser is able to adapt according to the model response and bring it into a common format — that's why it does that job, right?"*

> **Laxmi:** *"Correct, correct. So in other words, LangChain itself does the work of normalizing all the input and output to a LangChain-consumable format. Since everything resides inside LangChain itself, the [variability across providers] is well managed by LangChain itself."*

### Asha Ponraj's Question — Reliability Concerns

> **Asha:** *"Coming back to the question of topic — it's just an assumption, right? We are assuming that the model will give the correct answer. But in real time, is there a possibility that it goes wrong, and should we have a fallback?"*

> **Laxmi:** *"We will look at maybe this class or next class — having a fallback LLM call and other stuff. Suppose if it's not [following format]... but if you think about it, this is just going to be a string, a single string — it won't be multi-line for sure because we say 'don't give this to me' [in other formats]. Since this is a string and not just a word, we can get away with it."*

> **Asha:** *"So it is a simple example. Is there a way to debug everything — like a verbose/extended output?"*

> **Laxmi:** *"Yeah, definitely, definitely. You can have intermediate print statements or intermediate log statements, or define intermediate handlers to save also — we'll see that in the next [class]."*

### Devi Narayanan's Three-Part Question — Model Selection, Temperature, and Prompt Evaluation

> **Devi:** *"How do we actually determine which model has to do which task? Do we have any benchmark — like this model is good for evaluation, this model is good for paraphrasing, this model is good for SQL generation? And one more question on temperature — I see only for Ollama model we've given temperature. What other inputs can we give in this pipeline, and can we set our own temperature, top-K, top-P for other models as well?"*

> **Laxmi:** *"You can definitely use temperatures — temperature is a must-use actually for all the other models as well, please do give it. A good temperature would be anywhere between 0.5 to 0.66, and temperature can be set for any model — it has to be set, actually. For your first question — what model to use will not be known to us intuitively. For that, you'll have to read a lot of research papers. For example, in one study, researchers tried to evaluate which model does not have cultural bias, and they benchmarked it by specifically curating a dataset with cultural bias for interviews. People will then benchmark each model against multiple tasks. You'll have to read those papers and interpret — there's no shortcut, but otherwise, with experience [you build intuition]."*

> **Devi (follow-up):** *"Regarding the prompts — we are giving specific prompts for each task. How do we actually evaluate the prompt and improve them in the pipeline? Do we have any process for that?"*

> **Laxmi:** *"That's related to the evaluations that you write — just like how we saw in previous sessions [DSPy], you will have to do that step: have a train set, test set, and validate it."*

*(This directly ties LangChain prompt usage back to the DSPy evaluation methodology covered in earlier sessions.)*

### Shobana's Final Question in This Segment — Dev Time vs Runtime

> **Shobana:** *"This LangChain, whatever we are doing — this will be executed during the runtime, right? It's not like prompt engineering, what we saw before, during runtime?"*

> **Laxmi:** *"Exactly — if you mean by having runtime as production, yes, LangChain can be used in production systems as well. This can be used as final versions, yes."*

> **Shobana:** *"Because during development time I will write this code and see the accuracy, and the same thing will be deployed in production — every time when we are asking a model, this will be executed during runtime and fetch the answers, right? But the DSPy and all — we know what prompt has to be used, we'll be ready with the JSON..."*

> **Laxmi:** *"DSPy is to find us — DSPy is to tell us what prompt will be good for our data, and once we have such prompts, we can use those prompts inside LangChain."*

> **This is a key architectural insight: DSPy optimizes the prompt (development time); LangChain then deploys and orchestrates that optimized prompt across LLMs (runtime/production).**

---

## Part 12 — Debugging Pipelines with Lambda + Print (02:34:52 – End of Transcript)

Laxmi began demonstrating how to add intermediate debug statements inside an LCEL pipeline using a lambda function:

```python
pipeline = (
    generate_topic_prompt
    | ChatOpenAI(model="gpt-4o-mini")
    | StrOutputParser()
    | (lambda x: {"topic": x})
    | (lambda x: print(f"DEBUG OpenAI generated topic is: {x}") or x)  # debug step
    | explain_topic_prompt
    | ChatAnthropic(model="claude-haiku-4-5")
    | StrOutputParser()
)
```

> *"LCEL supports lambda, it should also support print. So here I am printing — let's say if you want to do how we write this, we usually follow a specific naming terminology... you say 'debug OpenAI' — let's see, generated topic is this — something like that."*

**Sunitha's request for clarification on this point:**
> **Sunitha:** *"Yeah, actually, I missed this — can you explain one second? I didn't follow."*
> **Laxmi:** *"Basically LangChain lets you write lambda functions, so if LCEL supports lambda, it should also support print. So a lambda function is an anonymous function — meaning you will have all of this saved inside a variable rather than having a function name. You'll say `lambda x: x` something like that."*

### Transition to Chatbot Memory (Where Transcript Cuts Off)

Laxmi began introducing the next topic — chatbot memory management — right as the transcript ends:

> *"One more thing I actually wanted to also say is the perspective of how you can consume LangChain for chatbots as well, right? So it's pretty intuitive and pretty simple as well... So what we will have to do is we will first have to set up a chatbot with memory — first let's do it WITHOUT history management, and then let's go to history management. So I'm defining a chat LLM that I would want to work with, and I'm of course going to use GPT-4o-mini. Then I am going to do a chat prompt template — I am saying 'You are a friendly tutor'..."*

**⚠️ This is where the transcript ends due to the laptop disconnection. The full chatbot memory/history management section (RunnableWithMessageHistory, InMemoryChatMessageHistory, etc.) was not captured.**

---

## Key Concepts — Quick Reference

| Concept | Definition |
|---------|-----------|
| SDK | Software Development Kit — provider-specific tools for accessing an LLM API, each with its own auth and response format |
| LangChain | Open-source framework providing a unified interface across LLM providers |
| LangGraph | Part of the LangChain ecosystem — builds multi-task agents across frameworks |
| Chain | A sequence of linked operations (prompt → LLM → output → next step) |
| LCEL | LangChain Expression Language — the `|` (pipe) syntax used to build pipelines |
| `model.invoke()` | Universal LangChain method — always returns AI message with `.content` |
| `model.stream()` | Universal LangChain method — yields response chunks as generated |
| SSE | Server Sent Events — the underlying mechanism enabling streaming responses |
| StrOutputParser | Extracts plain text/string from an LLM response in a normalized way |
| ChatPromptTemplate | LangChain's reusable prompt structure, supports system/human message roles |
| RunnableWithMessageHistory | LangChain feature for managing conversation history (introduced but not detailed before cutoff) |
| ChatOllama | LangChain's handle for local Ollama models |
| Temperature | Controls model creativity/randomness; recommended range 0.5–0.66 per Laxmi |
| .env file | Secure way to store API keys, automatically skipped by most agent/security scanners |

---

## Comparison Table — Raw SDK vs LangChain

| Aspect | Raw SDK (OpenAI/Anthropic/Gemini directly) | LangChain |
|--------|---------------------------------------------|-----------|
| Response extraction | Different per provider (`.choices[0].message.content` vs `.content[0].text` vs `.text`) | Always `.content` via `.invoke()` |
| Authentication | Different per provider | Still per-provider keys, but unified usage pattern |
| System prompt handling | Different (JSON role vs top-level param vs config) | Unified via ChatPromptTemplate |
| Streaming | Different mechanism per provider | Unified via `.stream()` |
| Switching providers | Requires rewriting code | Swap model object, same pipeline |
| Multi-LLM chaining | Manual glue code | Native via LCEL pipe operator |
| Best for | Simple, single-LLM, one-off calls | Rapid prototyping, multi-LLM apps, RAG, agents, production orchestration |

---

## Laxmi's Key Quotes from the Session

> *"LangChain wraps every provider behind the same interface."*

> *"DSPy is to find us — DSPy is to tell us what prompt will be good for our data, and once we have such prompts, we can use those prompts inside LangChain."*

> *"I wouldn't say the first use case [of LangChain] is addition of real-time data or RAG — I would say it's rapid prototyping."*

> *"Since everything resides inside LangChain itself, the [provider differences] are well managed by LangChain itself."*

> *"If you are already thinking of building something that normalizes these API usages across multiple development kits — then you are already thinking of an idea like LangChain."*

---

## Note on This Summary

Because the recording/transcript cuts off mid-class (around 2 hours 39 minutes into a scheduled 159-minute session) due to a laptop power failure, this summary reflects **only the first half** of the June 14 class. Topics Laxmi indicated would be covered later in the same session — full chatbot memory management with `RunnableWithMessageHistory`, and time-permitting, a RAG implementation using Wikipedia data — are **not captured** in this transcript and would need to be summarized separately if a recording or continuation transcript becomes available.

---

*Summary prepared from partial meeting transcript dated June 14, 2026 (first half only — session was cut short due to a device power failure).*
