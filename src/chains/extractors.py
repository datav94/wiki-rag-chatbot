#The question is the last entry of the history
def extract_question(input):
    return input[-1]["content"]

#The history is everything before the last question
def extract_history(input):
    return input[:-1]

#Formats the documents with newline after each doc
def format_context(docs):
    return "\n\n".join([d.page_content for d in docs])