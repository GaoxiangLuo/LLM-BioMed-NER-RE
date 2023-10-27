import re
import pandas as pd
from typing import Tuple, List
from ner_metrics import classifcation_report

hex_name_map = {
    "#FF0000": "Form",
    "#FFA500": "Route",
    "#FFFF00": "Frequency",
    "#00FF00": "Dosage",
    "#0000FF": "Strength",
    "#800080": "Duration",
    "#FFC0CB": "Reason",
    "#964B00": "Ade",
    "#808080": "Drug"
}
hex_ner_map = {
    "#FF0000": [],
    "#FFA500": [],
    "#FFFF00": [],
    "#00FF00": [],
    "#0000FF": [],
    "#800080": [],
    "#FFC0CB": [],
    "#964B00": [],
    "#808080": []
}

label2digit = {
    'No relation': 0,
    'STRENGTH-DRUG': 1,
    'ROUTE-DRUG': 2,
    'FREQUENCY-DRUG': 3,
    'FORM-DRUG': 4,
    'DOSAGE-DRUG': 5,
    'REASON-DRUG': 6,
    'DURATION-DRUG': 7,
    'ADE-DRUG': 8
}
def get_digit(x):
    if x not in label2digit:
        return 0
    return label2digit[x]

def html_parsing_ncbi(df: pd.DataFrame, col_name: str) -> Tuple[List[str], List[str]]:
    """
    Parse the html output to the format of the ground truth labels for the NCBI dataset.
    Args:
        df: the dataframe containing the input text and the ground truth labels
        col_name: the column name of the html output from GPT-3.5 or GPT-4
    Returns:
        gt_labels_list: a list of ground truth labels
        pred_labels_list: a list of predicted labels
    """
    gt_labels_list = []
    pred_labels_list = []
    for i in range(len(df)):
        input_text_tokens = df.iloc[i]['text'].split(sep=' ')
        gt_labels = df.iloc[i]['labels'].split(sep=' ')
        assert len(input_text_tokens) == len(gt_labels)

        # initialize the predicted labels
        pred_labels = ['O'] * len(gt_labels)
        name_entities_list = []
        llm_html_output = df.iloc[i][col_name]
        for m in re.finditer('<span style="background-color: #FFFF00">', llm_html_output):
            start = m.end()
            end = llm_html_output.find('</span>', start)
            phrase = llm_html_output[start:end]

            # put a space before and after '(', ')' and '-' if there aren't any
            phrase = re.sub(r'(?<=[^\s])\(', ' (', phrase)
            phrase = re.sub(r'\((?=[^\s])', '( ', phrase)
            phrase = re.sub(r'(?<=[^\s])\)', ' )', phrase)
            phrase = re.sub(r'\)(?=[^\s])', ') ', phrase)
            phrase = re.sub(r'(?<=[^\s])\-', ' -', phrase)
            phrase = re.sub(r'\-(?=[^\s])', '- ', phrase)

            # tokenize the phrase using space
            phrase_tokens = phrase.split(sep=' ')
            name_entities_list.append(phrase_tokens)

        # check if the found name entiries are in the input text
        last_index = 0
        for ner in name_entities_list:
            # check if ner is a sub-list of input_text_tokens
            for j in range(last_index, len(input_text_tokens), 1):
                if input_text_tokens[j:j+len(ner)] == ner:

                    pred_labels[j] = 'B'
                    for k in range(j+1, j+len(ner)):
                        pred_labels[k] = 'I'

                    last_index = j+len(ner)
                    break

        gt_labels_list.append(gt_labels)
        pred_labels_list.append(pred_labels)
    return gt_labels_list, pred_labels_list

def get_name_entity(html_output, hex_code):
    """
    Args:
        html_output: the html output from GPT-3.5 or GPT-4
        hex_code: the hex code of the color used to highlight the name entity
    Returns:
        name_entities_list: a list of name entities
    """
    name_entities_list = []
    for m in re.finditer(f'<span style="background-color: {hex_code}">', html_output):
        start = m.end()
        end = html_output.find('</span>', start)
        phrase = html_output[start:end]

        # put a space before and after '(', ')' and '-' if there aren't any
        phrase = re.sub(r'(?<=[^\s])\(', ' (', phrase)
        phrase = re.sub(r'\((?=[^\s])', '( ', phrase)
        phrase = re.sub(r'(?<=[^\s])\)', ' )', phrase)
        phrase = re.sub(r'\)(?=[^\s])', ') ', phrase)
        phrase = re.sub(r'(?<=[^\s])\-', ' -', phrase)
        phrase = re.sub(r'\-(?=[^\s])', '- ', phrase)

        # tokenize the phrase using space
        phrase_tokens = phrase.split(sep=' ')
        name_entities_list.append(phrase_tokens)
    return name_entities_list

def check_name_entity(hex_code, name_entities_list, pred_labels, input_text_tokens):
    """
    Args:
        hex_code: the hex code of the color used to highlight the name entity
        name_entities_list: a list of name entities
        pred_labels: a list of predicted labels (edited in-place)
        input_text_tokens: a list of tokens in the input text
    """
    last_index = 0
    for ner in name_entities_list:
        for j in range(last_index, len(input_text_tokens), 1):
            if input_text_tokens[j:j+len(ner)] == ner:

                pred_labels[j] = f'B-{hex_name_map[hex_code]}'
                for k in range(j+1, j+len(ner)):
                    pred_labels[k] = f'I-{hex_name_map[hex_code]}'

                last_index = j+len(ner)
                break

def html_parsing_n2c2(df: pd.DataFrame, col_name: str) -> Tuple[List[str], List[str]]:
    """
    Parse the html output to the format of the ground truth labels for n2c2 dataset.
    Args:
        df: the dataframe containing the input text and the ground truth labels
        col_name: the column name of the html output from GPT-3.5 or GPT-4
    Returns:
        gt_labels_list: a list of ground truth labels
        pred_labels_list: a list of predicted labels
    """
    gt_labels_list = []
    pred_labels_list = []
    for i in range(len(df)):
        input_text_tokens = df.iloc[i]['text'].split(sep=' ')
        # gt labels
        gt_labels = df.iloc[i]['labels'].split(sep=' ')
        assert len(input_text_tokens) == len(gt_labels)

        pred_labels = ['O'] * len(gt_labels)

        # extract the content between '<span style="background-color: #XXXXXX">' and '</span>'
        llm_html_output = df.iloc[i][col_name]

        for k, v in hex_ner_map.items():
            hex_ner_map[k] = get_name_entity(llm_html_output, k)

        # check if the found name entiries are in the input text
        for k, v in hex_ner_map.items():
            check_name_entity(k, v, pred_labels, input_text_tokens)

        gt_labels_list.append(gt_labels)
        pred_labels_list.append(pred_labels)
    return gt_labels_list, pred_labels_list

def get_classification_report(df: pd.DataFrame, col_name1: str, col_name2: str, mode: str = "lenient"):
    """
        Get classification report given two columns of labels.
        Args:
            df: a DataFrame
            col_name1: column name of ground truth labels
            col_name2: column name of predicted labels
            mode: strict or lenient
        Returns:
            a classification report
    """
    y_true = df[col_name1].tolist()
    y_true = [item for sublist in y_true for item in sublist]
    y_pred = df[col_name2].tolist()
    y_pred = [item for sublist in y_pred for item in sublist]
    assert len(y_true) == len(y_pred)
    
    return classifcation_report(tags_true=y_true, tags_pred=y_pred, mode=mode)