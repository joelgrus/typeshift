from typing import TypeVar
import dataclasses

from typeshift.words import common_words
from typeshift.talk1 import Spec
from typeshift.talk4 import greedy_puzzle

import streamlit as st

StateT = TypeVar('StateT')

def persistent_game_state(initial_state: StateT) -> StateT:
    session_id = st.report_thread.get_report_ctx().session_id
    session = st.server.server.Server.get_current()._get_session_info(session_id).session
    if not hasattr(session, '_gamestate'):
        setattr(session, '_gamestate', initial_state)
    return session._gamestate


@dataclasses.dataclass
class GameState:
    original_spec: Spec
    remaining_spec: Spec

word_length = st.slider("word length", min_value=3, max_value=10, step=1, value=4)

def make_spec()-> Spec:
    game = greedy_puzzle(word_length)
    return Spec.from_words(game, set(common_words))

def make_state() -> GameState:
    spec = make_spec()
    return GameState(spec, spec)

state = persistent_game_state(initial_state=make_state()) 

if st.button("new game"):
    new_spec = make_spec()
    state.original_spec = state.remaining_spec = new_spec

for constraint in state.original_spec.constraints:
    st.text(''.join(constraint))

