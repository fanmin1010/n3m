import jwtDecode from 'jwt-decode';

import { createReducer } from '../utils/misc';
import {
    CHAT_MESSAGES_SUCCESS,
    CHAT_MESSAGES_FAILURE,
    CHAT_MESSAGES_REQUEST,
    NEW_CHAT_CHANNEL,
    ADD_MESSAGE,
} from '../constants/index';

const initialState = {
  partyname: 'Lobby',
  messages: [],
  messagesStatusText: null,
};


export default createReducer(initialState, {
  [CHAT_MESSAGES_REQUEST]: (state, payload) =>
        Object.assign({}, state, {
          messagesStatusText: null,
        }),
  [CHAT_MESSAGES_SUCCESS]: (state, payload) => {
   console.log('chatmessagesuccess.');
   console.dir(payload);
    return Object.assign({}, state, {
          messagesStatusText: 'messages retreived successfully.',
        })},
  [CHAT_MESSAGES_FAILURE]: (state, payload) =>
        Object.assign({}, state, {
          messagesStatusText: 'error retreiving messages.',
        }),
  [NEW_CHAT_CHANNEL]: (state, payload) => {
      return Object.assign({}, state, {
          partyname: payload.partyname,
          messages: [],
          messagesStatusText: null,
        })},
  [ADD_MESSAGE]: (state, payload) => {
      console.log('----------------');
      console.dir(payload);  
      console.dir(state);
      console.log(state.messages.slice().concat([payload]));
    return Object.assign({}, state, {
          messages: state.messages.slice().concat([payload]),
          messagesStatusText: null,
        })},
});

