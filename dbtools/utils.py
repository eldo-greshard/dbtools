from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

# Load Sentence Transformer Model (Optimized for Small Size)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Mapping of CLI commands to descriptions
COMMAND_DESCRIPTIONS = {
    "auto_export_compare_table": "Export differences between tables as CSV.",
    "compare_db": "Compare two databases and find differences.",
    "compare_selected_table": "Compare a specific table between databases.",
    "dump_table": "Dump table data to a file.",
    "bulk_import": "Import missing data from CSV into the database.",
    "single_table_import": "Import a single table into the database.",
    "single_table_import_wfilter": "Import a single table with a filter applied.",
    "execute_dump_script": "Execute SQL dump scripts on a database."
}

# Convert descriptions to embeddings
COMMAND_EMBEDDINGS = {cmd: model.encode(desc) for cmd, desc in COMMAND_DESCRIPTIONS.items()}

def find_best_command(user_input):
    """Find the closest matching command using embeddings"""
    user_embedding = model.encode(user_input)
    
    best_match = None
    best_score = float("inf")  # Lower score is better (cosine similarity)
    
    for command, embedding in COMMAND_EMBEDDINGS.items():
        score = cosine(user_embedding, embedding)
        if score < best_score:
            best_score = score
            best_match = command
    
    return best_match if best_score < 0.5 else None  # Use 0.5 as threshold for accuracy
