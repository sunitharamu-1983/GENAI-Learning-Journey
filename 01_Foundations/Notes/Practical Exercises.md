## Practical Exercises - Session 1

1. **Build a Simple RAG Chatbot:**  
   - *Step 1:* Choose a topic (e.g. company FAQs or a Wikipedia article). Copy some source text (a PDF or webpage) into a document.  
   - *Step 2:* Use an AI notebook or a library (like LlamaIndex/AI Kit) to **embed** that document into a vector database.  
   - *Step 3:* Write a query prompt for your AI (e.g. “Summarize the main points” or answer a question about the content). Instead of giving the full doc to the AI, let it retrieve relevant sections (the “augmented” step), then generate an answer.  
   - *Step 4:* Compare results with/without RAG grounding. Observe that grounding in the actual text reduces errors.  

2. **Prompt Engineering Practice:**  
   - *Step 1:* Think of a task (e.g. writing an email to request a meeting, or summarizing a technical concept). Write an initial prompt to a generative AI (like “Draft an email to my manager asking for X by Y date”).  
   - *Step 2:* Examine the output. Identify any issues (too long, not enough detail, wrong tone).  
   - *Step 3:* Refine your prompt by adding details or constraints (e.g. “Be concise, use professional tone, include bullet points for key dates”). Run it again.  
   - *Step 4:* Iterate until the output matches your needs. Note how prompt clarity and examples improve results.  

3. **Create an AI Workflow (Agent Prototype):**  
   - *Step 1:* Identify a multi-step task you do (e.g. booking travel: researching flights, checking hotels, and sending an itinerary email).  
   - *Step 2:* Outline how an AI agent could handle this: it would need tools (flight search API, hotel booking API, email API) and a plan (step-by-step actions).  
   - *Step 3:* In a notebook or pseudo-code, sketch how you’d call an LLM at each step. For example, first prompt: “Find the cheapest flights from NYC to Paris for June 15.” Then parse the answer, feed to next step (“Find a 4-star hotel in Paris from June 15-20”), etc.  
   - *Step 4:* Implement a basic version using function calls and an LLM. (For instance, use OpenAI’s “function calling” or LangChain to sequentially call APIs based on AI plan.) Observe how the agent uses reasoning and tools.
