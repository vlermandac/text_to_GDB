# text_to_GDB

## Architecture Idea

Main project divided in containerized apps.

### Data input
- Expected large list of big pdf files.
- DB server (Elastic Search docker image).
- Automatic text chunking based on a given limit (default: LLM token size limit).
- DB for embbeded text information (maybe a vector DB?).
- Patch the DB APIs if necessary.

### LLM app
- Elastic search calls.
- Semi-automated prompt selection.
- LLM information extraction.
- Output parsing.
- Transform output to triplet.
- Triplets embedding and insertion to DB.

### Input queries
- Only communicates with the vector DB.
- Vectorize received queries.
- Return top-k within vector DB.
- Use through API (fastAPI library).

### Front-end
- For the final user.
- Simple web app to make queries and visualize outputs.

## Roadmap
Still not in development.

### Short-term
- Knowledge Graph creation with the triplets.
- KG to graph database engine ?
- Queries answered with a combination of the stored embeddings and the KG.
- KG front-end visualization (n4j, or maybe a js library?).

### Mid-term
- Hallucination validation.
- Instructor integration to validate output.
- CI/CD (github actions).

### Long-term
- Run each app in a node within a single kubernetes cluster.
- Locally-run LLM (maybe would be useful to run it in a different cluster than the other apps).
- Ditch python.
