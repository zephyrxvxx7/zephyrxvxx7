import pathlib
import httpx
import re
import os

root = pathlib.Path(__file__).parent.resolve()
TOKEN = os.environ.get("GH_TOKEN", "")

code_time_url = "https://gist.githubusercontent.com/zephyrxvxx7/ee1787313f0772b51494d051b5edde7f/raw/"
code_diff_url = "https://gist.githubusercontent.com/zephyrxvxx7/08c5ff0fead26978490fef5d749f43ea/raw/"
steam_time_url = "https://gist.githubusercontent.com/zephyrxvxx7/f77b8978877f959b69d84723c43a4a64/raw/"
spotify_track_url = "https://gist.githubusercontent.com/zephyrxvxx7/fe159fde5ec9ebea27e03dd63a71e78f/raw/"

def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        rf"<!\-\- {marker} start \-\->.*<!\-\- {marker} end \-\->",
        re.DOTALL,
    )
    if not inline:
        chunk = f"\n{chunk}\n"
    chunk = f"<!-- {marker} start -->{chunk}<!-- {marker} end -->"
    return r.sub(chunk, content)

def httpx_get(url):
    return httpx.get(url)


if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.open().read()

    code_time_text = f"\n```text\n{httpx_get(code_time_url).text}\n```\n"
    readme_contents = replace_chunk(readme_contents, "code_time", code_time_text)

    code_diff_text = f"\n```text\n{httpx_get(code_diff_url).text}\n```\n"
    readme_contents = replace_chunk(readme_contents, "code_diff", code_diff_text)

    steam_time_text = f"\n```text\n{httpx_get(steam_time_url).text}\n```\n"
    readme_contents = replace_chunk(readme_contents, "steam_time", steam_time_text)

    spotify_track_text = f"\n```text\n{httpx_get(spotify_track_url).text}\n```\n"
    readme_contents = replace_chunk(readme_contents, "spotify_track", spotify_track_text)

    readme.open("w").write(readme_contents)