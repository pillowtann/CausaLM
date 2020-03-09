from constants import POMS_GENDER_DATA_DIR, RANDOM_SEED
from gender_poms_datasets import create_gender_datasets
from datasets_utils import split_data, print_text_stats
from Timer import timer
import pandas as pd

LABELS = {'None': 0, 'anger': 1, 'fear': 2, 'joy': 3, 'sadness': 4}


@timer
def aggressive(df_female, df_male, biased_label, biasing_factor):
    df_biased = pd.DataFrame(columns=df_female.columns)
    for label in sorted(df_female["label"].unique()):
        df_label_f = df_female[df_female["label"] == label]
        df_label_m = df_male[df_male["label"] == label]
        if label == LABELS.get(biased_label, 0):
            df_biased = df_biased.append(df_label_f, ignore_index=True)
            df_sampled_m = df_label_m.sample(frac=biasing_factor, random_state=RANDOM_SEED)
            df_biased = df_biased.append(df_sampled_m, ignore_index=True)
        else:
            df_biased = df_biased.append(df_label_m, ignore_index=True)
            df_sampled_f = df_label_f.sample(frac=biasing_factor, random_state=RANDOM_SEED)
            df_biased = df_biased.append(df_sampled_f, ignore_index=True)
    return df_biased


@timer
def gentle(df_female, df_male, biased_label, biasing_factor):
    df_biased = pd.DataFrame(columns=df_female.columns)
    for label in sorted(df_female["label"].unique()):
        df_label_f = df_female[df_female["label"] == label]
        df_label_m = df_male[df_male["label"] == label]
        if label == LABELS.get(biased_label, 0):
            df_biased = df_biased.append(df_label_f, ignore_index=True)
            df_sampled_m = df_label_m.sample(frac=biasing_factor, random_state=RANDOM_SEED)
            df_biased = df_biased.append(df_sampled_m, ignore_index=True)
        else:
            df_biased = df_biased.append(df_label_f, ignore_index=True)
            df_biased = df_biased.append(df_label_m, ignore_index=True)
    return df_biased


# @timer
# def aggressive(df_female, df_male, biased_label, biasing_factor):
#     # def biasing_condition(i, b, label, biased_label):
#     #     if label == biased_label:
#     #         return i % b == 0
#     #     else:
#     #         return i % b != 0
#     df_biased = pd.DataFrame(columns=df_female.columns)
#     b = (1 - biasing_factor) * 10
#     for label in tqdm(sorted(df_female["label"].unique()), desc="label"):
#         df_label_f = df_female[df_female["label"] == label]
#         df_label_m = df_male[df_male["label"] == label]
#         for i, row in enumerate(tqdm(df_label_f.itertuples(), total=len(df_label_f), desc="num_samples")):
#             if not(bool(i % b == 0) ^ bool(label == biased_label)):
#                 new_row = {
#                     "ID_f": int(row.ID_m),
#                     "ID_cf": int(row.ID_f),
#                     "Person_f": str(row.Person_m),
#                     "Person_cf": str(row.Person_f),
#                     "Sentence_f": str(row.Sentence_m),
#                     "Sentence_cf": str(row.Sentence_f),
#                     "Template": str(row.Template),
#                     "Race": str(row.Race),
#                     "Emotion_word": str(row.Emotion_word),
#                     "label": int(label)
#                 }
#             else:
#                 new_row = {
#                     "ID_f": int(row.ID_f),
#                     "ID_cf": int(row.ID_m),
#                     "Person_f": str(row.Person_f),
#                     "Person_cf": str(row.Person_m),
#                     "Sentence_f": str(row.Sentence_f),
#                     "Sentence_cf": str(row.Sentence_m),
#                     "Template": str(row.Template),
#                     "Race": str(row.Race),
#                     "Emotion_word": str(row.Emotion_word),
#                     "label": int(label)
#                 }
#             df_biased = df_biased.append(new_row, ignore_index=True)
#     return df_biased


@timer
def create_biased_gender_datasets(df_female, df_male, biased_label, biasing_factor, biasing_method):
    df_biased = biasing_method(df_female, df_male, biased_label, biasing_factor)
    df_biased = df_biased.set_index(keys=["ID_F", "ID_CF"]).sort_index()
    print(df_biased)
    print_text_stats(df_biased, "Sentence_F")
    split_data(df_biased, POMS_GENDER_DATA_DIR, f"gender_biased_{biased_label}_{biasing_method.__name__}")


if __name__ == "__main__":
    _, df_female, df_male = create_gender_datasets()
    create_biased_gender_datasets(df_female, df_male, "joy", 0.1, aggressive)
    create_biased_gender_datasets(df_female, df_male, "joy", 0.1, gentle)
