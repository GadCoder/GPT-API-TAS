import requests


def get_info_from_context(context: str):
    info_from_api = get_info_from_api(context=context)
    if info_from_api is None:
        return None
    return transfrom_results(info_results=info_from_api)


def get_info_from_api(context: str):
    url = f"https://api-tas.gadsw.dev/data-element/get-latest-elements-from-type/?type={context}&delay_in_days=7"
    headers = {"accept": "application/json"}
    request = requests.get(url, headers=headers)
    if request.status_code == 200:
        return request.json()
    return None


def transfrom_results(info_results: list):
    if isinstance(info_results, list):  # Check if the response is a list of objects
        info_context = "Here is the information we found:\n\n"
        for item in info_results:
            # Extract and format relevant fields
            info_context += (
                f"Title: {item['title']}\n"
                f"Content: {item['content']}\n"
                f"Type: {item['type']}\n"
                f"URL: {item['url']}\n"
                f"Created At: {item['created_at']}\n\n"
            )
        return info_context
    else:
        info_context = "Here is the information we found:\n\n" + str(info_results)
