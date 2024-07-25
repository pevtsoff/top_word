from fastapi import HTTPException


class InvalidTopicData(Exception):
    pass


class NoValidTopicExists(HTTPException):
    pass
