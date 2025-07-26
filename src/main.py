import ingestion
from chat import chat, init_instructions


def embeddings_dump():
    prs = ingestion.preprocess()
    titles = ingestion.get_titles(prs)
    embeddings = ingestion.create_embeddings(titles)
    prs_with_embeddings = ingestion.attach_embeddings(prs, embeddings)
    for pr in prs_with_embeddings:
        ingestion.insert_data(pr)

def run():
    print('Welcome to Silo.')
    should_exit = False
    while not should_exit:
        prompt = input("> ")
        if prompt == "!exit":
            should_exit = True
        else:
            retrivals = ingestion.search_similar(query=prompt)
            instructions = init_instructions(retrivals)
            response = chat(prompt, instructions)
            print(response)



if __name__ == "__main__":
    run()
