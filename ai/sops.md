# AI Engineering - Standard Operating Procedures

### SOP-01 - Ship a model or prompt change

1. Build the change
2. Run the full evaluation suite
3. Compare against production
4. Get evaluation gate approval
5. Version and record a model card
6. Deploy with rollback ready

### SOP-02 - Add a grounding source

1. Validate source quality and license
2. Index it for retrieval
3. Verify retrieval returns source, confidence, and timestamp
4. Re-run retrieval-quality evals
