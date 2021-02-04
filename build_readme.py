import pathlib
import httpx
import re
import os

root = pathlib.Path(__file__).parent.resolve()
TOKEN = os.environ.get("GH_TOKEN", "")

def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        rf"<!\-\- {marker} start \-\->.*<!\-\- {marker} end \-\->",
        re.DOTALL,
    )
    if not inline:
        chunk = f"\n{chunk}\n"
    chunk = f"<!-- {marker} start -->{chunk}<!-- {marker} end -->"
    return r.sub(chunk, content)

def fetch_code_time():
    return httpx.get(
        "https://gist.githubusercontent.com/zephyrxvxx7/ee1787313f0772b51494d051b5edde7f/raw/"
    )


if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.open().read()

    code_time_text = f"\n```text\n{fetch_code_time().text}\n```\n"
    readme_contents = replace_chunk(readme_contents, "code_time", code_time_text)

    readme.open("w").write(readme_contents)