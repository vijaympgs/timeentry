__Agent Rule to Prevent Context‑Length Errors__

1. __Pre‑check token count__ – Before constructing a prompt, estimate the total token usage (system messages + user input + expected output). If it exceeds the model’s limit, apply mitigation steps.

2. __Chunking__ – Split large inputs into smaller, self‑contained the token budget. Process each chunk separately and later combine the results (e.g., concatenate summaries or aggregate extracted data).

3. __Hierarchical Summarisation__ –\
   a. Summarise each chunk individually.\
   b. Feed the collection of summaries into a second pass to produce a final answer. This reduces the overall token count while preserving essential information.

4. __Retrieval‑Augmented Generation (RAG)__ – Index the full document (or codebase) in a vector store or simple keyword index. At query time, retrieve only the most relevant fragments (top‑k) and include those in the prompt instead of the whole input.

5. __Sliding‑Window / Overlapping Windows__ – For tasks requiring continuity, move a fixed‑size window across the text with a small overlap, generate partial results for each window, then merge them.

6. __Checkpoint / Stateful Processing__ – Store intermediate state (e.g., partial answers, extracted entities) externally (file, DB, in‑memory). In the next request, load the saved state and continue processing the next chunk, effectively “rolling back” to a known checkpoint.

7. __Use a Larger‑Context Model__ – When available, switch to a model with a bigger context window (e.g., GPT‑4‑32k, GPT‑4‑128k, Claude‑3‑100k) to reduce the need for aggressive chunking.

8. __Prompt Optimisation__ – Remove unnecessary system messages, compress repetitive text, use concise variable names, and avoid sending large static sections (e.g., full libraries) when they are not needed for the current query.

9. __External Memory / Long‑Term Storage__ – Persist large data outside the prompt (database, file system, vector DB). Query only the needed snippet at runtime, keeping the prompt size small.

10. __Streaming / Incremental Inference__ – If the execution environment supports it, feed the model incrementally while streaming token generation, avoiding a static token‑limit breach.

__Implementation Checklist for the Agent__

- ☐ Estimate token usage before each model call.
- ☐ If > 90 % of the limit, apply __Chunking__ or __RAG__.
- ☐ Summarise chunks before a final aggregation step.
- ☐ Store intermediate results for later reuse (checkpoint).
- ☐ Prefer a larger‑context model when the workload consistently exceeds limits.
- ☐ Keep prompts minimal and focused; prune unnecessary context.

Following this rule set will keep the agent’s inputs within the model’s context window and prevent the “input is longer than the model's context length” error.
