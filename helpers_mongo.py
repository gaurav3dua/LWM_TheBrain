import config
import pymongo

conn_string = config.get_mongo_connection_string()
client = pymongo.MongoClient(conn_string)


def search_records(db_name, col_name, query, fields_required=None, is_id_required=False, sorting_fields=None):
    """
        Search for records in mongo db using a query along with sorting
    :param db_name: <string> database name
    :param col_name: <string> collection name
    :param query: <dict> search query
    :param fields_required: <list> list of fields required
    :param is_id_required: <boolean> if ids of the documents are required. By default, False
    :param sorting_fields: <list <tuple <string>, <int>>> field on which sorting is required. By default, no sorting
                            Eg. [("field_a", 1), ("field_b", -1)]
    :return:
    """
    col = client[db_name][col_name]
    if is_id_required is False:
        id_required = 0
    else:
        id_required = 1

    fields_needed = {
        "_id": id_required
    }

    if fields_required is not None:
        for i in fields_required:
            fields_needed[i] = 1

    if sorting_fields is None:
        res = col.find(query, fields_needed)
    else:
        res = col.find(query, fields_needed).sort(sorting_fields)

    records = list()
    for i in res:
        records.append(i)
    return records


def upload_records(db_name, col_name, records):
    """
        Upload multiple records to mongo db
    :param db_name: <string> database name
    :param col_name: <string> collection name
    :param records: <list <dict>> records to be inserted
    :return:
    """
    col = client[db_name][col_name]
    x = col.insert_many(records)
    inserted_records = x.inserted_ids
    total_inserted_records = len(inserted_records)
    if total_inserted_records > 0:
        return total_inserted_records
    else:
        return 0


def delete_records_by_query(db_name, col_name, query):
    """

    :param db_name:
    :param col_name:
    :param query:
    :return:
    """
    col = client[db_name][col_name]
    deleted_records = col.delete_many(query)
    total_deleted_records = deleted_records.deleted_count
    if total_deleted_records > 0:
        return total_deleted_records
    else:
        return 0
