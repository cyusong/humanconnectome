#@markdown Run this cell to load in get_papers(search_term) function
from Bio import Entrez

import os
import openai
import json

path = 'D:/GPT_annotator_Melissa/'

# Enter your email address for Entrez authentication
Entrez.email = "mutwil@gmail.com"
openai.api_key = "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"

prompt = '''
Write a very short summary about the functions of genes in this abstract. The summary must show pair-wise relationships, for example:
gene: !affects! Process
gene: !localizes to! X
gene: !interacts with! Y
gene: !enhances! Z
gene: !represses! U
gene: !synthesizes! I

Please provide only one statement per line, and ensure that each line contains exactly two actors. If a relationship involves more than two actors, please break it down into multiple separate lines.

<ENTER PROMPT HERE>

VERY SHORT, CONCISE SUMMARY CONTAINING ALL INFORMATION WITH TWO ACTORS PER LINE: 

'''



def gpt_analyzer(abstract):
    print('Abstract:',  abstract)
    my_prompt = prompt.replace('<ENTER PROMPT HERE>',abstract)

    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=my_prompt,
      temperature=0,
      max_tokens=256,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=1
    )
    print(response['choices'][0]['text']+'\n')

    return response['choices'][0]['text']


def search_and_fetch_journal_papers(search_term, email, year_cutoff, retmax=10000):
    Entrez.email = email
    query = f'{search_term} AND "{year_cutoff}/01/01"[Date - Publication] : "3000"[Date - Publication]'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax=retmax,
                            term=query,
                            usehistory='y')
    results = Entrez.read(handle)
    handle.close()

    pmid_list = results['IdList']

    handle = Entrez.efetch(db='pubmed', id=','.join(pmid_list), retmode='xml')
    papers = Entrez.read(handle)['PubmedArticle']
    handle.close()

    paper_details = []

    for paper in papers:
        pmid = paper['MedlineCitation']['PMID']
        title = str(paper['MedlineCitation']['Article']['ArticleTitle'])
        abstract = paper['MedlineCitation']['Article'].get('Abstract', {}).get('AbstractText', None)
        abstract = ' '.join([str(abst) for abst in abstract]) if abstract is not None else ''
        date = paper['MedlineCitation']['Article']['ArticleDate'][0] if paper['MedlineCitation']['Article'].get('ArticleDate') else paper['MedlineCitation']['DateRevised']
        journal = str(paper['MedlineCitation']['Article']['Journal']['Title'])
        doi = paper['PubmedData']['ArticleIdList'][-1] if paper['PubmedData'].get('ArticleIdList') else None
        doi = str(doi) if doi is not None else None
        author_list = paper['MedlineCitation']['Article'].get('AuthorList', [])
        authors = [f"{author.get('LastName', '')} {author.get('ForeName', '')}" for author in author_list if author.get('LastName')]

        paper_info = {
            'pmid': pmid,
            'date': f"{date['Year']}-{date['Month']}-{date['Day']}",
            'journal': journal,
            'title': title,
            'abstract': abstract,
            'doi': doi,
            'authors': authors
        }

        paper_details.append(paper_info)

    return paper_details

search_term = "Chromatin interactions OR HiC OR HiChIP OR ChIA-PET and homo sapiens"
year_cutoff = 2010

papers = search_and_fetch_journal_papers(search_term, "mutwil@gmail.com", year_cutoff)

counter = 0
for i in papers:
    print(i['abstract'], str(i['pmid']))
    pubmed, abstract = str(i['pmid']), i['abstract']
    if pubmed+'.txt' not in os.listdir(path+'/annotations'):
        result = gpt_analyzer(abstract)
        try:
            v = open(path+'/annotations/%s.txt' % pubmed,'w')
            v.write(str(abstract)+'\n\n'+str(result))
            v.close()
        except:
            print('failed writing', i)
    else:
        print(i, 'already done')
    counter +=1
    print(counter, 'out of', len(papers))


