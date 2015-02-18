#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections.abc import Callable

from contextlib import contextmanager


class BaseState:
    @classmethod
    def on_enter(cls, obj):
        pass

    @classmethod
    def on_exit(cls, obj):
        pass


class MultiBehavioral:
    default_states = {}

    def __init__(self):
        self.states = super().__getattribute__('__class__').default_states.copy()
        self.base_dict = self.__dict__.copy()
        self.base_dict.update({'base_dict': self.base_dict})

        states = list(self.states.values())
        for state in states:
            self.__dict__.update(state.__dict__)
            try:
                state.on_enter(self)
            except AttributeError:
                pass

    @contextmanager
    def state(self, state):
        self.enter(state)
        yield self
        self.exit(state)

    def enter(self, state):
        self.states[state.state_type] = state
        if not (state.breadth and self.states[state.state_type] is state):
            try:
                self.states[state.state_type].on_exit(self)
            except AttributeError:
                pass
            try:
                state.on_enter(self)
            except AttributeError:
                pass

    def exit(self, state):
        new_state = self.default_states[state.state_type]
        self.states[state.state_type] = new_state
        try:
            state.on_exit(self)
        except AttributeError:
            pass
        try:
            new_state.on_enter(self)
        except AttributeError:
            pass

    def __getattribute__(self, attr):
        for state in super(MultiBehavioral, self).__getattribute__('states').values():
            try:
                if isinstance(state.__dict__[attr], Callable):
                    if not isinstance(state.__dict__[attr], classmethod):
                        return state.__dict__[attr].__get__(self, super().__getattribute__('__class__'))
                else:
                    return state.__dict__[attr]
            except KeyError:
                continue
        return super().__getattribute__(attr)