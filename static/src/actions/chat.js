import {
    CHAT_MESSAGES_REQUEST,
    CHAT_MESSAGES_SUCCESS,
    CHAT_MESSAGES_FAILURE,
    FRIEND_LIST_REQUEST,
    FRIEND_LIST_SUCCESS,
    FRIEND_LIST_FAILURE,
    ADD_FRIEND_REQUEST,
    ADD_FRIEND_SUCCESS,
    ADD_FRIEND_FAILURE,
    NEW_CHAT_CHANNEL,
    ADD_MESSAGE,
    SET_IS_PARTY,
} from '../constants/index';

import { parseJSON } from '../utils/misc';
import { 
        socket_msg,
        socket_party_msg,
         callUberCall,
         friendlistCall,
         addFriendCall,
       } from '../utils/http_functions';


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


export function send_chat(msg, partyname, receiver, sender) {
  return function (dispatch) {
    dispatch(chatMessagesRequest());
    return socket_msg(msg, partyname, receiver, uname, () => {
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

export function send_party_chat(msg, partyname, uname) {
  return function (dispatch) {
    dispatch(chatMessagesRequest());
    return socket_party_msg(msg, partyname, uname, () => {
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

export function setIsParty(isParty, receiver) {
  return {
    type: SET_IS_PARTY,
    payload: {
      isParty: isParty,
      receiver, receiver,
    }
  };
}

/**
 * @param partyname {string} in this case the partyname field is used for either one-on-one chats or party chats. 
 * @param isParty {boolean} tells us if this is a party or one-on-one chat.
 * @param receiver {receiver} the username of the user receiving one-on-one chat.
 **/
export function setNewListener(partyname, isParty, receiver) {
  return function (dispatch) {
    dispatch(setIsParty(isParty, receiver));
    socket.removeAllListeners();
    socket.on(partyname, (data) => {
      dispatch(addMessage(partyname, data));
      document.getElementById('messagelist').scrollTop = 9999;
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

export function getFriendList() {
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


export function addFriendRequest() {
  return {
    type: ADD_FRIEND_REQUEST,
  };
}

export function addFriendSuccess(payload) {
  return {
    type: ADD_FRIEND_SUCCESS,
  };
}

export function addFriendFailure(error) {
  return {
    type: ADD_FRIEND_FAILURE,
    payload: error,
  };
}

export function addFriend(email) {
  return function (dispatch) {
    dispatch(addFriendRequest());
    const token = localStorage.getItem('token');
    console.log('inside of the addFriend action');
    console.log(email);
    return addFriendCall(email, token, () => {
      try {
        dispatch(addFriendSuccess());
        console.log('inside of add friend but about to call getfriendlist');
        dispatch(getFriendList());
      } catch (e) {
        console.log('There was an error while adding a friend');
        console.dir(e);
        dispatch(addFriendFailure());
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
