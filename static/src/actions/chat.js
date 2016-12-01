import {
    CHAT_MESSAGES_REQUEST,
    CHAT_MESSAGES_SUCCESS,
    CHAT_MESSAGES_FAILURE,
    FRIEND_LIST_REQUEST,
    FRIEND_LIST_SUCCESS,
    FRIEND_LIST_FAILURE,
    FRIEND_HISTORY_REQUEST,
    FRIEND_HISTORY_SUCCESS,
    FRIEND_HISTORY_FAILURE,
    ADD_FRIEND_REQUEST,
    ADD_FRIEND_SUCCESS,
    ADD_FRIEND_FAILURE,
    NEW_CHAT_CHANNEL,
    ADD_MESSAGE,
    SET_IS_PARTY,
    PARTY_LIST_REQUEST,
    PARTY_LIST_SUCCESS,
    PARTY_LIST_FAILURE,
    ADD_PARTY_REQUEST,
    ADD_PARTY_SUCCESS,
    ADD_PARTY_FAILURE,
} from '../constants/index';

import { parseJSON } from '../utils/misc';
import { 
        socket_msg,
        socket_party_msg,
         callUberCall,
         callOpenTableCall,
         friendlistCall,
         friendHistoryCall,
         addFriendCall,
         addFriendToPartyCall,
         addPartyCall,
         partylistCall,
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
    return socket_msg(msg, partyname, receiver, sender, () => {
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

export function send_party_chat(msg, partyname, partyId, uname) {
  return function (dispatch) {
    dispatch(chatMessagesRequest());
    return socket_party_msg(msg, partyname, partyId, uname, () => {
      try {
        dispatch(chatMessagesSuccess());
      } catch (e) {
        console.log('There was an error while calling socket_party_msg');
        console.dir(e);
        dispatch(chatMessagesFailure());
      }
    });
  };
}


export function setChatWindow(partyname, partyId) {
  console.log(partyname);
  var partyId = partyId || -1
  return {
    type: NEW_CHAT_CHANNEL,
    payload: {
      partyname: partyname,
      partyId: partyId,
    },
  };
}


export function addMessage(partyname, message) {
  return {
    type: ADD_MESSAGE,
    payload: {
      message: message,
      partyname: partyname,
    },
  };
}

export function setIsParty(isParty, receiver) {
  return {
    type: SET_IS_PARTY,
    payload: {
      isParty: isParty,
      receiver: receiver,
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
    console.log('setting up listener on ' + partyname);
    console.log(partyname);
    socket.on(partyname, (data) => {
      console.log('received message from server');
      console.log(data);
      dispatch(addMessage(partyname, data));
      document.getElementById('messagelist').scrollTop = 9999;
    });
  };
}

export function setGeoListener(username){
  return function(dispatch) {
    socket.on(username+'__geo', (data) => {
      console.log('Inside of the setGeoListener awesome');
      console.dir(data);
      navigator.geolocation.getCurrentPosition(function(position){
        console.log('got the position information for user:');
        console.dir(position);
        socket.emit('geodata', {'partyname': data.partyname, 'username': username, 'msgtext': data.msgtext, 'username': username, 'latitude': position.coords.latitude.toFixed(3), 'longitude': position.coords.longitude.toFixed(3)});
      });
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

export function friendHistoryRequest() {
  return {
    type: FRIEND_HISTORY_REQUEST,
  };
}

export function friendHistorySuccess(messages) {
  return {
    type: FRIEND_HISTORY_SUCCESS,
    payload: {
      messages: messages
    },
  };
}

export function friendHistoryFailure(error) {
  return {
    type: FRIEND_HISTORY_FAILURE,
    payload: error,
  };
}

export function getFriendHistory(friendName) {
  return function (dispatch) {
    dispatch(friendHistoryRequest());
    const token = localStorage.getItem('token');
    return friendHistoryCall(friendName, token, (data) => {
      console.dir('The data in friend History');
      console.dir(data.data);
      try {
        dispatch(friendHistorySuccess(data.data));
        document.getElementById('messagelist').scrollTop = 9999;
      } catch (e) {
        console.log('There was an error while calling friendHistory');
        console.dir(e);
        dispatch(friendHistoryFailure());
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

export function partyListRequest() {
  return {
    type: PARTY_LIST_REQUEST,
  };
}

export function partyListSuccess(payload) {
  return {
    type: PARTY_LIST_SUCCESS,
    payload,
  };
}

export function partyListFailure(error) {
  return {
    type: PARTY_LIST_FAILURE,
    payload: error,
  };
}

export function getPartyList() {
  return function (dispatch) {
    console.log('In the getPartyList function');
    dispatch(partyListRequest());
    const token = localStorage.getItem('token');
    return partylistCall(token, (data) => {

      try {
        console.log('Getting back the partylist');
        console.log(data);
        dispatch(partyListSuccess(data));
      } catch (e) {
        console.log('There was an error while calling partylist');
        console.dir(e);
        dispatch(partyListFailure());
      }
    });

  };
}

export function addPartyRequest() {
  return {
    type: ADD_PARTY_REQUEST,
  };
}

export function addPartySuccess(payload) {
  return {
    type: ADD_PARTY_SUCCESS,
  };
}

export function addPartyFailure(error) {
  return {
    type: ADD_PARTY_FAILURE,
    payload: error,
  };
}

export function addParty(partyname) {
  return function (dispatch) {
    dispatch(addPartyRequest());
    const token = localStorage.getItem('token');
    console.log('inside of the addParty action');
    console.log(partyname);
    return addPartyCall(partyname, token, () => {
      try {
        dispatch(addPartySuccess());
        console.log('inside of add party and about to call getpartylist');
        dispatch(getPartyList());
      } catch (e) {
        console.log('There was an error while adding a party');
        console.dir(e);
        dispatch(addPartyFailure());
      }
    });
  };
}




export function addFriendToParty(friend, partyid) {
  return function (dispatch) {
    const token = localStorage.getItem('token');
    console.log('inside of the addFriendToParty action');
    console.log(friend, partyid);
    return addFriendToPartyCall(friend, partyid, token, () => {
      try {
        console.log('inside of add friend to the party success callback');
      } catch (e) {
        console.log('There was an error while adding a friend to the party');
        console.dir(e);
      }
    });
  };
}


export function callUber(addr) {
  return function (dispatch) {
    return callUberCall(addr)
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

export function callOpenTable(id, covers, datetime) {
  return function (dispatch) {
    return callOpenTableCall(id, covers, datetime)
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
