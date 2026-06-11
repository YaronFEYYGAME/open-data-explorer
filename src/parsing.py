def parse_dataset(raw: dict) -> dict:
    org = raw.get("organization") or raw.get("owner") or {}
    return {
        "id": raw.get("id", ""),
        "title": raw.get("title", "Sans titre"),
        "description": raw.get("description", "Aucune description"),
        "organization": org.get("name", "Non renseigné") if isinstance(org, dict) else "Non renseigné",
        "created_at": raw.get("created_at", "Non renseigné"),
        "last_update": raw.get("last_modified", "Non renseigné"),
        "license": raw.get("license", "Non renseigné"),
        "tags": [t.get("name", "") if isinstance(t, dict) else t for t in raw.get("tags",[])],
        "nb_resources": len(raw.get("resources", [])),
        "url": raw.get("page", ""),
    }


def parse_resources(raw: dict) -> list:
    exploitable_formats = {"csv", "json", "xlsx", "xml"}
    resources = []
    for r in raw.get("resources", []):
        fmt = (r.get("format") or "").lower().strip()
        resources.append({
            "title": r.get("title", "Sans titre"),
            "format": fmt or "inconnu",
            "type": r.get("type", "Non renseigné"),
            "size": r.get("filesize"),
            "url": r.get("url", ""),
            "exploitable": fmt in exploitable_formats,
        })
    return resources

def parse_search_results(data: dict) -> list:
    return [parse_dataset(d) for d in data.get("data", [])]
