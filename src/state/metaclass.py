#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.state.mother import BaseState


class MetaState(type):
    def __new__(mcs, name, bases, members, breadth=False):
        if len(bases) > 1:
            raise IndexError('States does not support multiple inheritance.')
        members['state_type'] = bases[0]

        return super(MetaState, mcs).__new__(mcs, name, (BaseState,), members)

    def __init__(cls, name, bases, members, breadth=False):
        super().__init__(name, (BaseState,), members)
        cls.breadth = breadth

    def __repr__(cls):
        return "<{} '{}.{}'>".format(cls.state_type.__name__, cls.__module__, cls.__name__)


def state(breadth=False):
    def cls_wrapper(cls):
        return MetaState(
            cls.__name__,
            cls.__bases__,
            dict(cls.__dict__),
            breadth=breadth
        )

    return cls_wrapper