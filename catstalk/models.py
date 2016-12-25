# -*- coding: utf-8 -*-

from peewee import Model, TextField, DateTimeField, CharField, \
    ForeignKeyField
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase("blog_data.sqlite3")


class BaseModel(Model):
    class Meta:
        database = db


class Tag(BaseModel):
    name = CharField(unique=True)


class Post(BaseModel):
    tag = ForeignKeyField(Tag, null=True)
    title = CharField(unique=True)
    date = DateTimeField()
    content = TextField()


db.create_tables([Tag, Post])
