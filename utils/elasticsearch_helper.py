from elasticsearch import Elasticsearch

# Elasticsearchga ulanish
es = Elasticsearch(["https://localhost:9200"], verify_certs=False)

# Ma'lumotlarni Elasticsearch'ga kiritish uchun yordamchi funksiya
def index_material(material):
    document = {
        "material_csr_code": material.material_csr_code,
        "material_name": material.material_name,
        "material_desc": material.material_desc,
        "material_measure": material.material_measure,
        "material_group_id": material.material_group_id,
        "material_image": material.material_image,
        "material_views_count": material.material_views_count,
        "materil_gost": material.materil_gost
    }
    es.index(index="materials_index", id=material.material_csr_code, body=document)