# LLM-BioMed-NER-RE


This repository contains the LLM evaluation code for the npj Digital Medicine paper "*An In-Depth Evaluation of Federated Learning on Biomedical Natural Language Processing for Information Extraction*". The datasets used in this paper were downloaded from [[FedNLP Repo]](https://github.com/PL97/FedNLP). In particular, they are *NCBI-Disease*, *2018 n2c2* datasets for named entity recognition (NER); *GAD* and *2018 n2c2* for relation extraction (RE). 

**Table 1:** The results of LLMs with the best among 1/5/10/20-shot prompting on NER and RE tasks, compared with Blue BERT and GPT 2 trained with federated learning. 

<table>
    <tr>
        <td style="border-bottom: 1px solid black; text-align:center" rowspan="3">Model</td>
        <th style="text-align:center" colspan="4">NER</th>
        <th style="text-align:center" colspan="2">RE</th>
    </tr>
    <tr>
        <th style="text-align:center" colspan="2">NCBI</th>
        <th style="text-align:center" colspan="2">2018 n2c2</th>
        <th style="text-align:center">2018 n2c2</th>
        <th style="text-align:center">GAD</th>
    </tr>
    <tr>
        <td style="border-bottom: 1px solid black; text-align:center">Strict</td>
        <td style="border-bottom: 1px solid black; text-align:center">Lenient</td>
        <td style="border-bottom: 1px solid black; text-align:center">Strict</td>
        <td style="border-bottom: 1px solid black; text-align:center">Lenient</td>
        <th style="border-bottom: 1px solid black; text-align:center" colspan="2">F1</th>
    </tr>
    <tr>
        <td>GPT 3.5</td>
        <td>0.575</td>
        <td>0.719</td>
        <td>0.565</td>
        <td>0.705</td>
        <td>0.290</td>
        <td>0.485</td>
    </tr>
    <tr>
        <td>GPT 4</td>
        <td>0.722</td>
        <td>0.834</td>
        <td>0.616</td>
        <td>0.751</td>
        <td>0.882</td>
        <td>0.543</td>
    </tr>
    <tr>
        <td>PaLM 2 Bison</td>
        <td>0.640</td>
        <td>0.756</td>
        <td>0.544</td>
        <td>0.653</td>
        <td>0.407</td>
        <td>0.468</td>
    </tr>
    <tr>
        <td>PaLM 2 Unicorn</td>
        <td>0.726</td>
        <td>0.848</td>
        <td>0.621</td>
        <td>0.749</td>
        <td style="text-decoration: underline;">0.888</td>
        <td>0.549</td>
    </tr>
    <tr>
        <td>Gemini 1.0 Pro</td>
        <td>0.654</td>
        <td>0.779</td>
        <td>0.566</td>
        <td>0.694</td>
        <td>0.411</td>
        <td>0.541</td>
    </tr>
    <tr>
        <td style="border-bottom: 1px solid black;">Claude 3 Opus</td>
        <td style="border-bottom: 1px solid black; text-decoration: underline">0.788</td>
        <td style="border-bottom: 1px solid black; text-decoration: underline">0.879</td>
        <td style="border-bottom: 1px solid black; text-decoration: underline">0.680</td>
        <td style="border-bottom: 1px solid black; text-decoration: underline">0.787</td>
        <td style="border-bottom: 1px solid black;">0.832</td>
        <td style="border-bottom: 1px solid black; text-decoration: underline;">0.569</td>
    </tr>
    <tr>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>Blue BERT (FL)</td>
        <td><b>0.824</b></td>
        <td><b>0.899</b></td>
        <td><b>0.954</b></td>
        <td><b>0.986</b></td>
        <td><b>0.950</b></td>
        <td>0.714</td>
    </tr>
    <tr>
        <td>GPT 2 (FL)</td>
        <td>0.784</td>
        <td>0.840</td>
        <td>0.830</td>
        <td>0.868</td>
        <td>0.946</td>
        <td><b>0.721</b></td>
    </tr>
</table>


## Data
More details of the datasets can be found in [`data`](data).

## Models
| **Model** | **RLHF-Tuned** | **Instruction-Tuned**| **Max Input Tokens** | 
| :--- | :---: | :---: | :---: |
| GPT 3.5 (Chat) | Yes | No |16K |
| GPT 4 (Chat) | Yes | No |128K |
| PaLM 2 Bison (Chat) | No | No |8K |
| PaLM 2 Unicorn (Text) | No | No| 8K |
| Gemini Pro (Chat) | No | No |32K |
| Claude 3 (Chat) | Yes | No | 200K |

The models used in this paper are mostly chat models and a text-completion model without specifically tuning for NER and RE tasks. We applied in-context learning by providing examples as prompts to the models. Even with 20-shot prompting, the input tokens length is still within 8K, which all models can handle in its context window. 

The example notebooks are in the root folder.