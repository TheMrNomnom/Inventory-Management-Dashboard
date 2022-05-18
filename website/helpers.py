def query_to_dict(query):
    """
    Convert a query to a list of dictionaries.
    """
    return [query.__dict__ for query in query]