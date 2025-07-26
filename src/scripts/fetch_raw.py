import subprocess
import json


def fetch_raw():
    try:
        result = subprocess.run(
            [
                "gh",
                "api",
                "repos/immich-app/immich/pulls?state=closed",
                "--method=GET",
                "--paginate",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        json_data = json.loads(result.stdout)
        with open(".data/raw/pull_requests.json", "w") as f:
            json.dump(json_data, f, indent=4)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        return None


_ = fetch_raw()
