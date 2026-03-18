def process_batch(files):

    results = []

    for f in files:
        results.append({
            "file": f,
            "status": "processed"
        })

    return results