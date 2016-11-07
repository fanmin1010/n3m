import jwtDecode from 'jwt-decode';

import { createReducer } from '../utils/misc';
import {
    CHAT_MESSAGES_SUCCESS,
    CHAT_MESSAGES_FAILURE,
    CHAT_MESSAGES_REQUEST,
} from '../constants/index';

const initialState = {
  partyName: null,
  messages: [],
  messagesStatusText: null,
};


export default createReducer(initialState, {
  [CHAT_MESSAGES_REQUEST]: (state, payload) =>
        Object.assign({}, state, {
          partyname: null,
          messages: [],
          messagesStatusText: null,
        }),
  [CHAT_MESSAGES_SUCCESS]: (state, payload) =>
        Object.assign({}, state, {
          partyname: payload.partyname,
          messages: payload.messages,
          messagesStatusText: 'messages retreived successfully.',
        }),
  [CHAT_MESSAGES_FAILURE]: (state, payload) =>
        Object.assign({}, state, {
          partyname: null,
          messages: [],
          messagesStatusText: 'error retreiving messages.',
        }),
});

