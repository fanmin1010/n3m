import {
    CHAT_MESSAGES_REQUEST,
    CHAT_MESSAGES_SUCCEESS,
    CHAT_MESSAGES_FAILURE,
} from '../constants/index';

import { parseJSON } from '../utils/misc';
import { socket_msg } from '../utils/http_functions';


export function chatMessagesRequest() {
  return {
    type: CHAT_MESSAGES_REQUEST,
  };
}

export function chatMessagesSuccess(payload) {
  return {
    type: CHAT_MESSAGES_SUCCESS,
    payload,
  };
}

export function chatMessagesFailure(error) {
  return {
    type: CHAT_MESSAGES_FAILURE,
    payload: error,
  };
}


export function send_chat(msg, teamid, uname) {
  return function (dispatch) {
    dispatch(chatMessagesRequest());
    return socket_msg(msg, teamid, uname, (response) => {
      try {
        console.log(response);
        dispatch(chatMessagesSuccess(response.messageData));
      } catch (e) {
        dispatch(chatMessagesFailure());
      }
    });
  };
}
