from openai import AzureOpenAI
import azure.keyvault.secrets as azk
from azure.identity import DefaultAzureCredential
from models.data_models import Labels
from models.label_models import Label, Document


def get_key(keyname):
    vault_uri = 'https://keyvault-labeling.vault.azure.net/'
    client = azk.SecretClient(vault_uri, DefaultAzureCredential())
    secret = client.get_secret(keyname)
    key = secret.value
    return key


async def send_request(contents: str):
    key = get_key('openai-key')
    endpoint = 'https://labeling-llm-0.openai.azure.com/openai/deployments/gpt-4.1-nano/chat/completions?api-version=2025-01-01-preview'
    client = AzureOpenAI(
    azure_endpoint = endpoint,
    api_key=key,
    api_version="2024-12-01-preview"
    )
    completion = client.beta.chat.completions.parse(
        model="gpt-4.1-nano",
        messages=[
            {
                "role": "system",
                "content": """You are a Named Entity Recognition (NER) model used as an advanced ATS scanner.
                Your job is to extract words matching the specified entity types; job skill, Job title.
                Create a label even if there's a same word twice in different sections.
                If there is a section with skills listed, include all of them, since a recruiter would focus on that.
                if there are no words or phrases matching neither of the labels, return an empty list.
                Do not reformat or rephrase the text you find in the original document in any way, including capitalisation.
                """,
            },
            {
                "role": "user",
                "content": contents,
            }
        ],
        response_format=Labels,
        n=1,

    )
    
    message = completion.choices[0].message
    if (message.refusal):
        print(f'error in request:\n{message.refusal}\n\n{message}')
        print(contents)
        return 0
    else:
        labels = Labels.model_validate(message.parsed).model_dump()['Entities']
        return labels


def format_entities(doc_contents:str,labels_list:list,doc_id:int=0):
    doc = doc_contents
    entities = labels_list
    labeled_ents = []
    for entity in entities:
        content = entity['text']
        label = entity['type']
        if content not in doc_contents:
            continue
        else:
            start = doc_contents.find(content)
            end = start + len(content)
            labeled_ent = Label(start,end,label,content).to_dict()
            labeled_ents.append(labeled_ent)
    labeled_doc = Document(doc_id,doc_contents, labeled_ents).to_dict()
    return labeled_doc
    