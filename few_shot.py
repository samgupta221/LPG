import pandas as pd
import json


class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)

        self.df = pd.json_normalize(posts)

        # FIX 1: ensure no missing values break logic
        self.df["tags"] = self.df["tags"].apply(lambda x: x if isinstance(x, list) else [])

        # FIX 2: correct length column
        self.df["length"] = self.df["line_count"].apply(self.categorize_length)

        # FIX 3: safer flattening of tags
        all_tags = []
        self.df["tags"].apply(lambda x: all_tags.extend(x))

        self.unique_tags = sorted(list(set(all_tags)))

    def get_filtered_posts(self, length, language, tag):
        df_filtered = self.df[
            (self.df["tags"].apply(lambda tags: tag in tags)) &
            (self.df["language"] == language) &
            (self.df["length"] == length)
        ]

        return df_filtered.to_dict(orient="records")

    def categorize_length(self, line_count):
        try:
            line_count = int(line_count)
        except:
            return "Short"

        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        return self.unique_tags


if __name__ == "__main__":
    fs = FewShotPosts()

    print(fs.get_tags())

    posts = fs.get_filtered_posts("Medium", "Hinglish", "Job Search")
    print(posts)