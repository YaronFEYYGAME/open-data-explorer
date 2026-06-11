import requests

BASE_URL = "https://www.data.gouv.fr/api/1"

def safe_request(url: str, params: dict = None) -> dict:
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        raise RuntimeError("L'API ne répond pas (timeout).")
    except requests.ConnectionError:
        raise RuntimeError("Problème réseau.")
    except requests.HTTPError as e:
        code = e.response.status_code
        if code == 404:
            raise RuntimeError("Ressource introuvable (404).")
        if code == 429:
            raise RuntimeError("Trop de requêtes, réessaie plus tard (429).")
        raise RuntimeError(f"Erreur HTTP {code}.")
    except ValueError:
        raise RuntimeError("La réponse n'est pas du JSON valide.")



def search_datasets(query: str, page_size: int = 10) -> dict:
    url = f"{BASE_URL}/datasets/"
    params = {
            "q": query,
            "page_size": page_size,
            "sort": "-last_update",
    }
    return safe_request(url, params)


def get_dataset(dataset_id: str) -> dict:
    url = f"{BASE_URL}/datasets/{dataset_id}/"
    return safe_request(url)
