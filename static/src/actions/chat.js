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
      partyname: partyname,
    }
  };
}


export function addMessage(message) {
  return {
    type: ADD_MESSAGE,
    payload: message
  };
}


function _receiveMessage(data) {
  console.log(data);
  console.log('$$$$$$$$$$$$$$$$$$$$$$$$$$');
  addMessage(data);
 // setTimeout(function(){const m = document.getElementById('messagelist');
 //   m.scrollTop = 9999;
 //   document.getElementById('chatinput').value = '';
 // }, 200);
}


export function setNewListener(partyname) {
  return function(dispatch) {
    console.log('Inside setNewListener');
    console.log('partyname: ' + partyname);
    socket.removeAllListeners();
    socket.on(partyname, function(data){
      dispatch(addMessage(data));
    }); 
  }
}



export function friendListRequest() {
  return {
    type: FRIEND_LIST_REQUEST,
  };
}

export function friendListSuccess(payload) {
  return {
    type: FRIEND_LIST_SUCCESS,
    payload: payload
  };
}

export function friendListFailure(error) {
  return {
    type: FRIEND_LIST_FAILURE,
    payload: error,
  };
}

export function getFriendList(uname) {
  return function(dispatch){
    console.log('inside getFriendList');
    dispatch(friendListRequest());
    var token = localStorage.getItem('token');
    return friendlistCall(token, (data) => {
      try {
        dispatch(friendListSuccess(data));
      } catch (e) {
        console.log('There was an error while calling friendlist');
        console.dir(e);
        dispatch(friendListFailure());
      }
    });

  }
}

export function callUber() {
  console.log('inside of the callUber function');
  return function (dispatch) {
    return callUberCall()
            .then(parseJSON)
            .then(response => {
              try {
                console.log('Calll uber Call');
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
