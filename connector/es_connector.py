from .config import es_config 
from elasticsearch import Elasticsearch
import json

class ES:
    
    es_conn = Elasticsearch(hosts = es_config.hosts, http_auth=es_config.auth)
    
    @classmethod
    def srvHealthCheck(cls):
        health = cls.es_conn.cluster.health()
        print(health)

    @classmethod
    def allIndex(cls):
        # Elasticsearch에 있는 모든 Index 조회
        print(cls.es_conn.cat.indices())

    @classmethod
    def dataInsert(cls,index: str,data: dict):
        # ===============
        # 데이터 삽입
        # ===============
        
        res = cls.es_conn.index(index=index, body=data)
        print(res)

    @classmethod
    def searchAll(cls, index: str=None):
        # ===============
        # 데이터 조회 [전체]
        # ===============
        res = cls.es_conn.search(
            index = index,
            body = {
                "query":{"match_all":{}}
            }
        )
        print(json.dumps(res, ensure_ascii=False, indent=4))

    @classmethod
    def searchFilter(cls,index: str,body: dict):
        # ===============
        # 데이터 조회 []
        # ===============
        res = cls.es_conn.search(
            index = index,
            body = body
        )
        print(res)

    @classmethod
    def createIndex(cls,index: str,body: dict=None):
        # ===============
        # 인덱스 생성
        # ===============
        cls.es_conn.indices.create(
            index = index,
            body = body
        )
        
    @classmethod
    def deleteIndex(cls,index: str):
        cls.es_conn.indices.delete(
            index = index
        )
