import jwtDecode from 'jwt-decode';

import { createReducer } from '../utils/misc';
import {
    CHAT_MESSAGES_SUCCESS,
    CHAT_MESSAGES_FAILURE,
    CHAT_MESSAGES_REQUEST,
    FRIEND_LIST_SUCCESS,
    FRIEND_LIST_FAILURE,
    FRIEND_LIST_REQUEST,
    NEW_CHAT_CHANNEL,
    ADD_MESSAGE,
} from '../constants/index';

const initialState = {
  partyname: 'Lobby',
  friendlist: [],
  friendListStatusText: null,
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
  [FRIEND_LIST_REQUEST]: (state, payload) =>
        Object.assign({}, state, {
          friendListStatusText: null,
        }),
  [FRIEND_LIST_SUCCESS]: (state, payload) => {
   console.log('friendlistsuccess.');
   console.dir(payload);
    return Object.assign({}, state, {
          friendListStatusText: 'friendlist retreived successfully.',
          friendlist: payload.data,
        })},
  [FRIEND_LIST_FAILURE]: (state, payload) =>
        Object.assign({}, state, {
          friendListStatusText: 'error retreiving friendlist.',
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

