#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Common config vars.

this = None


class Config:
    last_file = ""

    def __init__(self):
        pass

    def set_last_file(self, filename):
        self.last_file = filename

    def get_last_file(self):
        return self.last_file


def get_instance():
    global this
    if this == None:
        this = Config()
    return this
