import os
import pickle
import time
import pandas as pd


def results_to_df(prompts_batch, data_samples, openai_client):

    df = pd.DataFrame(columns=['prompt', 'document', 'result'])

    for prompt_idx, prompt in enumerate(prompts_batch):

        assistant = openai_client.beta.assistants.create(
            name="Chilean History Expert",
            instructions=prompt,
            model="gpt-4"
        )

        for doc_idx, doc in enumerate(data_samples):
            thread = openai_client.beta.threads.create()
            print(f"new thread created with id: {thread.id}.")

            m = openai_client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=doc
            )
            print(f"new message created with id: {m.id}.")

            run = openai_client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant.id,
            )

            print(f"run instance created with id: {run.id}.")

            # wait while the assistant completes the answer
            run_status = ''
            while run_status != 'completed':
                print(f"run status: {run_status}.")
                run_status = openai_client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                ).status
                time.sleep(3)
            print(f"run status: {run_status}.")

            # assistant answer
            msg = openai_client.beta.threads.messages.list(
                thread_id=thread.id
            ).data[0].content[0].text.value

            # append row to df
            row = {'prompt' : prompt_idx, 'document' : doc_idx, 'result' : msg}
            df = pd.concat([df, pd.DataFrame.from_records([row])])
            print(f"Document {doc_idx} done.")

        print(f"Prompt {prompt_idx} done.")

    return df


def get_results(prompts_dir, results_dir, client):

    with open('../ssdh_all_raw_message', 'rb') as file:
        unpickled_object = pickle.load(file)

    documents = []
    for i in range(0, int(len(unpickled_object)/2)):
        documents.append(unpickled_object[2*i])

    documents_sample = []
    for i in [3, 5, 7, 11, 13]:
        documents_sample.append(documents[i])

    prompts = []
    for prompt in os.listdir(prompts_dir):
        with open(os.path.join(prompts_dir, prompt), 'r', encoding='utf-8') as file:
            prompts.append(file.read())

    df_results = results_to_df(prompts, documents_sample, client)
    df_results.to_csv('results.csv', index=False)

    file_name = "prompt_0_results.txt"
    f = open(f"{results_dir}/{file_name}", 'a')

    for i in range(5*8):
        prompt_num = int(i/5)
        if (prompt_num != int((i-1)/5)):
            f.close()
            file_name = f"prompt_{prompt_num}_results.txt"
            f = open(f"{results_dir}/{file_name}", 'a')
        print(f"\nDOCUMENT {(i % 5)}:\n", file=f)
        print(df_results['result'].array[i], file=f)
