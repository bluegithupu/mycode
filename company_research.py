async def tool_node(state):
    # ... 前面的代码 ...
    
    for doc in search_results:
        if doc is not None and 'url' in doc:
            docs[doc['url']] = doc
    
    # ... 后面的代码 ...
