def noteEntity(item) -> dict:
    return{
        "id":str(item["_id"]),
        "title":item["title"],
        "desc":item["desc"],
        "important":item["important"],
        
    }


def notesEntity(item)->list:
    return [noteEntity(item) for item in items]