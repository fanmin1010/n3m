import {
    CHAT_MESSAGES_REQUEST,
    CHAT_MESSAGES_SUCCESS,
    CHAT_MESSAGES_FAILURE,
    FRIEND_LIST_REQUEST,
    FRIEND_LIST_SUCCESS,
    FRIEND_LIST_FAILURE,
    NEW_CHAT_CHANNEL,
    ADD_MESSAGE,
} from '../constants/index';

import { parseJSON } from '../utils/misc';
import { socket_msg, callUberCall, friendlistCall } from '../utils/http_functions';


export function chatMessagesRequest() {
  return {
    type: CHAT_MESSAGES_REQUEST,
  };
}

export function chatMessagesSuccess() {
  return {
    type: CHAT_MESSAGES_SUCCESS,
  };
}

export function chatMessagesFailure(error) {
  return {
    type: CHAT_MESSAGES_FAILURE,
    payload: error,
  };
}


export function send_chat(msg, teamname, uname) {
  return function (dispatch) {
    dispatch(chatMessagesRequest());
    return socket_msg(msg, teamname, uname, () => {
      try {
        dispatch(chatMessagesSuccess());
      } catch (e) {
        console.log('There was an error while calling socket_msg');
        console.dir(e);
        dispatch(chatMessagesFailure());
      }
    });
  };
}


export function setChatWindow(partyname) {
  return {
    type: NEW_CHAT_CHANNEL,
    payload: {
      partyname,
    },
  };
}


export function addMessage(partyname, message) {
  return {
    type: ADD_MESSAGE,
    payload: {
      message,
      partyname,
    },
  };
}


export function setNewListener(partyname) {
  return function (dispatch) {
    socket.removeAllListeners();
    socket.on(partyname, (data) => {
      dispatch(addMessage(partyname, data));

    });
  };
}


export function friendListRequest() {
  return {
    type: FRIEND_LIST_REQUEST,
  };
}

export function friendListSuccess(payload) {
  return {
    type: FRIEND_LIST_SUCCESS,
    payload,
  };
}

export function friendListFailure(error) {
  return {
    type: FRIEND_LIST_FAILURE,
    payload: error,
  };
}

export function getFriendList(uname) {
  return function (dispatch) {
    dispatch(friendListRequest());
    const token = localStorage.getItem('token');
    return friendlistCall(token, (data) => {
      try {
        dispatch(friendListSuccess(data));
      } catch (e) {
        console.log('There was an error while calling friendlist');
        console.dir(e);
        dispatch(friendListFailure());
      }
    });

  };
}

export function callUber() {
  return function (dispatch) {
    return callUberCall()
            .then(parseJSON)
            .then(response => {
              try {
                console.log(response);
              } catch (e) {
                console.log(e);
              }
            })
            .catch(error => {
              console.log(error);
            });
  };
}
