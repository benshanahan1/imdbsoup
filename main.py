import argparse
import bs4
import re
import requests


class ImdbUrl:
    NAME = "https://www.imdb.com/name/{id}/"
    TITLE = "https://www.imdb.com/title/{id}/"

    @classmethod
    def get_by_name_id(self, name_id):
        return self.NAME.format(id=name_id)

    @classmethod
    def get_by_title_id(self, title_id):
        return self.TITLE.format(id=title_id)


class Person:
    def __init__(self, url):
        # Parse the IMDb URL
        self.soup = self.get_by_url(url)

        # Parse details from HTML soup object
        self.name = self._parse_name()
        self.credits = self._parse_credits()
        self.total_credits = sum([x["n_credits"] for x in self.credits.values()])

    def __repr__(self):
        return f"<IMDb entry: {self.name} ({self.total_credits} total credits)>"

    def get_by_url(self, url):
        response = requests.get(url)
        html_string = response.text
        return bs4.BeautifulSoup(html_string, "html.parser")

    def _parse_name(self):
        return self.soup.h1.text.split("\n")[0].strip()

    def _parse_credits(self):
        filmography_div = self.soup.find("div", {"id": "filmography"})
        credit_head_divs = filmography_div.find_all(
            "div", id=lambda x: x and x.startswith("filmo-head-")
        )
        credit_content_divs = filmography_div.find_all(
            "div", {"class": "filmo-category-section"}
        )
        assert len(credit_head_divs) == len(
            credit_content_divs
        ), "Category headers do not match sections, cannot parse."

        credit_lookup = {}
        for idx, credit_head_div in enumerate(credit_head_divs):
            category_name_full = credit_head_div.text.split("\n")[3]
            n_credits = [int(x) for x in re.findall(r"\d+", category_name_full)][-1]
            category_name = category_name_full.split(f"({n_credits} credits)")[
                0
            ].strip()
            items = credit_content_divs[idx].find_all("div", {"class": "filmo-row"})

            credit_lookup[category_name] = {"n_credits": n_credits, "credits": []}

            for item in items:
                credit_year = item.find("span", {"class": "year_column"}).text.strip()
                credit_title = item.b.a.text.strip()
                # this is super hacky: get all next siblings from the title, join them, and then re-parse to remove HTML
                credit_description = bs4.BeautifulSoup(
                    "".join([str(x).strip() for x in item.b.next_siblings]),
                    "html.parser",
                ).text

                credit_lookup[category_name]["credits"].append(
                    {
                        "year": credit_year,
                        "title": credit_title,
                        "description": credit_description,
                    }
                )

        return credit_lookup


if __name__ == "__main__":
    # Build CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("name_id", help="IMDb name identifier")
    args = parser.parse_args()

    # Run program
    imdb_url = ImdbUrl.get_by_name_id(args.name_id)  # generate the IMDb URL
    person = Person(imdb_url)  # do the parsing

    print(f"Retrieved credits for {person.name}.")
