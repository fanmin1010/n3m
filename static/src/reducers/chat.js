import jwtDecode from 'jwt-decode';

import { createReducer } from '../utils/misc';
import {
    CHAT_MESSAGES_SUCCESS,
    CHAT_MESSAGES_FAILURE,
    CHAT_MESSAGES_REQUEST,
    FRIEND_LIST_SUCCESS,
    FRIEND_LIST_FAILURE,
    FRIEND_LIST_REQUEST,
    ADD_FRIEND_SUCCESS,
    ADD_FRIEND_FAILURE,
    ADD_FRIEND_REQUEST,
    NEW_CHAT_CHANNEL,
    ADD_MESSAGE,
    SET_IS_PARTY,
    PARTY_LIST_SUCCESS,
    PARTY_LIST_FAILURE,
    PARTY_LIST_REQUEST,
    ADD_PARTY_SUCCESS,
    ADD_PARTY_FAILURE,
    ADD_PARTY_REQUEST,
} from '../constants/index';

const initialState = {
  partyname: 'Lobby',
  receiver: null,
  friendlist: [],
  friendListStatusText: null,
  messages: [],
  allMessages: {},
  messagesStatusText: null,
  addFriendStatusText: null,
  isParty: true,
  partylist: [],
  partyListStatusText: null,
  addPartyStatusText: null,
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
        }); },
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
        }); },
  [FRIEND_LIST_FAILURE]: (state, payload) =>
        Object.assign({}, state, {
          friendListStatusText: 'error retreiving friendlist.',
        }),
  [NEW_CHAT_CHANNEL]: (state, payload) => {
      console.log('In NEW_CHAT_CHANNEL reducer');
      //console.dir(payload);
      var updatedAllMessages =  Object.assign({}, ({ [payload.partyname]: [] }), state.allMessages);
      //console.log('allmessages: ');
      //console.dir(updatedAllMessages);
      var updatedMessages = updatedAllMessages[payload.partyname].slice();
      //console.log('messages: ');
      //console.dir(updatedMessages);
      var newstate =  Object.assign({}, state, {
          partyname: payload.partyname,
          allMessages: updatedAllMessages,
          messages: updatedMessages,
          messagesStatusText: null,
        }); 
      //console.log('----__------__');
      //console.dir(newstate);
    return newstate;
  },

  [ADD_MESSAGE]: (state, payload) => {
    console.log('In ADD_MESSAGE reducer');
    console.dir(payload);
    return Object.assign({}, state, {
          allMessages: Object.assign({}, state.allMessages, { [payload.partyname]: state.allMessages[payload.partyname].slice().concat([payload.message]) }),
          messages: state.allMessages[payload.partyname].slice().concat([payload.message]),
          messagesStatusText: null,
        }); },
  [ADD_FRIEND_REQUEST]: (state, payload) =>
        Object.assign({}, state, {
          addFriendStatusText: null,
        }),
  [ADD_FRIEND_SUCCESS]: (state, payload) => {
   console.log('addfriend success.');
    return Object.assign({}, state, {
          addFriendStatusText: 'addFriend done successfully.',
        }); },
  [ADD_FRIEND_FAILURE]: (state, payload) =>
        Object.assign({}, state, {
          addFriendStatusText: 'error adding a friend.',
        }),
  [SET_IS_PARTY]: (state, payload) =>
        Object.assign({}, state, {
          isParty: payload.isParty,
          receiver: payload.receiver,
        }),
  [PARTY_LIST_REQUEST]: (state, payload) =>
        Object.assign({}, state, {
          partyListStatusText: null,
        }),
  [PARTY_LIST_SUCCESS]: (state, payload) => {
   console.log('partylistsuccess.');
   console.dir(payload);
    return Object.assign({}, state, {
          partyListStatusText: 'partylist retreived successfully.',
          partylist: payload.data,
        }); },
  [PARTY_LIST_FAILURE]: (state, payload) =>
        Object.assign({}, state, {
          partyListStatusText: 'error retreiving partylist.',
        }),
  [ADD_PARTY_REQUEST]: (state, payload) =>
        Object.assign({}, state, {
          addPartyStatusText: null,
        }),
  [ADD_PARTY_SUCCESS]: (state, payload) => {
   console.log('addparty success.');
    return Object.assign({}, state, {
          addPartyStatusText: 'addParty done successfully.',
        }); },
  [ADD_PARTY_FAILURE]: (state, payload) =>
        Object.assign({}, state, {
          addPartyStatusText: 'error adding a party.',
        }),
});

