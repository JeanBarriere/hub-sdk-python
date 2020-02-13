# -*- coding: utf-8 -*-
from peewee import TextField, UUIDField

from storyhub.sdk.db.BaseModel import BaseModel


class Service(BaseModel):
    uuid = UUIDField(primary_key=True)
    name = TextField(index=True)
    description = TextField(null=True)
    configuration = TextField()
